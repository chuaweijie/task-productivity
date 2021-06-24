from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    verified_account = models.BooleanField(default=False)

class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    expected_time = models.PositiveIntegerField()
    time_used = models.PositiveIntegerField(null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

class Sessions(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="sessions")
    total_time = models.PositiveIntegerField(null=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)

class Recoveries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recovery")
    key = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

class Verifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification")
    key = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)