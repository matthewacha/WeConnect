import os
import unittest
import json
from app import app, users
from app.models import User, Business

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        pass

class TestUserApi(BaseTestCase):
    def test_sign_up_user(self):
        response = self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='greater')))
        self.assertIn(u'Successfully signed up',response.data)
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_unique_sign_up(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='greater')))
        response = self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(email='me@gmail.com',
                                                        password='greater')))
        data = json.loads(response.data.decode())
        self.assertIn(u'User already taken',data['message'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

        ##############
        ##TEST LOGIN##
        ##############

    def test_incorrect_credential_login_failure(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        response = self.tester.post('/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='us@gmail.com',
                                                      password='amazon')))
        self.assertIn(u'you need to use a correct email',response.data)
        self.assertEqual(response.status_code, 401)

    def test_correct_credential_login(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        response = self.tester.post('/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
