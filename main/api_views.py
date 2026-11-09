from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Experience, Education
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import ExperienceSerializer, EducationSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experience = Experience.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            experience = experience.filter(title__icontains=title)
        serializer = ExperienceSerializer(
            experience, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    serializer = ExperienceSerializer(experience, context={"request": request})
    return Response(serializer.data)

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_list(request):
    if request.method in ("GET", "HEAD"):
        educations = Education.objects.prefetch_related("starred_by").order_by("institution", "id")

        institution_query = request.query_params.get("institution", "").strip()

        if institution_query:
            educations = educations.filter(institution__icontains=institution_query)

        serializer = EducationSerializer(
            educations,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    serializer = EducationSerializer(
        data=request.data,
        context={"request": request},
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    education = get_object_or_404(
        Education.objects.prefetch_related("starred_by"),
        id=education_id,
    )

    if request.method in ("GET", "HEAD"):
        serializer = EducationSerializer(
            education,
            context={"request": request},
        )
        return Response(serializer.data)

    if request.method == "DELETE":
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = EducationSerializer(
        education,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    education = get_object_or_404(
        Education.objects.prefetch_related("starred_by"),
        id=education_id,
    )

    if request.user in education.starred_by.all():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)

    serializer = EducationSerializer(
        education,
        context={"request": request},
    )

    return Response(serializer.data)