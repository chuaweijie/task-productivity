from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from taskproductivity.models import User, Tasks, Sessions, Verification, Recovery

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create 2 users
        self.user1 = User.objects.create(password="4321", is_superuser=False, username="user1", first_name="user", last_name="1", email="user1@test.com", is_staff=False, is_active=True, date_joined=timezone.now())
        self.user2 = User.objects.create(password="4321", is_superuser=False, username="user2", first_name="user", last_name="2", email="user2@test.com", is_staff=False, is_active=True, date_joined=timezone.now())

        # Create 2 tasks for user 1
        # With all fields
        self.user1_task1 = Tasks.objects.create(user=self.user1, title="Test Task 1", description="This is the description of test task 1.", priority="0", expected_time="5", time_used="5")
        self.user1_task2 = Tasks.objects.create(user=self.user1, title="Test Task 2", expected_time="5")

        # create a session to reflect the used time in task 1. 
        self.task1_session1 = Sessions.objects.create(task=self.user1_task1, total_time = "5", end = self.user1_task1.creation_date + timedelta(minutes=5))


    def test_user_task_count(self):
        """Check the count of users"""
        user = User.objects.get(username="user1")
        self.assertEqual(user.tasks.count(), 2)

        user = User.objects.get(username="user2")
        self.assertEqual(user.tasks.count(), 0)

    def test_task_session_count(self):
        """Check the count of tasks"""
        tasks = Tasks.objects.filter(user=self.user1)

        session_count = 1
        for task in tasks:
            self.assertEqual(task.sessions.count(), session_count)
            session_count -= 1