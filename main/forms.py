from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput

from main.models import Education, Experience

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "role",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Title",
            "role": "Role",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail URL",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Enter the experience title",
                }
            ),
            "role": TextInput(
                attrs={
                    "placeholder": "Enter your role",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your experience",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "Enter a thumbnail URL",
                }
            ),
            "started_at": DateTimeInput(
                attrs={
                    "type": "date",
                    "placeholder": "Enter the start date",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "date",
                    "placeholder": "Enter the end date",
                }
            ),
        }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "description",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "institution": "Institution",
            "degree": "Degree",
            "description": "Description",
            "thumbnail": "Thumbnail URL",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Enter your institution",
                }
            ),
            "degree": TextInput(
                attrs={
                    "placeholder": "Enter your degree",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your education",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "Enter a thumbnail URL",
                }
            ),
            "started_at": DateTimeInput(
                attrs={
                    "type": "date",
                    "placeholder": "Enter the start date",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "date",
                    "placeholder": "Enter the end date",
                }
            ),
        }
