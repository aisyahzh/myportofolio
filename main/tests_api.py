import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Education


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.experience = Experience.objects.create(
            title="RISTEK Fasilkom UI",
            role="Member of Marketing & Communications",
            description="Contributing to marketing and communication initiatives.",
            category="organization",
            started_at="2026-03-01T00:00:00Z",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "New Experience",
            "role": "New Role",
            "description": "A new experience",
            "category": "organization",
            "thumbnail": "",
            "started_at": "2026-03-01T00:00:00Z",
            "ended_at": None,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "RISTEK"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "RISTEK Fasilkom UI")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.description,
            "Contributing to marketing and communication initiatives.",
        )
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)

        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")

        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_education",
            password="password123",
        )

        self.visitor = User.objects.create_user(
            username="visitor_education",
            password="password123",
        )

        self.editor = User.objects.create_user(
            username="editor_education",
            password="password123",
        )

        editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(editor_group)

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Belajar Sistem Informasi.",
            started_at="2025-08-01T00:00:00Z",
        )

        self.list_url = reverse("api:education-list")
        self.detail_url = reverse(
            "api:education-detail",
            kwargs={"education_id": self.education.id},
        )
        self.star_url = reverse(
            "api:education-star",
            kwargs={"education_id": self.education.id},
        )

        self.payload = {
            "institution": "University of Indonesia",
            "degree": "Bachelor of Information Systems",
            "description": "Studying information systems.",
            "thumbnail": None,
            "started_at": "2025-08-01T00:00:00Z",
            "ended_at": None,
        }

    def test_public_can_view_education_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["institution"], self.education.institution)

    def test_education_search_and_empty_result(self):
        response = self.client.get(self.list_url, {"institution": "Indonesia"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(self.list_url, {"institution": "Tidak Ada"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_missing_education_returns_404(self):
        missing_url = reverse(
            "api:education-detail",
            kwargs={"education_id": "00000000-0000-0000-0000-000000000000"},
        )

        response = self.client.get(missing_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_cannot_create_education(self):
        initial_count = Education.objects.count()

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), initial_count)

    def test_regular_user_cannot_create_update_or_delete_education(self):
        self.client.force_authenticate(user=self.visitor)
        initial_count = Education.objects.count()
        original_institution = self.education.institution

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), initial_count)

        response = self.client.patch(
            self.detail_url,
            {"institution": "Changed"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, original_institution)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Education.objects.filter(id=self.education.id).exists())

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        initial_count = Education.objects.count()

        response = self.client.patch(
            self.detail_url,
            {"institution": "Updated University"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "Updated University")

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), initial_count)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Education.objects.filter(id=self.education.id).exists())

    def test_owner_can_create_education(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Education.objects.filter(
                institution="University of Indonesia"
            ).exists()
        )

    def test_owner_can_delete_education(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Education.objects.filter(id=self.education.id).exists()
        )

    def test_education_validation_strips_html_and_rejects_empty_institution(self):
        self.client.force_authenticate(user=self.owner)

        payload = self.payload.copy()
        payload["institution"] = "<b></b>"

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("institution", response.data)

        payload["institution"] = "<b>Universitas Indonesia</b>"

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["institution"],
            "Universitas Indonesia",
        )

    def test_guest_cannot_star_education(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_authenticated_user_can_toggle_star(self):
        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.education.starred_by.filter(id=self.visitor.id).exists()
        )
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            self.education.starred_by.filter(id=self.visitor.id).exists()
        )
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_computed_star_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {
                "star_count": 999,
                "is_starred": True,
                "starred_by_names": "fake-user",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    def test_csrf_missing_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(
            username="owner_education",
            password="password123",
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)