import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase

from selenium import webdriver

from datetime import datetime, timedelta

class ViewTestCase(ViewBaseCase): 
    def setUp(self):
        super().setUp()
        self._setup_default_user()


    def test_tracking(self):
        '''Testing all the paths in tacking'''
        data = {
            'username': 'test', 
            'password':'1234', 
        }
        self._csrf_post("/login", data)
        response = self.client.get("/tracking")
        self.assertEqual(response.json(), {"data": None})
        self.assertEqual(response.status_code, 200)

        # Test the case of adding a new tracking where the renewal date is known
        data = {
            "mode": "renewal", 
            "renewal": datetime.fromisoformat('2021-05-04').timestamp()
        }
        response = self._csrf_post("/tracking" ,data)
        online_start = datetime.fromisoformat('2021-05-04') - timedelta(days=14)
        online_end = datetime.fromisoformat('2021-05-04') - timedelta(days=7)
        self.assertEqual(response.json(), { "id": 1,
                                            "entry": None, 
                                            "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                            "online_start": online_start.timestamp(),
                                            "online_end": online_end.timestamp()})
        
        # Test marking as reported




# In order to speed up the completion of the project, I am going to omit all the tests.
class UITestCase(UIBaseCase):
    def setUp(self):
        super().setUp()

    # Write the test for both browsers here. 
    def test_incorrect_password_registration(self):
        '''Testing the registration when passwords are incorrect.'''
        self._signup_user("wpass", "wpass@wpass.com", "12345678", "87654321", False)
        input_confirmation = self.web_driver.find_element_by_id("confirmation")
        self.assertEqual(input_confirmation.get_attribute("class"), "form-control is-invalid")
        div_feedback = self.web_driver.find_element_by_id("div_confirmation_feedback")
        self.assertEqual(div_feedback.text, "Invalid password. Please ensure your passwords are the same.")

    
class UITestCaseChrome(UITestCase, StaticLiveServerTestCase):
     def setUp(self):
        # Set Chrome to run headless so that it can work in automated tests of github actions
        super().setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.web_driver = webdriver.Chrome(options=options)
        self._signup_user("test", "test@test.com", "12345678", "12345678")
        # For the rest of the test methods, please refer to UITestCase

class UITestCaseFirefox(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        # Set Firefox to run headless so that it can work in automated tests
        super().setUp()
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.web_driver = webdriver.Firefox(options=options)
        self._signup_user("test", "test@test.com", "12345678", "12345678")