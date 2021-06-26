from django.test import TestCase, Client

# The classes here are created to setup all of the required methods for all webpage test cases. 
class ViewBaseCase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
    
    def _csrf_post(self, url, data):
        resp = self.client.get(url)
        if resp.status_code != 200:
            resp = self.client.get('/')
        data['csrfmiddlewaretoken'] = resp.cookies['csrftoken'].value
        response = self.client.post(url, data)
        return response

class UIBaseCase(object):
    def setUp(self):
        self.web_driver = None
    
    def tearDown(self):
        self.web_driver.quit()