from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ── Auth ──────────────────────────────────────
    path("", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

     # ── Subject ──────────────────────────────────
    path("subjects/", views.subjects_list, name="subjects_list"),
    path("subjects/new/", views.subject_create, name="subject_create"),
    path("subjects/<int:pk>/", views.subject_detail, name="subject_detail"),
    path("subjects/<int:pk>/edit/", views.subject_edit, name="subject_edit"),
    path("subjects/<int:pk>/delete/", views.subject_delete, name="subject_delete"),

    # ── Topics (API by fetch) ────────────────────
    path("topics/new/", views.topic_create, name="topic_create"),
    path("topics/<int:pk>/toggle/", views.topic_toggle, name="topic_toggle"),
    path("topics/<int:pk>/delete/", views.topic_delete, name="topic_delete"),

    path("flashcards/", views.flashcard_list, name="flashcard_list"),
    path("flashcards/new/", views.flashcard_create, name="flashcard_create"),
    path("flashcards/review/", views.flashcard_review_session, name="flashcard_review"),
    path("flashcards/<int:pk>/delete/", views.flashcard_delete, name="flashcard_delete"),
    path("flashcards/<int:pk>/submit/", views.flashcard_submit_review, name="flashcard_submit"),

    # ── Pomodoro ─────────────────────────────────
    path("pomodoro/", views.pomodoro, name="pomodoro"),
    path("pomodoro/save/", views.pomodoro_save, name="pomodoro_save"),
]