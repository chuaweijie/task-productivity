from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from datetime import timedelta

from taskproductivity.models import ERDates, User, Recoveries
from taskproductivity.utils import send_email


class Command(BaseCommand):
    help = "Checkes for users who are approaching or at their online reporting date or visa renewal deadline."

    def handle(self, *args, **options):
        # Only get the active ERDates of active users
        er_dates = ERDates.objects.filter(active=True).select_related('user').filter(user__is_active=True)

        # Send email if users are due for renewal
        for er_date in er_dates:
            email_data = {
                "sender": "noreply@weijie.info",
                "sender_name": "90 Days Reporting Tracker",
                "to": er_date.user.email,
                "to_name": er_date.user.first_name + " " + er_date.user.last_name,
                "subject": "90 Days Reporting Tracker - Online Notification of Staying in the Kingdom Reminder",
                "day_num": "7 days",
            }
             
            if timezone.now().date() - er_date.online_start == timedelta(days=0):
                send_email(email_data, 3930904)
            elif timezone.now().date() - er_date.online_end == timedelta(days=0):
                email_data["day_num"] = "the last day"
                send_email(email_data, 3930904)
            elif timezone.now().date() - er_date.renewal == timedelta(days=-6):
                email_data["subject"] = "90 Days Reporting Tracker - Notification of Staying in the Kingdom Reminder"
                email_data["day_num"] = "6 days"
                send_email(email_data, 3936662)
            elif timezone.now().date() - er_date.renewal == timedelta(days=0):
                email_data["subject"] = "90 Days Reporting Tracker - Notification of Staying in the Kingdom Reminder"
                email_data["day_num"] = "the last day"
                send_email(email_data, 3936662)