import json
from django.test import TestCase, Client

# The classes here are created to setup all of the required methods for all webpage test cases. 
class ViewBaseCase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
    
    def _csrf_post(self, url, data, json=False):
        resp = self.client.get(url)
        if resp.status_code != 200:
            resp = self.client.get('/')
        csfrtoken = resp.cookies['csrftoken'].value

        # If the post is JSON based.
        if json:
            response = self.client.post(url, data, content_type="application/json", HTTP_X_CSRFTOKEN=csfrtoken)
        else:
            data['csrfmiddlewaretoken'] = csfrtoken
            response = self.client.post(url, data)
        return response


class UIBaseCase(object):
    def setUp(self):
        self.web_driver = None
    
    def _signup_user(self, username, email, password, confirmation, click=True):
        self.web_driver.get('%s%s' % (self.live_server_url, '/signup'))
        self.web_driver.find_element_by_name('username').send_keys(username)
        self.web_driver.find_element_by_name('email').send_keys(email)
        self.web_driver.find_element_by_name('password').send_keys(password)
        self.web_driver.find_element_by_name('confirmation').send_keys(confirmation)
        if click:
            self.web_driver.find_element_by_id("signup").click()
    
    def _login(self, username, password):
        self.web_driver.get('%s%s' % (self.live_server_url, '/login'))
        self.web_driver.find_element_by_name('username').send_keys(username)
        self.web_driver.find_element_by_name('password').send_keys(password)
        self.web_driver.find_element_by_id("btn_signin").click()

    def tearDown(self):
        self.web_driver.quit()