from datetime import datetime
import json

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout

from core.models import PomodoroSession, Subject, Topic
# Create your views here.
# Auth
def dashboard(request):
    return HttpResponse("Dashboard placeholder")

# AUTH
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to Study Manager.")
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# ─────────────────────────────────────────
# SUBJECTS
# ─────────────────────────────────────────

def subjects_list(request):
    subjects = Subject.objects.filter(user=request.user)
    return render(request, "subjects/list.html", {"subjects": subjects})

def subject_create(request):
    if request.method == "POST":
        name  = request.POST.get("name", "").strip()
        desc  = request.POST.get("description", "").strip()
        color = request.POST.get("color", "#5b88a5")
        if name:
            Subject.objects.create(user=request.user, name=name, description=desc, color=color)
            messages.success(request, f'Subject "{name}" created!')
            return redirect("subjects_list")
    return render(request, "subjects/form.html", {"action": "Create"})


def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    topics  = subject.topics.all()
    return render(request, "subjects/detail.html", {"subject": subject, "topics": topics})

def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == "POST":
        subject.name        = request.POST.get("name", subject.name).strip()
        subject.description = request.POST.get("description", "").strip()
        subject.color       = request.POST.get("color", subject.color)
        subject.save()
        messages.success(request, "Subject updated!")
        return redirect("subject_detail", pk=pk)
    return render(request, "subjects/form.html", {"action": "Edit", "subject": subject})


def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject deleted.")
        return redirect("subjects_list")
    return render(request, "subjects/confirm_delete.html", {"subject": subject})

# Topics -------------------------------------------------------------------
# ─────────────────────────────────────────
# TÓPICOS
# ─────────────────────────────────────────

@require_POST
def topic_create(request):
    subject_id = request.POST.get("subject_id")
    name       = request.POST.get("name", "").strip()
    notes      = request.POST.get("notes", "").strip()
    subject    = get_object_or_404(Subject, pk=subject_id, user=request.user)
    if name:
        Topic.objects.create(subject=subject, name=name, notes=notes)
    return redirect("subject_detail", pk=subject_id)


def topic_toggle(request, pk):
    """API: switch is_completed. Return JSON."""
    topic = get_object_or_404(Topic, pk=pk, subject__user=request.user)
    topic.is_completed = not topic.is_completed
    topic.save()
    return JsonResponse({
        "completed": topic.is_completed,
        "progress": topic.subject.progress(),
    })

def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk, subject__user=request.user)
    subject_pk = topic.subject.pk
    topic.delete()
    return JsonResponse({"deleted": True, "progress": Subject.objects.get(pk=subject_pk).progress()})

# Flashcards -----------------------------------------------------------------
def flashcard_list(request):
    return HttpResponse("Flashcards list placeholder")

def flashcard_create(request):
    return HttpResponse("Create flashcard placeholder")

def flashcard_review_session(request):
    return HttpResponse("Review session placeholder")

def flashcard_delete(request, pk):
    return HttpResponse(f"Delete flashcard {pk} placeholder")

def flashcard_submit_review(request, pk):
    return HttpResponse(f"Submit review for flashcard {pk} placeholder")

# ─────────────────────────────────────────
# POMODORO
# ─────────────────────────────────────────

def pomodoro(request):
    subjects = Subject.objects.filter(user=request.user)
    recent   = PomodoroSession.objects.filter(user=request.user, completed=True)[:10]
    return render(request, "pomodoro/timer.html", {"subjects": subjects, "recent": recent})

@require_POST
def pomodoro_save(request):
    """API: salva uma sessão Pomodoro concluída."""
    data       = json.loads(request.body)
    subject    = get_object_or_404(Subject, pk=data.get("subject_id"), user=request.user)
    PomodoroSession.objects.create(
        user=request.user,
        subject=subject,
        started_at=datetime.now(),
        duration_minutes=data.get("duration_minutes", 25),
        completed=True,
    )
    return JsonResponse({"saved": True})

# Goals -----------------------------------------------------------------------
def goals_list(request):
    return HttpResponse("Goals list placeholder")

def goal_create(request):
    return HttpResponse("Create goal placeholder")

def goal_delete(request, pk):
    return HttpResponse(f"Delete goal {pk} placeholder")

# Analytics
def dashboard_activity(request):
    return HttpResponse("Activity dashboard placeholder")