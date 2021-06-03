from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver

class HomepageTestCase(TestCase):

    def settings(self):
        self.client = Client(enforce_csrf_checks=True)
    
    def test_index(self):
        """Check the index page."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

class UITestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.web_driver = None

class UITestCaseChrome(UITestCase):
    def setUp(self):
        self.web_driver = webdriver.Chrome()
    
    def test_homepage(self):
        url = self.live_server_url
        self.web_driver.get(url)

        btn_login = self.web_driver.find_elements_by_name("btn_login")
        btn_signup = self.web_driver.find_elements_by_name("btn_signup")

        self.assertEqual(len(btn_login), 1)
        self.assertEqual(len(btn_signup), 1)
        self.assertEqual(btn_login.text, "Log In")
        self.assertEqual(btn_signup.text, "Sign up for free")

class UITestCaseEdge(UITestCase):
    def setUp(self):
        self.web_driver = webdriver.Edge()

class UITestCaseFirefox(UITestCase):
    def setUp(self):
        self.web_driver = webdriver.Firefox()

class UITestCaseSafari(UITestCase):
    def setUp(self):
        self.web_driver = webdriver.Safari()