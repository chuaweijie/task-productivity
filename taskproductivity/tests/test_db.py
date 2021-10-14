from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from taskproductivity.models import User, Verifications, Recoveries, ERDates

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create 2 users
        self.user1 = User.objects.create(password="4321", is_superuser=False, username="user1", first_name="user", last_name="1", email="user1@test.com", is_staff=False, is_active=True, date_joined=timezone.now())
        self.user2 = User.objects.create(password="4321", is_superuser=False, username="user2", first_name="user", last_name="2", email="user2@test.com", is_staff=False, is_active=True, date_joined=timezone.now(), verified_account=True)

        # Create mock verification insert. 
        self.verification = Verifications.objects.create(user=self.user2, key="MockKey")

        # Create a recovery
        self.recovery = Recoveries.objects.create(user=self.user1, key="RecoveryKey")

        # Create ERDate
        self.erdate = ERDates.objects.create(user=self.user1)
    
    def test_erdates_count(self):
        self.assertTrue(self.erdate.active)
        self.assertIsNotNone(self.erdate.creation_date)
        self.assertIsNotNone(self.erdate.edit_date)
        self.assertIsNone(self.erdate.entry)
        self.assertIsNone(self.erdate.renewal)
        self.assertIsNone(self.erdate.depature)
        self.assertIsNone(self.erdate.reported_date)
        self.assertIsNone(self.erdate.online_start)
        self.assertIsNone(self.erdate.online_end)

    def test_recovery_count(self):
        """Check the count of recovery"""
        self.assertEqual(self.user1.recovery.count(), 1)
        self.assertEqual(self.user2.recovery.count(), 0)
    
    def test_verification_count(self):
        """Check the count of recovery"""
        self.assertEqual(self.user1.verification.count(), 0)
        self.assertEqual(self.user2.verification.count(), 1)