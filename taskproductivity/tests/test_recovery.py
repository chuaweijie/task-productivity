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
        self.assertEqual(response.context[0].get("message"), "Invalid recovery key. Recovery key is probably older than 1 hour. Please request for the password reset and try again")
        # Check for the correct error styling
        self.assertEqual(response.context[0].get("type"), "danger")
    
    def test_fake_key(self):
        """Trying to reach the change password page with a fake key"""
        response = self.client.get("/reset_password/12345678971234")
        self.assertEqual(response.status_code, 401)
        
        # Check for the correct error message. 
        self.assertEqual(response.context[0].get("message"), "Invalid recovery key. Recovery key is probably older than 1 hour. Please request for the password reset and try again")
        # Check for the correct error styling
        self.assertEqual(response.context[0].get("type"), "danger")
    
    def test_expired_key(self):
        """Testing the condition when the key used is old."""
        recovery = Recoveries.objects.filter(key=self.recovery_key)
        earlier_time = timezone.now() - timedelta(hours=2)
        recovery.update(time=earlier_time)
        response = self.client.get("/reset_password/"+self.recovery_key)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.context[0].get("message"), "Invalid recovery key. Recovery key is probably older than 1 hour. Please request for the password reset and try again")
        self.assertEqual(response.context[0].get("type"), "danger")
        recovery = Recoveries.objects.filter(key=self.recovery_key, active=True)
        self.assertEqual(recovery.count(), 0)
    
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
        self.username = "test_user"
        self.email = "test_user@test.com"
        self.password = "12345678"
    # Tests to write
    # 1. Test requesting recovery with an existing email [Done]
    # 2. Test requesting recovery with an invalid email [Done]
    # 3. Test reseting password without any key [Done]
    # 4. Test reseting password with incorrect key
    # 5. Test reseting password with expired key
    # 6. Test reseting password with correct key but with incorrect confirmation password and then with the correct confirmation password
    # 7. Test reseting password with correct key and with correct confirmation password

    # Write the test for both browsers here.
    def test_recovery_page(self):
        '''Check if all the needed elements in the recovery page exists or not.'''
        self.web_driver.get('%s%s' % (self.live_server_url, '/recovery'))
        input_email = self.web_driver.find_elements_by_name("input_email")
        self.assertEqual(len(input_email), 1)
        self.assertEqual(input_email[0].get_attribute("placeholder"), "Email")
        btn_submit = self.web_driver.find_elements_by_name("btn_submit")
        self.assertEqual(len(btn_submit), 1)
        self.assertEqual(btn_submit[0].text, "Submit")
    
    def test_recovery_page_wrong_email(self):
        '''Check if the browser shows the correct message when an incorrect email is provided.'''
        email = "wrong@wrong.com"
        self.web_driver.get('%s%s' % (self.live_server_url, '/recovery'))
        self.web_driver.find_element_by_id("input_email").send_keys(email)
        self.web_driver.find_element_by_id("btn_submit").click()
        alert = self.web_driver.find_element_by_id("alert")
        self.assertEqual(alert.get_attribute("class"), "alert alert-success")
        self.assertEqual(alert.text, "We've sent an email to " + email +" with instructions to reset your password. If you do not receive a password reset message after 1 minute, verify that you entered the correct email address, or check your spam folder.")

    def test_recovery_page_correct_email(self):
        '''Check if the browser shows the correct message when a correct email is provided.'''
        self.web_driver.get('%s%s' % (self.live_server_url, '/recovery'))
        self.web_driver.find_element_by_id("input_email").send_keys(self.email)
        self.web_driver.find_element_by_id("btn_submit").click()
        alert = self.web_driver.find_element_by_id("alert")
        self.assertEqual(alert.get_attribute("class"), "alert alert-success")
        self.assertEqual(alert.text, "We've sent an email to " + self.email +" with instructions to reset your password. If you do not receive a password reset message after 1 minute, verify that you entered the correct email address, or check your spam folder.")

    def test_reset_page_without_key(self):
        '''Check if the browser will redirect and display the correct error message if someone access the rest_pasword page without key'''
        self.web_driver.get('%s%s' % (self.live_server_url, '/reset_password'))
        alert = self.web_driver.find_element_by_id("alert")
        self.assertEqual(alert.get_attribute("class"), "alert alert-danger")
        self.assertEqual(alert.text, "Invalid recovery key. Recovery key is probably older than 1 hour. Please request for the password reset and try again")

    def test_rest_page_incorrect_key(self):
        # Continue writing this during lunch time.
        self.web_driver.get('%s%s' % (self.live_server_url, '/reset_password/incorrect'))

class UITestCaseChrome(UITestCase, StaticLiveServerTestCase):
     def setUp(self):
        # Set Chrome to run headless so that it can work in automated tests of github actions
        super().setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.web_driver = webdriver.Chrome(options=options)
        self._signup_user(self.username, self.email, self.password, self.password)
        # For the rest of the test methods, please refer to UITestCase

class UITestCaseFirefox(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        # Set Firefox to run headless so that it can work in automated tests
        super().setUp()
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.web_driver = webdriver.Firefox(options=options)
        self._signup_user(self.username, self.email, self.password, self.password)

        # For the rest of the test methods, please refer to UITestCase