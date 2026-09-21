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
    json_response = get_experience_json(request)

    experience_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [experience.object for experience in experience_data]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Aisyah Zayyana Hanifah",
        "experience_list": experience_list,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def show_education(request):
    json_response = get_education_json(request)

    education_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [education.object for education in education_data]

    institution_query = request.GET.get("institution", "").strip()

    context = {
        "name": "Aisyah Zayyana Hanifah",
        "education_list": education_list,
        "institution_query": institution_query,
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

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience_list = Experience.objects.all()

    if title_query:
        experience_list = experience_list.filter(
            title__icontains=title_query
        )

    experience_json = serializers.serialize("json", experience_list)
    return HttpResponse(experience_json, content_type="application/json")

def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()
    education_list = Education.objects.all()

    if institution_query:
        education_list = education_list.filter(
            institution__icontains=institution_query
        )

    education_json = serializers.serialize("json", education_list)
    return HttpResponse(education_json, content_type="application/json")


def update_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Education updated successfully!")
            return redirect("main:show_education")

    context = {
        "name": "Aisyah Zayyana Hanifah",
        "form": form,
        "education": education,
    }
    return render(request, "education_form.html", context)

def delete_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education deleted successfully!")
        return redirect("main:show_education")

    return redirect("main:show_education")