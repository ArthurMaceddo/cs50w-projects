from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# Auth
def dashboard(request):
    return HttpResponse("Dashboard placeholder")

def register(request):
    return HttpResponse("Register placeholder")

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