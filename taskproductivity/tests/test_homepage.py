from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase

from selenium import webdriver

class ViewTestCase(ViewBaseCase):
    def test_index(self):
        """Check the index page."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

# Using object because the child classes will be using mixins so that I don't need to write complicated test commands.
class UITestCase(UIBaseCase):
    def test_homepage(self):
        """Check that all of the important elements exist and have the correct name"""
        url = self.live_server_url
        self.web_driver.get(url)

        # Get all the buttons
        btn_login = self.web_driver.find_elements_by_name("btn_login")
        btn_signup = self.web_driver.find_elements_by_name("btn_signup")
        featured_btn_login = self.web_driver.find_elements_by_name("featured_btn_login")
        featured_btn_signup = self.web_driver.find_elements_by_name("featured_btn_signup")

        # Check the number of buttons are correct. 
        self.assertEqual(len(btn_login), 1)
        self.assertEqual(len(btn_signup), 1)
        self.assertEqual(len(featured_btn_login), 1)
        self.assertEqual(len(featured_btn_signup), 1)

        # Check the texts on the home page button is correct. 
        self.assertEqual(btn_login[0].get_attribute('text'), "Log In")
        self.assertEqual(btn_signup[0].get_attribute('text'), "Sign Up")
        self.assertEqual(featured_btn_login[0].get_attribute('text'), "Already have an account? Login")
        self.assertEqual(featured_btn_signup[0].get_attribute('text'), "Sign up for free")

class UITestCaseChrome(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        # Set Chrome to run headless so that it can work in automated tests  of github actions
        options = webdriver.ChromeOptions()
        options.headless = True
        self.web_driver = webdriver.Chrome(options=options)

        # For the rest of the test methods, please refer to UITestCase

class UITestCaseFirefox(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        # Set Firefox to run headless so that it can work in automated tests
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.web_driver = webdriver.Firefox(options=options)

        # For the rest of the test methods, please refer to UITestCase

# Commented out because Windows runners don't support container operations. 
'''class UITestCaseEdge(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("headless")
        self.web_driver = Edge(options=options)'''