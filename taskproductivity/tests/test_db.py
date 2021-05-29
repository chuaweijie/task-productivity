from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from taskproductivity.models import User, Tasks, Sessions

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create 2 users
        u1 = User.objects.create(password="4321", is_superuser=False, username="user1", first_name="user", last_name="1", email="user1@test.com", is_staff=False, is_active=True, date_joined=timezone.now())
        u2 = User.objects.create(password="4321", is_superuser=False, username="user2", first_name="user", last_name="2", email="user2@test.com", is_staff=False, is_active=True, date_joined=timezone.now())

        # Create 2 tasks for user 1
        # With all fields
        u1t1 = Tasks.objects.create(user=u1, title="Test Task 1", description="This is the description of test task 1.", priority="0", expected_time="5", time_used="5")
        u1t2 = Tasks.objects.create(user=u1, title="Test Task 2", expected_time="5")

        # create a session to reflect the used time in task 1. 
        t1s1 = Sessions.objects.create(task=u1t1, total_time = "5", end = u1t1.creation_date + timedelta(minutes=5))

    def test_user_count(self):
        """Check the count of users"""
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_task_count(self):
        """Check the count of tasks"""
        tasks = Tasks.objects.all()
        self.assertEqual(tasks.count(), 2)