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