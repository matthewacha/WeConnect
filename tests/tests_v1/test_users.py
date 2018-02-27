import unittest
import json
from app import app, db
from app.v1 import users
from app.v1.users import views as users

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        users.database = []
        users.Business = []
        
class TestUserApi(BaseTestCase):
    def test_incorrect_credential_login_failure(self):
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        response = self.tester.post('/api/v1/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='us@gmail.com',
                                                      password='amazon')))
        self.assertIn(u'Authorize with correct credentials',response.data)
        self.assertEqual(response.status_code, 401)

    def test_correct_credential_login(self):
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        response = self.tester.post('/api/v1/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v1/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='you@gmail.com',
                                                      password='lantern')))
        result = json.loads(login.data.decode())
        
        response = self.tester.post('/api/v1/auth/reset-password',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'you@gmail.com',
                                                           old_password = 'lantern',
                                                           new_password = 'laters')),
                                    headers =dict(access_token = result['token'])
                                    )

        self.assertIn(u'Successfully changed password',response.data)
        self.assertEqual(response.status_code, 200)



    def test_logout_user(self):
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/v1/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        result = json.loads(login.data.decode())

        response = self.tester.post('/api/v1/auth/logout',
                                    content_type = 'application/json',
                                    headers = dict(access_token = result['token']))
        
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'])
        self.assertIn(u'Successfully logged out', response.data)
        self.assertEqual(response.status_code, 200)

    #ensure user_token generated on login
    def test_token_generate(self):
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/v1/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        result = json.loads(login.data.decode())
        self.assertTrue(result['token'])
        self.assertEqual(login.status_code, 200)

if __name__ == '__main__':
    unittest.main()
