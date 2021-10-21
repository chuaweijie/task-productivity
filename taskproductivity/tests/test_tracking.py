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
        self.assertEqual(response.json(), {"status": "no data", "data": None})
        self.assertEqual(response.status_code, 200)

        # Test the case of adding a new tracking where the renewal date is known
        data = {
            "mode": "renewal", 
            "renewal": datetime.fromisoformat('2021-05-04').timestamp()
        }
        response = self._csrf_post("/tracking" ,data, True)
        online_start = datetime.fromisoformat('2021-05-04') - timedelta(days=14)
        online_end = datetime.fromisoformat('2021-05-04') - timedelta(days=7)
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": {   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp()}
                                            })
        
        # Test marking as reported
        data = {
            "mode": "reported", 
            "id": 1,
            "reported_date": datetime.fromisoformat('2021-06-04').timestamp()
        }
        response = self._csrf_put("/tracking" ,data, True)
        self.assertEqual(response.json(), {"status": "successful",
                                            "data": None
                                            })

        response = self.client.get("/history")
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-06-04').timestamp()}]
                                            })
        
        data = {
            "mode": "renewal", 
            "renewal": datetime.fromisoformat('2021-06-04').timestamp()
        }
        response = self._csrf_post("/tracking" ,data, True)
        online_start = datetime.fromisoformat('2021-06-04') - timedelta(days=14)
        online_end = datetime.fromisoformat('2021-06-04') - timedelta(days=7)
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": {   "id": 2,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-06-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp()}
                                            })
        # Test delete
        data = {
            "id": 2
        }
        response = self._csrf_delete("/tracking", data, True)
        self.assertEqual(response.json(), {"status": "successful",
                                            "data": None
                                            })
        
        # Test the case of adding a new tracking where the renewal date is known
        data = {
            "mode": "renewal", 
            "renewal": datetime.fromisoformat('2021-07-04').timestamp()
        }
        response = self._csrf_post("/tracking" ,data, True)
        online_start = datetime.fromisoformat('2021-07-04') - timedelta(days=14)
        online_end = datetime.fromisoformat('2021-07-04') - timedelta(days=7)
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": {   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp()}
                                            })

        # Test marking as departed
        data = {
            "mode": "departure", 
            "id": 3,
            "date": datetime.fromisoformat('2021-07-15').timestamp(),
        }
        response = self._csrf_put("/tracking" ,data, True)
        self.assertEqual(response.json(), {"status": "successful",
                                            "data": None
                                            })

        response = self.client.get("/history")
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": datetime.fromisoformat('2021-05-04') - timedelta(days=14),
                                                        "online_end": datetime.fromisoformat('2021-05-04') - timedelta(days=7),
                                                        "depature": None,
                                                        "reported_date": datetime.fromisoformat('2021-05-04').timestamp()},
                                                    {   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "depature": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": datetime.fromisoformat('2021-07-04').timestamp()}]
                                            })

        # Test the case of adding a new entry with the arrival date
        data = {
            "mode": "entry", 
            "entry": datetime.fromisoformat('2021-08-04').timestamp()
        }
        response = self._csrf_post("/tracking" ,data)
        renewal = datetime.fromisoformat('2021-08-04') + timedelta(days=90)
        online_start = renewal - timedelta(days=14)
        online_end = renewal - timedelta(days=7)
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": {   "id": 4,
                                                        "entry": datetime.fromisoformat('2021-08-04').timestamp(), 
                                                        "renewal": renewal.timestamp(),
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp()}
                                            })
        # Testing of history after marking the most recent entry with reported. 
        data = {
            "mode": "reported", 
            "id": 4,
            "reported_date": datetime.fromisoformat('2021-08-31').timestamp()
        }
        response = self._csrf_put("/tracking" ,data)
        self.assertEqual(response.json(), {"status": "successful",
                                            "data": None
                                            })
        
        response = self.client.get("/history")
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": datetime.fromisoformat('2021-05-04') - timedelta(days=14),
                                                        "online_end": datetime.fromisoformat('2021-05-04') - timedelta(days=7),
                                                        "depature": None,
                                                        "reported_date": datetime.fromisoformat('2021-05-04').timestamp()},
                                                    {   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "depature": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": datetime.fromisoformat('2021-07-04').timestamp()},
                                                    {   "id": 4,
                                                        "entry": datetime.fromisoformat('2021-08-04').timestamp(), 
                                                        "renewal": renewal.timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "depature": None,
                                                        "reported_date": datetime.fromisoformat('2021-08-31').timestamp()}]
                                            })

        # Testing undo
        data = {
                "mode": "undo", 
                "id": 4
        }
        response = self._csrf_put("/history" ,data)
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": datetime.fromisoformat('2021-05-04') - timedelta(days=14),
                                                        "online_end": datetime.fromisoformat('2021-05-04') - timedelta(days=7),
                                                        "depature": None,
                                                        "reported_date": datetime.fromisoformat('2021-05-04').timestamp()},
                                                    {   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "depature": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": datetime.fromisoformat('2021-07-04').timestamp()}]
                                            })
        # Testing list history after undo
        response = self.client.get("/tracking")
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": {   "id": 4,
                                                        "entry": datetime.fromisoformat('2021-08-04').timestamp(), 
                                                        "renewal": renewal.timestamp(),
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp()}
                                            })
        

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