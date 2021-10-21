from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .utils import convert_to_timestamp

class User(AbstractUser):
    email = models.CharField(max_length=256, unique=True)
    verified_account = models.BooleanField(default=False)

class ERDates(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    entry = models.DateField(null=True)
    renewal = models.DateField(null=True)
    active = models.BooleanField(default=True)
    departure = models.DateField(null=True)
    online_start = models.DateField(null=True)
    online_end = models.DateField(null=True)
    reported_date = models.DateField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def serialize(self):
        entry, renewal, online_start, online_end, departure, reported_date = convert_to_timestamp(self.entry, self.renewal, self.online_start, self.online_end, self.departure, self.reported_date)
        return {
            "id": self.id,
            "entry": entry,
            "renewal": renewal,
            "online_start": online_start,
            "online_end": online_end,
            "departure": departure,
            "reported_date": reported_date
        }
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