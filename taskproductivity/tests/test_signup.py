import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase

from selenium import webdriver

class ViewTestCase(ViewBaseCase): 
    def setUp(self):
        super().setUp()
        data = {
            'username': 'test', 
            'email': 'test@test.com', 
            'password':'1234', 
            'confirmation':'1234'
        }
        self._csrf_post("/signup", data)
        self.client.get("/logout")


    def test_signup_page(self):
        """Check if we signup page and if all functions are operational."""
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'test', 
            'email': 'test2@test.com', 
            'password':'1234', 
            'confirmation':'1234'
        }

        # Test that the API will not accept POST without csrf. 
        response = self.client.post("/signup", data)
        self.assertEqual(response.status_code, 403)

        # Test the case where we have the same username. 
        response = self._csrf_post("/signup", data)
        self.assertEqual(response.context['message'], "Username and/or email is already registered.")
        self.assertEqual(response.status_code, 400)

        # Test the case where we have the same email. 
        data['username'] = 'test2'
        data['email'] = 'test@test.com'

        response = self._csrf_post("/signup", data)
        self.assertEqual(response.context['message'], "Username and/or email is already registered.")
        self.assertEqual(response.status_code, 400)
        
        # Test the case where passwords are not the same. 
        data['email'] = 'test2@test.com'
        data['confirmation'] = '4321'
        response = self._csrf_post("/signup", data)
        self.assertEqual(response.context['message'], "Passwords must match.")
        self.assertEqual(response.status_code, 400)

        # Test the case where all the data are ok. 
        data['confirmation'] = '1234'
        response = self._csrf_post("/signup", data)
        self.assertEqual(response.url, '/tasks')
        self.assertEqual(response.status_code, 302)
    
    def test_username_check(self):
        """This is to test if the duplicated username check works or not"""
        data = {
            'username': 'test', 
        }
        # Test that the API will not accept POST without csrf. 
        response = self.client.post("/username", data)
        self.assertEqual(response.status_code, 403)

        response = self._csrf_post("/username", data, True)
        self.assertEqual(response.json(), {"unique": False})

        data['username'] = 'test3'
        response = self._csrf_post("/username", data, True)
        self.assertEqual(response.json(), {"unique": True})
    
    def test_email_check(self):
        """This is to test if the duplicated email check works or not"""
        data = {
            'email': 'test@test.com', 
        }

        # Test that the API will not accept POST without csrf. 
        response = self.client.post("/email", data)
        self.assertEqual(response.status_code, 403)

        response = self._csrf_post("/email", data, True)
        self.assertEqual(response.json(), {"unique": False}, True)

        data['email'] = 'test3@test.com'
        response = self._csrf_post("/email", data, True)
        self.assertEqual(response.json(), {"unique": True}, True)

# In order to speed up the completion of the project, I am going to omit all the tests.
class UITestCase(UIBaseCase):
    def setUp(self):
        super().setUp()

    # Write the test for both browsers here. 
    def test_incorrect_password_registration(self):
        '''Testing the registration when passwords are incorrect.'''
        self._signup_user("wpass", "wpass@wpass.com", "12345678", "87654321", False)
        self.assertEqual(self.chrome_driver.current_url, self.live_server_url+'/register')
        div_msg = self.chrome_driver.find_elements_by_name("div-msg")
        self.assertEqual(len(div_msg), 1)
        self.assertEqual(div_msg[0].text, "Passwords must match.")

    def test_repeated_username_registration(self):
        '''Testing the registration when username already exists.'''
        self._signup_user("test", "test2@test.com", "12345678", "12345678", False)

        div_msg = self.chrome_driver.find_elements_by_name("div-msg")
        self.assertEqual(len(div_msg), 1)
        self.assertEqual(div_msg[0].text, "It looks like test belongs to an existing account. Try again with a different username.")
    
    def test_repeated_email_registration(self):
        '''Testing the registration when the email entered exists in the system.'''
        self._signup_user("test2", "test@test.com", "12345678", "12345678", False)

        div_msg = self.chrome_driver.find_elements_by_name("div-msg")
        self.assertEqual(len(div_msg), 1)
        self.assertEqual(div_msg[0].text, "It looks like test@test.com belongs to an existing account. Try again with a different email address.")


    def test_registration(self):
        '''Testing the registration of a user'''
        self._signup_user("new_user", "new@new.com", "12345678", "12345678")
        self.assertEqual(self.web_driver.current_url, '%s%s' % (self.live_server_url, '/tasks'))
    

class UITestCaseChrome(UITestCase, StaticLiveServerTestCase):
     def setUp(self):
        # Set Chrome to run headless so that it can work in automated tests of github actions
        super().setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.web_driver = webdriver.Chrome(options=options)
        self.web_driver.implicitly_wait(1)
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