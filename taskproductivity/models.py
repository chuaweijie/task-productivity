from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.CharField(max_length=256, unique=True)
    verified_account = models.BooleanField(default=False)

class ERDates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    entry = models.DateField(null=True)
    renewal = models.DateField(null=True)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

# Table unused. Will be utilized for future implementation
class Recoveries(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recovery")
    key = models.CharField(max_length=128)
    time = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

# Table unused. Will be utilized for future implementation
class Verifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification")
    key = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)