from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .base_case import ViewBaseCase, UIBaseCase
from django.db.transaction import TransactionManagementError

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

        # Test the case where we have the same username. 
        with self.assertRaises(TransactionManagementError):
            self._csrf_post("/signup", data)

        # Test the case where we have the same email. 
        data['username'] = 'test2'
        data['email'] = 'test@test.com'

        with self.assertRaises(TransactionManagementError):
            self._csrf_post("/signup", data)
        
        # Test the case where passwords are not the same. 
        data['email'] = 'test2@test.com'
        data['confirmation'] = '4321'
        response = self._csrf_post("/register", data)
        self.assertEqual(response.context['message'], "Passwords must match.")
        self.assertEqual(response.status_code, 200)

        # Test the case where all the data are ok. 
        data['confirmation'] = '1234'
        response = self._csrf_post("/signup", data)
        self.assertEqual(response.url, '/')
        self.assertEqual(response.status_code, 302)


class UITestCase(UIBaseCase):
    def setUp(self):
        super().setUp()
        self._signup_user("test", "test@test.com", "1234", "1234")

    # Write the test for both browsers here. 
    def _signup_user(self, username, email, password, confirmation):
        self.web_driver.get('%s%s' % (self.live_server_url, '/signup'))
        self.web_driver.find_element_by_name('username').send_keys(username)
        self.web_driver.find_element_by_name('email').send_keys(email)
        self.web_driver.find_element_by_name('password').send_keys(password)
        self.web_driver.find_element_by_name('confirmation').send_keys(confirmation)
        self.web_driver.find_element_by_id("signup").click()
    
    def test_signup(self):
        url = self.live_server_url
        self.web_driver.get(url)

    def test_incorrect_password_registration(self):
        '''Testing the registration when passwords are incorrect.'''
        self._signup_user("wpass", "wpass@wpass.com", "1234", "4321")

        self.assertEqual(self.chrome_driver.current_url, self.live_server_url+'/register')
        div_msg = self.chrome_driver.find_elements_by_name("div-msg")
        self.assertEqual(len(div_msg), 1)
        self.assertEqual(div_msg[0].text, "Passwords must match.")

    def test_repeated_username_registration(self):
        '''Testing the registration when username already exists.'''
        self._signup_user("test", "test2@test.com", "1234", "1234")

        div_msg = self.chrome_driver.find_elements_by_name("div-msg")
        self.assertEqual(len(div_msg), 1)
        self.assertEqual(div_msg[0].text, "It looks like fuqin belongs to an existing account. Try again with a different username.")
    
    def test_repeated_email_registration(self):
        '''Testing the registration when the email entered exists in the system.'''
        self._signup_user("test2", "test@test.com", "1234", "1234")

        div_msg = self.chrome_driver.find_elements_by_name("div-msg")
        self.assertEqual(len(div_msg), 1)
        self.assertEqual(div_msg[0].text, "It looks like test@test.com belongs to an existing account. Try again with a different email address.")


    def test_registration(self):
        '''Testing the registration of a user'''
        self._signup_user("new_user", "new@new.com", "1234", "1234")
        self.assertEqual(self.web_driver.current_url, '%s%s' % (self.live_server_url, '/tasks'))
    

class UITestCaseChrome(UITestCase, StaticLiveServerTestCase):
     def setUp(self):
        # Set Chrome to run headless so that it can work in automated tests of github actions
        super().setUp()
        options = webdriver.ChromeOptions()
        options.headless = True
        self.web_driver = webdriver.Chrome(options=options)
        # For the rest of the test methods, please refer to UITestCase

class UITestCaseFirefox(UITestCase, StaticLiveServerTestCase):
    def setUp(self):
        # Set Firefox to run headless so that it can work in automated tests
        super().setUp()
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.web_driver = webdriver.Firefox(options=options)