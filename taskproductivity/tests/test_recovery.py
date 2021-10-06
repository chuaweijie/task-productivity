import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from .base_case import ViewBaseCase, UIBaseCase
from taskproductivity.models import  Recoveries, User

from datetime import timedelta

from selenium import webdriver

class ViewTestCase(ViewBaseCase):    
    def setUp(self):
        super().setUp()
        self._setup_default_user()
        
        # Setup the recovery with the correct flow to test the recovery flow. To change the email, please go to base_case.py
        data = {'email': self.email,}
        self.user = User.objects.get(email=self.email)
        self.recovery_key = "12345678"
        earlier_time = timezone.now() - timedelta(minutes=15)
        Recoveries.objects.create(user=self.user, key=self.recovery_key, time=earlier_time)
        # Manually create the key to skip repeated email request. Email request will be tested in test_recovery_page_with_correct_email and test_recovery_page_with_wrong_email

    def test_recovery_page(self):
        """Check the recovery page."""
        response = self.client.get("/recovery")
        self.assertEqual(response.status_code, 200)
    
    def test_change_pass_wo_key(self):
        """Test without recovery key"""
        response = self.client.get("/reset_password")
        self.assertEqual(response.status_code, 401)
        
        # Check for the correct error message. 
        self.assertEqual(response.context[0].get("message"), "Invalid recovery key")
        # Check for the correct error styling
        self.assertEqual(response.context[0].get("type"), "danger")
    
    def test_fake_key(self):
        """Trying to reach the change password page with a fake key"""
        response = self.client.get("/reset_password/12345678971234")
        self.assertEqual(response.status_code, 401)
        
        # Check for the correct error message. 
        self.assertEqual(response.context[0].get("message"), "Invalid recovery key")
        # Check for the correct error styling
        self.assertEqual(response.context[0].get("type"), "danger")
    
    #
    #Add a test when different passwords are entered. Write this later.
    #
    def test_correct_key_incorrect_password(self):
        """Try to reach change password page with correct key and incorrect password"""
        response = self.client.get("/reset_password/"+self.recovery_key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get("key"), self.recovery_key)
        old_password = self.user.password
        data = {
            'password': '4321',
            'confirmation': '1234',
            'key': self.recovery_key
        }
        response = self._csrf_post("/reset_password", data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.context[0].get("message"), "Passwords don't match. Please make sure they are the same and try again.")
        self.assertEqual(response.context[0].get("type"), "warning")
        self.assertEqual(response.context[0].get("key"), self.recovery_key)

        recovery = Recoveries.objects.filter(key=self.recovery_key)
        self.assertTrue(recovery[0].active)
        new_password = User.objects.get(email=self.email).password
        self.assertEqual(old_password, new_password)

    def test_correct_key_correct_password(self):
        """Try to reach change password page with correct key and correct password"""
        response = self.client.get("/reset_password/"+self.recovery_key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get("key"), self.recovery_key)
        old_password = self.user.password
        data = {
            'password': '4321',
            'confirmation': '4321',
            'key': self.recovery_key
        }
        self._csrf_post("/reset_password", data)
        recovery = Recoveries.objects.get(key=self.recovery_key)
        self.assertFalse(recovery.active)
        new_password = User.objects.get(email=self.email).password
        self.assertNotEqual(old_password, new_password)

    def test_recovery_page_with_wrong_email(self):
        """Check the recovery page when a wrong email is provided"""
        recoveries_before = Recoveries.objects.all()
        data = {'email': 'wrong@wrong.com'}
        response = self._csrf_post("/recovery", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get("message"), "We've sent an email to wrong@wrong.com with instructions to reset your password. If you do not receive a password reset message after 1 minute, verify that you entered the correct email address, or check your spam folder.")
        self.assertEqual(response.context[0].get("type"), "success")
        recoveries_after = Recoveries.objects.all()
        self.assertEqual(recoveries_before.count(), recoveries_after.count())
    
    def test_recovery_page_with_correct_email(self):
        """Check the recovery page when a correct email is provided"""
        recoveries_count_before = Recoveries.objects.filter(user=self.user).count()
        data = {'email': self.email}
        response = self._csrf_post("/recovery", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get("message"), "We've sent an email to " + self.email +" with instructions to reset your password. If you do not receive a password reset message after 1 minute, verify that you entered the correct email address, or check your spam folder.")
        self.assertEqual(response.context[0].get("type"), "success")
        recoveries_count_after = Recoveries.objects.filter(user=self.user).count()
        self.assertNotEqual(recoveries_count_before, recoveries_count_after)


class UITestCase(UIBaseCase):
    def setUp(self):
        super().setUp()

    # Tests to write
    # 1. Test requesting recovery with an existing email
    # 2. Test requesting recovery with an invalid email
    # 3. Test reseting password without any key
    # 4. Test reseting password with incorrect key
    # 5. Test reseting password with expired key
    # 6. Test reseting password with correct key but with incorrect confirmation password and then with the correct confirmation password
    # 7. Test reseting password with correct key and with correct confirmation password

    # Write the test for both browsers here.
    def test_recovery_page(self):
        '''Test the elements in the recovery page. The page where users go and get their password reset.'''
        self._login("user", "12345678")
    
    def test_reset_page(self):
        '''Test the elements in the reset page. The page where users go and reset their password once they have the link'''
        self._login("user", "12345678")
        

class UITestCaseChrome(UITestCase, StaticLiveServerTestCase):
     def setUp(self):
        # Set Chrome to run headless so that it can work in automated tests of github actions
        super().setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.web_driver = webdriver.Chrome(options=options)
        self._signup_user("test_user", "test_user@test.com", "12345678", "12345678")
        # For the rest of the test methods, please refer to UITestCase

class UITestCaseFirefox(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        # Set Firefox to run headless so that it can work in automated tests
        super().setUp()
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.web_driver = webdriver.Firefox(options=options)
        self._signup_user("test_user", "test_user@test.com", "12345678", "12345678")

        # For the rest of the test methods, please refer to UITestCase