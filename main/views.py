from django.shortcuts import render

from main.models import Experience, Education


def show_main(request):
    context = {
        "name": "Aisyah Zayyana Hanifah",
        "npm": "2506609132",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "A 2nd-year Information Systems student who’s still figuring out what comes next."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Aisyah Zayyana Hanifah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Aisyah Zayyana Hanifah",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)