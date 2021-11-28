from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase

from selenium import webdriver

class ViewTestCase(ViewBaseCase):    
    def setUp(self):
        super().setUp()
        self._setup_default_user()

    def test_login_page(self):
        """Check the login page."""
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
    
    def test_login_page_incorrect_username(self):
        """Check the post request to login page with the wrong username"""
        # Trying to enter the wrong username
        data = {
            'username': 'wrong', 
            'password':'1234', 
        }
        response = self._csrf_post("/login", data)
        self.assertEqual(response.status_code, 401)
        
        # Check for the correct error message. 
        self.assertEqual(response.context[0].get("message"), "Invalid username and/or password.")
        # Check for the correct error styling
        self.assertEqual(response.context[0].get("type"), "danger")
    
    def test_login_page_incorrect_password(self):
        """Check the post request to login page with the wrong password"""
        # Trying to enter the wrong username
        data = {
            'username': 'test', 
            'password':'4321', 
        }
        response = self._csrf_post("/login", data)
        self.assertEqual(response.status_code, 401)
        
        # Check for the correct error message. 
        self.assertEqual(response.context[0].get("message"), "Invalid username and/or password.")
        # Check for the correct error styling
        self.assertEqual(response.context[0].get("type"), "danger")
    
    def test_login_page_correct_username_and_password(self):
        """Check the post request to login page with the correct username and password"""
        # Trying to enter the wrong username
        data = {
            'username': 'test', 
            'password':'1234', 
        }
        response = self._csrf_post("/login", data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/main")


class UITestCase(UIBaseCase):
    def setUp(self):
        super().setUp()

    # Write the test for both browsers here.
    def test_invalid_username_login(self):
        '''Testing the login with a user that doesn't exists.'''
        self._login("user", "12345678")
        
    def test_invalid_password_login(self):
        '''Testing the login with a wrong password'''
        self._login("test_user", "87654321")
    
    def test_valid_login(self):
        '''Testing the login with correct credential'''
        self._login("test_user", "12345678")

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