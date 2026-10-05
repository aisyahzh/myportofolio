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
from django.http import JsonResponse   
from django.views.decorators.http import require_POST

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
    title_query = request.GET.get("title", "").strip()

    is_editor = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Editor").exists()
    )

    context = {
        "name": NAME,
        "title_query": title_query,
        "is_editor": is_editor,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    institution_query = request.GET.get("institution", "").strip()

    is_editor = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Editor").exists()
    )

    context = {
        "name": NAME,
        "institution_query": institution_query,
        "is_editor": is_editor,
        "form": EducationForm(),
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
    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []

    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )
        starred_by_names = ", ".join(
            [user.username for user in starred_users]
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "role": experience.role,
                "description": experience.description,
                "category": experience.category,
                "thumbnail": experience.thumbnail,
                "started_at": experience.started_at.isoformat(),
                "ended_at": (
                    experience.ended_at.isoformat()
                    if experience.ended_at
                    else None
                ),
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()
    educations = Education.objects.prefetch_related("starred_by").all()

    if institution_query:
        educations = educations.filter(
            institution__icontains=institution_query
        )

    data = []

    for education in educations:
        starred_users = education.starred_by.all()
        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )
        starred_by_names = ", ".join(
            [user.username for user in starred_users]
        )

        data.append({
            "pk": str(education.id),
            "fields": {
                "institution": education.institution,
                "degree": education.degree,
                "description": education.description,
                "thumbnail": education.thumbnail,
                "started_at": education.started_at.isoformat(),
                "ended_at": (
                    education.ended_at.isoformat()
                    if education.ended_at
                    else None
                ),
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied

    experience = get_object_or_404(Experience, id=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Experience updated successfully!")
            return redirect("main:show_experience")

    context = {
        "name": NAME,
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def update_education(request, education_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not (request.user.is_superuser or is_editor):
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
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, id=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience deleted successfully!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

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
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def toggle_star_education(request, education_id):
    education = get_object_or_404(Education, id=education_id)

    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)

    return redirect("main:show_education")

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)

    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )

@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan education."},
            status=403,
        )

    form = EducationForm(request.POST)

    if form.is_valid():
        education = form.save()
        return JsonResponse(
            {"message": "Education berhasil ditambahkan.", "pk": str(education.id)},
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )