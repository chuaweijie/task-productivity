import json

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from datetime import datetime, timedelta

from time import sleep

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
        # BUG Logical error. The system should auto calculate and return data.
        online_start = datetime.fromisoformat('2021-06-04') - timedelta(days=14)
        online_end = datetime.fromisoformat('2021-06-04') - timedelta(days=7)
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": {   "id": 2,
                                                        "entry": None, 
                                                        "renewal": (datetime.fromisoformat('2021-06-04') + timedelta(days=90)).timestamp(),
                                                        "online_start": (datetime.fromisoformat('2021-06-04') + timedelta(days=90) - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-06-04') + timedelta(days=90) - timedelta(days=7)).timestamp()}
                                            })

        response = self.client.get("/history")
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-05-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-05-04') - timedelta(days=7)).timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-06-04').timestamp()}]
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
                                            "data": [{   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "departure": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": None},
                                                    {   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-05-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-05-04') - timedelta(days=7)).timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-06-04').timestamp()}]
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
        self.assertEqual(response.json(), { "status": "successful",
                                    "data": {   "id": 5,
                                                "entry": None, 
                                                "renewal": (datetime.fromisoformat('2021-08-31') + timedelta(days=90)).timestamp(),
                                                "online_start": (datetime.fromisoformat('2021-08-31') + timedelta(days=90) - timedelta(days=14)).timestamp(),
                                                "online_end": (datetime.fromisoformat('2021-08-31') + timedelta(days=90) - timedelta(days=7)).timestamp()}
                                    })
        
        data = {
            "id": 5
        }
        response = self._csrf_delete("/tracking", data, True)
        self.assertEqual(response.json(), {"status": "successful",
                                            "data": None
                                            })
        
        response = self.client.get("/history")
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 4,
                                                        "entry": datetime.fromisoformat('2021-08-04').timestamp(), 
                                                        "renewal": renewal.timestamp(), 
                                                        "online_start": online_start.timestamp(),
                                                        "online_end": online_end.timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-08-31').timestamp()},
                                                    {   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-07-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-07-04') - timedelta(days=7)).timestamp(),
                                                        "departure": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": None},
                                                    {   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-05-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-05-04') - timedelta(days=7)).timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-06-04').timestamp()}]
                                            })

        # Testing undo
        data = {
                "mode": "undo", 
                "id": 4
        }
        response = self._csrf_put("/history" ,data, True)
        self.assertEqual(response.json(), { "status": "successful",
                                            "data": [{   "id": 3,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-07-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-07-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-07-04') - timedelta(days=7)).timestamp(),
                                                        "departure": datetime.fromisoformat('2021-07-15').timestamp(),
                                                        "reported_date": None},
                                                    {   "id": 1,
                                                        "entry": None, 
                                                        "renewal": datetime.fromisoformat('2021-05-04').timestamp(), 
                                                        "online_start": (datetime.fromisoformat('2021-05-04') - timedelta(days=14)).timestamp(),
                                                        "online_end": (datetime.fromisoformat('2021-05-04') - timedelta(days=7)).timestamp(),
                                                        "departure": None,
                                                        "reported_date": datetime.fromisoformat('2021-06-04').timestamp()}]
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

    def _check_tracking_elements_blank(self):
        tab_tracking = self.web_driver.find_element_by_id("tab_tracking")
        tab_tracking.click()

        tab_tracking = self.web_driver.find_elements_by_name("tab_tracking")
        tab_history = self.web_driver.find_elements_by_name("tab_history")
        btn_entry = self.web_driver.find_elements_by_name("btn_entry")
        btn_renewal = self.web_driver.find_elements_by_name("btn_renewal")

        self.assertEqual(len(tab_tracking), 1)
        self.assertEqual(len(tab_history), 1)
        self.assertEqual(len(btn_entry), 1)
        self.assertEqual(len(btn_renewal), 1)

    def _check_tracking_elements_with_record(self, entry, online_start, online_end, renewal):
        tab_tracking = self.web_driver.find_element_by_id("tab_tracking")
        tab_tracking.click()

        row_entry = self.web_driver.find_elements_by_name("row_entry")
        row_online_start = self.web_driver.find_elements_by_name("row_online_start")
        row_online_end = self.web_driver.find_elements_by_name("row_online_end")
        row_renewal = self.web_driver.find_elements_by_name("row_renewal")
        btn_report = self.web_driver.find_elements_by_name("btn_report")
        btn_depart = self.web_driver.find_elements_by_name("btn_depart")
        btn_delete = self.web_driver.find_elements_by_name("btn_delete")
        btn_gcal = self.web_driver.find_elements_by_name("btn_gcal")
        btn_ical = self.web_driver.find_elements_by_name("btn_ical")
        btn_outlook = self.web_driver.find_elements_by_name("btn_outlook")
        btn_yahoo = self.web_driver.find_elements_by_name("btn_yahoo")

        # Renewal: Check UI elements
        self.assertEqual(len(row_entry), 1)
        self.assertEqual(len(row_online_start), 1)
        self.assertEqual(len(row_online_end), 1)
        self.assertEqual(len(row_renewal), 1)
        self.assertEqual(len(btn_report), 1)
        self.assertEqual(len(btn_depart), 1)
        self.assertEqual(len(btn_delete), 1)
        self.assertEqual(len(btn_gcal), 1)
        self.assertEqual(len(btn_ical), 1)
        self.assertEqual(len(btn_outlook), 1)
        self.assertEqual(len(btn_yahoo), 1)

        # Renewal: Check texts on buttons
        self.assertEqual(btn_report[0].text, "Report")
        self.assertEqual(btn_depart[0].text, "Depart")

        self.assertEqual(row_entry[0].text, entry)
        self.assertEqual(row_online_start[0].text, online_start)
        self.assertEqual(row_online_end[0].text, online_end)
        self.assertEqual(row_renewal[0].text, renewal)

    def _renew(self, date, btn="btn_renewal"):
        btn_renewal = self.web_driver.find_element_by_id(btn)
        btn_renewal.click()

        date_renewal = self.web_driver.find_element_by_id("dateEntry")
        date_renewal.click()
        date_renewal.send_keys(date, Keys.TAB, "2021")
        sleep(0.1)
        btn_submit = self.web_driver.find_element_by_id("btn_submit")
        btn_submit.click()
    
    def _check_history(self, data, row_num):
        tab_history = self.web_driver.find_element_by_id("tab_history")
        tab_history.click()

        tbl_history_id = self.web_driver.find_elements_by_name("tbl_history_id")
        tbl_history_entry = self.web_driver.find_elements_by_name("tbl_history_entry")
        tbl_history_renewal = self.web_driver.find_elements_by_name("tbl_history_renewal")
        tbl_history_online_start = self.web_driver.find_elements_by_name("tbl_history_online_start")
        tbl_history_online_end = self.web_driver.find_elements_by_name("tbl_history_online_end")
        tbl_history_depart = self.web_driver.find_elements_by_name("tbl_history_depart")
        tbl_history_reported_date = self.web_driver.find_elements_by_name("tbl_history_reported_date")

        for i in range(row_num):
            self.assertEqual(tbl_history_id[i].text, data[i]["id"])
            self.assertEqual(tbl_history_entry[i].text, data[i]["entry"])
            self.assertEqual(tbl_history_renewal[i].text, data[i]["renewal"])
            self.assertEqual(tbl_history_online_start[i].text, data[i]["online_start"])
            self.assertEqual(tbl_history_online_end[i].text, data[i]["online_end"])
            self.assertEqual(tbl_history_depart[i].text, data[i]["depart"])
            self.assertEqual(tbl_history_reported_date[i].text, data[i]["reported_date"])

    # Write the test for both browsers here. 
    def test_full_tracking_flow(self):
        '''This is one test that test all the UI interactions of the system'''
        self.web_driver.implicitly_wait(1)
        self._signup_user(self.username, self.email, self.password, self.password, False)
        self._login(self.username, self.password)
        # Test the existance of tracking, history, entry and renewal since start.
        self._check_tracking_elements_blank()
        # TODO: I suspect I will need to add test cases to test if the tab is active or not. 

        # Test adding renewal.
        self._renew("0405")

        # Renewal: Check the page render after the renewal adding has been added successfully. 
        self._check_tracking_elements_with_record("-", "Tue Apr 20 2021", "Tue Apr 27 2021", "Tue May 04 2021")
        
        btn_renew = self.web_driver.find_element_by_id("btn_report")
        btn_renew.click()

        # Test cancel button after 
        btn_cancel = self.web_driver.find_element_by_id("btn_cancel")
        btn_cancel.click()

        self._renew("0406", "btn_report")

        # Reported: Check the page render after the renewal adding has been added successfully. 
        self._check_tracking_elements_with_record("-", "Thu Aug 19 2021", "Thu Aug 26 2021", "Thu Sep 02 2021")
        
        # Test delete
        btn_delete = self.web_driver.find_element_by_id("btn_delete")
        btn_delete.click()
        btn_cancel = self.web_driver.find_element_by_id("btn_cancel")
        btn_cancel.click()
        btn_delete = self.web_driver.find_element_by_id("btn_delete")
        btn_delete.click()
        btn_yes = self.web_driver.find_element_by_id("btn_yes")
        btn_yes.click()

        self._check_tracking_elements_blank()
        
        self._renew("0407")
        self._check_tracking_elements_with_record("-", "20 June 2021", "27 June 2021", "4 July 2021")

        # Test departure
        btn_depart = self.web_driver.find_element_by_id("btn_depart")
        btn_depart.click()

        date_depart = self.web_driver.find_element_by_id("date_depart")
        date_depart.click()
        date_depart.send_keys("1507", Keys.TAB ,"2021")

        self._check_tracking_elements_blank()
        
        # Test clicking on history to check records
        data = [{   "id": 1,
                    "entry": "-", 
                    "renewal": "4 May 2021", 
                    "online_start": "20 April 2021",
                    "online_end": "27 April 2021",
                    "depart": "-",
                    "reported_date": "4 June 2021"},
                {   "id": 3,
                    "entry": "-", 
                    "renewal": "4 July 2021", 
                    "online_start": "20 June 2021",
                    "online_end": "27 June 2021",
                    "depart": "15 July 2021",
                    "reported_date": "-"}]
        
        self._check_history(data, 2)

        # Test adding a tracking with entry date.
        tab_tracking = self.web_driver.find_element_by_id("tab_tracking")
        tab_tracking.click()

        btn_entry = self.web_driver.find_element_by_id("btn_entry")
        btn_entry.click()
        date_depart = self.web_driver.find_element_by_id("date_entry")
        date_depart.click()
        date_depart.send_keys("0408", Keys.TAB, "2021")
        btn_submit = self.web_driver.find_element_by_id("btn_submit")
        btn_submit.click()

        self._check_tracking_elements_with_record("4 August 2021", "21 August 2021", "28 August 2021", "3 September 2021")

        # Test marking as reported to check history
        self._renew("3108", "btn_report")
        data = [{   "id": 1,
                    "entry": "-", 
                    "renewal": "4 May 2021", 
                    "online_start": "20 April 2021",
                    "online_end": "27 April 2021",
                    "depart": "-",
                    "reported_date": "4 June 2021"},
                {   "id": 3,
                    "entry": "-", 
                    "renewal": "4 July 2021", 
                    "online_start": "20 June 2021",
                    "online_end": "27 June 2021",
                    "depart": "15 July 2021",
                    "reported_date": "-"}, 
                {   "id": 4,
                    "entry": "4 August 2021", 
                    "renewal": "3 September 2021", 
                    "online_start": "21 August 2021",
                    "online_end": "28 August 2021",
                    "departure": "-",
                    "reported_date": "31 August 2021"}]

        # The history has one more record
        self._check_history(data, 3)
        
        # Delete the newest record created from the renewal above.
        tab_tracking = self.web_driver.find_element_by_id("tab_tracking")
        tab_tracking.click()
        btn_delete = self.web_driver.find_element_by_id("btn_delete")
        btn_delete.click()
        btn_yes = self.web_driver.find_element_by_id("btn_yes")
        btn_yes.click()

        self._check_tracking_elements_blank()

        tab_history = self.web_driver.find_element_by_id("tab_history")
        tab_history.click()

        btn_undo = self.web_driver.find_element_by_id("btn_undo")
        btn_undo.click()

        data = [{   "id": 1,
                    "entry": "-", 
                    "renewal": "4 May 2021", 
                    "online_start": "20 April 2021",
                    "online_end": "27 April 2021",
                    "depart": "-",
                    "reported_date": "4 June 2021"},
                {   "id": 3,
                    "entry": "-", 
                    "renewal": "4 July 2021", 
                    "online_start": "20 June 2021",
                    "online_end": "27 June 2021",
                    "depart": "15 July 2021",
                    "reported_date": "-"}]

        # The history has one less record
        self._check_history(data, 2)
        self._check_tracking_elements_with_record("4 August 2021", "21 August 2021", "28 August 2021", "3 September 2021")


    
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