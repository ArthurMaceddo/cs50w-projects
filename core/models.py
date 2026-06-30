from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subjects")
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color       = models.CharField(max_length=7, default="#5B88A5") 
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    

    def progress(self):
        """return the % of topics completed in this subject."""
        topics = self.topics.all()
        if not topics.exists():
            return 0
        completed = topics.filter(is_completed=True).count()
        return int((completed / topics.count()) * 100)

    def total_study_minutes(self):
        """total study minutes for this subject based on completed pomodoro sessions."""
        sessions = self.pomodoro_sessions.filter(completed=True)
        return sum(s.duration_minutes for s in sessions)

    class Meta:
        ordering = ["name"]

class Topic(models.Model):
    subject      = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")
    name         = models.CharField(max_length=200)
    notes        = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    order        = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.subject.name}"

    class Meta:
        ordering = ["order", "created_at"]


class PomodoroSession(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pomodoro_sessions")
    subject          = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="pomodoro_sessions")
    started_at       = models.DateTimeField()
    duration_minutes = models.IntegerField(default=25)
    completed        = models.BooleanField(default=False)

    def __str__(self):
        status = "✅" if self.completed else "⏳"
        return f"{status} {self.subject.name} — {self.duration_minutes}min em {self.started_at:%d/%m/%Y}"

    class Meta:
        ordering = ["-started_at"] # descending order by started_at

class Flashcard(models.Model):
    subject          = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="flashcards")
    front            = models.TextField()           # question
    back             = models.TextField()           # answer
    next_review_date = models.DateField(default=date.today)
    interval_days    = models.IntegerField(default=1)   # current interval in days
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card: {self.front[:50]} ({self.subject.name})"

    def is_due_today(self):
        return self.next_review_date <= date.today()

    def apply_review(self, rating):
        """
        Simplified SRS algorithm.
        rating: 'easy' | 'hard' | 'wrong'
        Updates interval_days and next_review_date.
        """
        if rating == "easy":
            self.interval_days = max(self.interval_days * 2, 7)
        elif rating == "hard":
            self.interval_days = max(self.interval_days, 2)
        else:  # wrong
            self.interval_days = 1

        self.next_review_date = date.today() + timedelta(days=self.interval_days)
        self.save()

    class Meta:
        ordering = ["next_review_date"]

class FlashcardReview(models.Model):
    RATING_CHOICES = [
        ("easy",  "Fácil"),
        ("hard",  "Difícil"),
        ("wrong", "Errei"),
    ]
    flashcard   = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name="reviews")
    rating      = models.CharField(max_length=10, choices=RATING_CHOICES)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flashcard} — {self.rating} em {self.reviewed_at:%d/%m/%Y}"

    class Meta:
        ordering = ["-reviewed_at"]