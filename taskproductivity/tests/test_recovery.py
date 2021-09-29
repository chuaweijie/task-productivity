from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase
from taskproductivity.models import  Recoveries, User

from selenium import webdriver

class ViewTestCase(ViewBaseCase):    
    def setUp(self):
        super().setUp()
        self._setup_default_user()
        
        # Setup the recovery with the correct flow to test the recovery flow
        self.email = 'test@test.com'
        data = {
            'email': self.email,
            'mode': "trigger"
        }
        self._csrf_post("/recovery", data)
        self.user = User.objects.get(email=self.email)
        print(self.user.recovery)
        self.recovery_key = self.user.recovery.key

    def test_recovery_page(self):
        """Check the recovery page."""
        response = self.client.get("/recovery")
        self.assertEqual(response.status_code, 200)
    
    def test_change_pass_wo_key(self):
        """Test without recovery key"""
        response = self.client.get("/recovery_key")
        self.assertEqual(response.status_code, 401)
        
        # Check for the correct error message. 
        self.assertEqual(response.context[0].get("message"), "Invalid recovery key")
        # Check for the correct error styling
        self.assertEqual(response.context[0].get("type"), "danger")
    
    def test_fake_key(self):
        """Trying to reach the change password page with a fake key"""
        response = self.client.get("/recovery_key/12345678971234")
        self.assertEqual(response.status_code, 401)
        
        # Check for the correct error message. 
        self.assertEqual(response.context[0].get("message"), "Invalid recovery key")
        # Check for the correct error styling
        self.assertEqual(response.context[0].get("type"), "danger")
    
    def test_correct_key_change_password(self):
        """Try reaching with correct key and change password"""
        response = self.client.get("/recovery_key/"+self.recovery_key)
        self.assertEqual(response.status_code, 200)
        old_password = self.user.password
        recovery = Recoveries.objects.get(key=self.recovery_key)
        data = {
            'password': '4321',
            'confirmation': '4321',
            'mode': "reset"
        }
        self._csrf_post("/recovery", data)
        self.assertFalse(recovery.active)
        self.assertNotEqual(old_password,self.user.password)

    def test_recovery_page_with_wrong_email(self):
        """Check the recovery page when a wrong email is provided"""
        recoveries_before = Recoveries.objects.all()
        data = {
            'email': 'wrong@wrong.com',
            'mode': "trigger"
        }
        response = self._csrf_post("/recovery", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get("message"), "We sent an email to wrong@wrong.com with instructions to reset your password. If you do not receive a password reset message after 1 minute, verify that you entered the correct email address, or check your spam folder.")
        self.assertEqual(response.context[0].get("type"), "success")
        recoveries_after = Recoveries.objects.all()
        self.assertEqual(recoveries_before.count(), recoveries_after.count())
    
    def test_recovery_page_with_correct_email(self):
        """Check the recovery page when a wrong email is provided"""
        self.user = User.objects.get(email=self.email)
        recoveries_count_before = self.user.recovery.get(active=True).count()
        data = {
            'email': self.email,
            'mode': "trigger"
        }
        response = self._csrf_post("/recovery", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get("message"), "We sent an email to test@test.com with instructions to reset your password. If you do not receive a password reset message after 1 minute, verify that you entered the correct email address, or check your spam folder.")
        self.assertEqual(response.context[0].get("type"), "success")
        recoveries_count_after = Recoveries.objects.get(user=self.user, active=True).count()
        self.assertEqual(recoveries_count_before, recoveries_count_after)


class UITestCase(UIBaseCase):
    def setUp(self):
        super().setUp()

    # Write the test for both browsers here.
    def test_invalid_username_login(self):
        '''Testing the login when that doesn't exists.'''
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