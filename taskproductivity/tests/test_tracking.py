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
                                                        "online_start": (datetime.fromisoformat('2021-05-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-05-04') - timedelta(days=7)).timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-06-04').timestamp()},
                                                    {   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "departure": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": None}]
                                            })

        # Test the case of adding a new entry with the arrival date
        data = {
            "mode": "entry", 
            "entry": datetime.fromisoformat('2021-08-04').timestamp()
        }
        response = self._csrf_post("/tracking" ,data, True)
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
        response = self._csrf_put("/tracking" ,data, True)
        self.assertEqual(response.json(), {"status": "successful",
                                            "data": None
                                            })
        
        response = self.client.get("/history")
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-05-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-05-04') - timedelta(days=7)).timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-06-04').timestamp()},
                                                    {   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-07-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-07-04') - timedelta(days=7)).timestamp(),
                                                        "departure": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": None},
                                                    {   "id": 4,
                                                        "entry": datetime.fromisoformat('2021-08-04').timestamp(), 
                                                        "renewal": renewal.timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-08-31').timestamp()}]
                                            })

        # Testing undo
        data = {
                "mode": "undo", 
                "id": 4
        }
        response = self._csrf_put("/history" ,data, True)
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-05-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-05-04') - timedelta(days=7)).timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-06-04').timestamp()},
                                                    {   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-07-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-07-04') - timedelta(days=7)).timestamp(),
                                                        "departure": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": None}]
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
        
        # Write code to test undo when there is an active tracking
        data = {
                "mode": "undo", 
                "id": 3
        }
        response = self._csrf_put("/history" ,data, True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), { "status": "Error",
                                            "msg": "Active tracking data"
                                            })
        

# In order to speed up the completion of the project, I am going to omit all the tests.
class UITestCase(UIBaseCase):
    def setUp(self):
        super().setUp()
        self.username = "test_user"
        self.email = "test_user@test.com"
        self.password = "12345678"

    # Write the test for both browsers here. 
    def test_full_tracking_flow(self):
        '''This is one test that test all the UI interactions of the system'''
        self._login(self.username, self.password)
        self._signup_user("wpass", "wpass@wpass.com", "12345678", "87654321", False)
        
        # Test the existance of tracking, history, entry and renewal since start.
        tab_tracking = self.web_driver.find_element_by_name("tab_tracking")
        tab_history = self.web_driver.find_element_by_name("tab_history")
        btn_entry = self.web_driver.find_element_by_name("btn_entry")
        btn_renewal = self.web_driver.find_element_by_name("btn_renewal")

        self.assertEqual(len(tab_tracking), 1)
        self.assertEqual(len(tab_history), 1)
        self.assertEqual(len(btn_entry), 1)
        self.assertEqual(len(btn_renewal), 1)
        # TODO: I suspect I will need to add test cases to test if the tab is active or not. 

        # Test adding renewal.
        btn_renewal[0].click()

        date_renewal = self.web_driver.find_element_by_id("date_renewal")
        date_renewal.click()
        date_renewal.send_keys("04052021")

        btn_submit = self.web_driver.find_element_by_id("btn_submit")
        btn_submit.click()

        # Check the page render after the renewal adding has been added successfully. 
        row_entry = self.web_driver.find_element_by_name("row_entry")
        row_online_start = self.web_driver.find_element_by_name("row_online_start")
        row_online_end = self.web_driver.find_element_by_name("row_online_end")
        row_renewal = self.web_driver.find_element_by_name("row_renewal")
        btn_renew = self.web_driver.find_element_by_name("btn_renew")
        btn_departure = self.web_driver.find_element_by_name("btn_departure")
        btn_gcal = self.web_driver.find_element_by_name("btn_gcal")
        btn_ical = self.web_driver.find_element_by_name("btn_ical")
        btn_outlook = self.web_driver.find_element_by_name("btn_outlook")
        btn_yahoo = self.web_driver.find_element_by_name("btn_yahoo")

        # Check UI elements
        self.assertEqual(len(row_entry), 1)
        self.assertEqual(len(row_online_start), 1)
        self.assertEqual(len(row_online_end), 1)
        self.assertEqual(len(row_renewal), 1)
        self.assertEqual(len(btn_renew), 1)
        self.assertEqual(len(btn_departure), 1)
        self.assertEqual(len(btn_gcal), 1)
        self.assertEqual(len(btn_ical), 1)
        self.assertEqual(len(btn_outlook), 1)
        self.assertEqual(len(btn_yahoo), 1)

        # Check texts on buttons
        self.assertEqual(btn_renew[0].text, "Renew")
        self.assertEquan(btn_departure[0].text, "Departure")

        # Check data
        self.assertEqual(row_entry[0].text, "-")
        self.assertEqual(row_online_start[0].text, "20 April 2021")
        self.assertEqual(row_online_end[0].text, "27 April 2021")
        self.assertEqual(row_renewal[0].text, "4 May 2021")
        


        # TODO Test adding a new tracking where the renewal date is known

        # TODO Test marking as reported
        # TODO Test delete
            # Test add then delete
        # TODO Test departure
            # Test marking a tracking as renewal
        # TODO Test clicking on history to check records
        # TODO Test adding a tracking with entry date. 
        # TODO Test marking as reported to check history
            # The history has one more record
        # TODO Testing undo
            # Testing list history after undo
            # Test undo when there is an active tracking 


    
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