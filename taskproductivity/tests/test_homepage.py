from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

class HomepageTestCase(TestCase):

    def settings(self):
        self.client = Client(enforce_csrf_checks=True)
    
    def test_index(self):
        """Check the index page."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

class UITestCase(object):
    def setUp(self):
        self.web_driver = None
    
    def test_homepage(self):
        url = self.live_server_url
        self.web_driver.get(url)

        btn_login = self.web_driver.find_elements_by_name("btn_login")
        btn_signup = self.web_driver.find_elements_by_name("btn_signup")
        featured_btn_login = self.web_driver.find_elements_by_name("featured_btn_login")
        featured_btn_signup = self.web_driver.find_elements_by_name("featured_btn_signup")

        self.assertEqual(len(btn_login), 1)
        self.assertEqual(len(btn_signup), 1)
        self.assertEqual(len(featured_btn_login), 1)
        self.assertEqual(len(featured_btn_signup), 1)
        self.assertEqual(btn_login[0].get_attribute('text'), "Log In")
        self.assertEqual(btn_signup[0].get_attribute('text'), "Sign Up")
        self.assertEqual(featured_btn_login[0].get_attribute('text'), "Already have an account? Login")
        self.assertEqual(featured_btn_signup[0].get_attribute('text'), "Sign up for free")
    
    def tearDown(self):
        self.web_driver.quit()

class UITestCaseChrome(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True

        # Set Chrome to run headless so that it can work in automated tests
        self.web_driver = webdriver.Chrome(options=options)

class UITestCaseEdge(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("headless")
        self.web_driver = Edge(options=options)

class UITestCaseFirefox(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.web_driver = webdriver.Firefox(options=options)