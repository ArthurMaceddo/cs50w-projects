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
