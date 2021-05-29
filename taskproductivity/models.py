from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=256)
    description = models.TextField()
    priority = models.PositiveSmallIntegerField()
    completed = models.BooleanField()
    expected_time = models.PositiveIntegerField()
    time_used = models.PositiveIntegerField()
    deadline = models.DateTimeField()
    finish_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    edit_date = models.DateTimeField()

class Sessions(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="sessions")
    total_time = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()