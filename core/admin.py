from django.contrib import admin
from .models import Subject, Topic, Flashcard, FlashcardReview, PomodoroSession, WeeklyGoal

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display  = ["name", "user", "color", "progress", "created_at"]
    list_filter   = ["user"]
    search_fields = ["name", "user__username"]

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display  = ["name", "subject", "is_completed", "order"]
    list_filter   = ["is_completed", "subject__user"]
    search_fields = ["name", "subject__name"]

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display  = ["front", "subject", "next_review_date", "interval_days", "is_due_today"]
    list_filter   = ["subject__user", "subject"]
    search_fields = ["front", "back"]

@admin.register(FlashcardReview)
class FlashcardReviewAdmin(admin.ModelAdmin):
    list_display = ["flashcard", "rating", "reviewed_at"]
    list_filter  = ["rating"]

@admin.register(PomodoroSession)
class PomodoroSessionAdmin(admin.ModelAdmin):
    list_display = ["subject", "user", "duration_minutes", "completed", "started_at"]
    list_filter  = ["completed", "user"]

@admin.register(WeeklyGoal)
class WeeklyGoalAdmin(admin.ModelAdmin):
    list_display = ["subject", "user", "target_hours", "week_start", "current_hours", "percentage"]
    list_filter  = ["user"]