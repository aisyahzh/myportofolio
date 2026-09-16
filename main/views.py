from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Education
from main.forms import ExperienceForm, EducationForm

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

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Experience added successfully!")
            return redirect("main:show_experience")

    context = {
        "name": "Aisyah Zayyana Hanifah",
        "form": form,
    }
    return render(request, "experience_form.html", context)


def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Education added successfully!")
            return redirect("main:show_education")

    context = {
        "name": "Aisyah Zayyana Hanifah",
        "form": form,
    }
    return render(request, "education_form.html", context)