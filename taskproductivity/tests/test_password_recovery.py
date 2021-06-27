from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase

from selenium import webdriver

class ViewTestCase(ViewBaseCase):    
    def test_login_page(self):
        """Check the index page."""
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

class UITestCase(UIBaseCase):
    def setUp(self):
        self.web_driver = None
    
    def test_login(self):
        url = self.live_server_url
        self.web_driver.get(url)
    
    def tearDown(self):
        self.web_driver.quit()