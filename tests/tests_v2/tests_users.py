import unittest
import json
from app import app, db
from app.v1 import users
from app.v1.users import views as users
#from app.businesses import views as businesses

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestUserApi(BaseTest):    
    def test_add_user(self):
        """Test that a new user can be added"""
        response = self.tester.post('/api/v2/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(email = 'me@gmail.com',
                                                 password = 'animal')))
        
        self.assertIn(u'Successfully signed up', response.data)
        self.assertEqual(response.status_code, 200)

    def test_add_unique_user(self):
        """tests that a unique user is added"""
        self.tester.post('/api/v2/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(email = 'me@gmail.com',
                                                 password = 'animal')))
        
        response = self.tester.post('/api/v2/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(email = 'me@gmail.com',
                                                 password = 'animal')))
        
        self.assertIn(u'User already exists', response.data)
        self.assertEqual(response.status_code, 401)


    def test_login_with_credentials(self):
        """test that a user can signup with correct credentials"""
        self.tester.post('/api/v2/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(email = 'me@gmail.com',
                                                      password = 'animal')))
        response = self.tester.post('/api/v2/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'animal')))
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        """test that a user cannot signup with incorrect password"""
        self.tester.post('/api/v2/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(email = 'me@gmail.com',
                                                      password = 'animal')))
        response = self.tester.post('/api/v2/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'animals')))
        self.assertEqual(response.status_code, 401)
        self.assertIn(u'Login with correct password', response.data)

    def test_invalid_email_login(self):
        """test that a user cannot signup with incorrect email"""
        self.tester.post('/api/v2/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(email = 'me@gmail.com',
                                                      password = 'animal')))
        response = self.tester.post('/api/v2/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'mea@gmail.com',
                                                           password = 'animals')))
        self.assertEqual(response.status_code, 401)
        self.assertIn(u'User does not exist', response.data)

    def test_password_reset(self):
        """test that a user can reset password"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v2/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='you@gmail.com',
                                                      password='lantern')))
        result = json.loads(login.data.decode())
        
        response = self.tester.post('/api/v2/auth/reset_password',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'you@gmail.com',
                                                           old_password = 'lantern',
                                                           new_password = 'laters')),
                                    headers =dict(access_token = result['token'])
                                    )

        self.assertIn(u'Successfully changed password',response.data)
        self.assertEqual(response.status_code, 200)

    def test_failed_password_reset(self):
        """test that a user cannot reset password with missing credentials"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/v2/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='you@gmail.com',
                                                      password='lantern')))
        result = json.loads(login.data.decode())
        
        response = self.tester.post('/api/v2/auth/reset_password',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'you@gmail.com',
                                                           old_password = '',
                                                           new_password = 'laters')),
                                    headers =dict(access_token = result['token'])
                                    )

        self.assertIn(u'Fill all credentials',response.data)
        self.assertEqual(response.status_code, 401)


"""
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
        self.assertEqual(login.status_code, 200)"""

if __name__ == '__main__':
    unittest.main()
