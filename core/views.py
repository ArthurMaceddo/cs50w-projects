from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout
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

# Subjects -----------------------------------------------------------------
def subjects_list(request):
    return HttpResponse("Subjects list placeholder")

def subject_create(request):
    return HttpResponse("Create subject placeholder")

def subject_detail(request, pk):
    return HttpResponse(f"Detail of subject {pk} placeholder")

def subject_edit(request, pk):
    return HttpResponse(f"Edit subject {pk} placeholder")

def subject_delete(request, pk):
    return HttpResponse(f"Delete subject {pk} placeholder")

# Topics -------------------------------------------------------------------
def topic_create(request):
    return HttpResponse("Create topic placeholder")

def topic_toggle(request, pk):
    return HttpResponse(f"Toggle topic {pk} placeholder")

def topic_delete(request, pk):
    return HttpResponse(f"Delete topic {pk} placeholder")

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

# Pomodoro --------------------------------------------------------------------
def pomodoro(request):
    return HttpResponse("Pomodoro timer placeholder")

def pomodoro_save(request):
    return HttpResponse("Save pomodoro session placeholder")

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