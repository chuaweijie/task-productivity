from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase

from selenium import webdriver

class ViewTestCase(ViewBaseCase):    
    def test_login_page(self):
        """Check the login page."""
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

class UITestCase(UIBaseCase):
    def setUp(self):
        super().setUp()

    # Write the test for both browsers here.
    def test_invalid_username_login(self):
        '''Testing the login when that doesn't exists.'''
        self._login("user", "12345678")
        
    
    def test_invalid_password_login(self):
        '''Testing the login when that doesn't exists.'''
        self._login("test_user", "87654321")
    
    def test_alid_login(self):
        '''Testing the login when that doesn't exists.'''
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