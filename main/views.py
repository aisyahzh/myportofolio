import datetime

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied       

from main.models import Experience, Education
from main.forms import ExperienceForm, EducationForm

NAME = "Aisyah Zayyana Hanifah"

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": NAME,
        "npm": "2506609132",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "A 2nd-year Information Systems student who’s still figuring out what comes next."
        ),
        "last_login": last_login,

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
        "name": NAME,
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
        "name": NAME,
        "education_list": education_list,
        "institution_query": institution_query,
    }
    return render(request, "education.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    # Cek apakah akun yang sedang login adalah superuser (admin/kamu);
    # kalau bukan, hentikan permintaannya dengan 403.
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ExperienceForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Experience added successfully!")
            return redirect("main:show_experience")

    context = {
        "name": NAME,
        "form": form,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = EducationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Education added successfully!")
            return redirect("main:show_education")

    context = {
        "name": NAME,
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
    education_list = Education.objects.all()

    education_json = serializers.serialize(
        "json",
        education_list,
        use_natural_foreign_keys=True,
    )

    return HttpResponse(education_json, content_type="application/json")

@login_required(login_url="/login/")
def update_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    education = get_object_or_404(Education, id=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Education updated successfully!")
            return redirect("main:show_education")

    context = {
        "name": NAME,
        "form": form,
        "education": education,
    }
    return render(request, "education_form.html", context)

@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    education = get_object_or_404(Education, id=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education deleted successfully!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": NAME,
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": NAME,
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)

    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)

    return redirect("main:show_education")