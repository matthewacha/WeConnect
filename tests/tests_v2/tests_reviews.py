import os
import unittest
import json
from app import app, db
from app.v2 import users
from app.v2.users import views as users
from app.v2.models import Business, User
    

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestUserApi(BaseTestCase):
    def test_add_review(self):
        """ensure reviews can be added for business"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        
        response = self.tester.post('/api/v2/businesses/1/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(description = "It's awesome")),
                                    headers = dict(access_token = result['token']))
        self.assertIn(u'Successfully added', response.data)
        self.assertEqual(response.status_code, 200)

    def test_fail_add_review(self):
        """Ensure review cannot be added with error"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        
        response = self.tester.post('/api/v2/businesses/1/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "It's awesome")),
                                    headers = dict(access_token = result['token']))
        self.assertIn(u'Exited with error', response.data)
        self.assertEqual(response.status_code, 401)

    def test_fail_add_review_none_business(self):
        """Ensure review cannot be added for non-existent business"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        
        response = self.tester.post('/api/v2/businesses/2/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(description = "It's awesome")),
                                    headers = dict(access_token = result['token']))
        self.assertIn(u'Business does not exist', response.data)
        self.assertEqual(response.status_code, 401)
        
    def test_view_reviews(self):
        """ensure reviews can be viewed for business"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        self.tester.post('/api/v2/businesses/1/reviews',
                         content_type = 'application/json',
                         data = json.dumps(dict(description = "It's awesome")),
                         headers = dict(access_token = result['token']))
        self.tester.post('/api/v2/businesses/1/reviews',
                         content_type = 'application/json',
                         data = json.dumps(dict(description = "Amazing place")),
                         headers = dict(access_token = result['token']))
        self.tester.post('/api/v2/businesses/1/reviews',
                         content_type = 'application/json',
                         data = json.dumps(dict(description = "Favorite ever")),
                         headers = dict(access_token = result['token']))

        
        response = self.tester.get('/api/v2/businesses/1/reviews',
                                   headers=dict(access_token=result['token']))

        self.assertIn(u'Amazing place', response.data)
        self.assertEqual(response.status_code, 200)

    def test_fail_view_reviews(self):
        """ensure reviews cannot be viewed for non existent business"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        self.tester.post('/api/v2/businesses/1/reviews',
                         content_type = 'application/json',
                         data = json.dumps(dict(description = "It's awesome")),
                         headers = dict(access_token = result['token']))
        self.tester.post('/api/v2/businesses/1/reviews',
                         content_type = 'application/json',
                         data = json.dumps(dict(description = "Amazing place")),
                         headers = dict(access_token = result['token']))
        self.tester.post('/api/v2/businesses/1/reviews',
                         content_type = 'application/json',
                         data = json.dumps(dict(description = "Favorite ever")),
                         headers = dict(access_token = result['token']))

        
        response = self.tester.get('/api/v2/businesses/2/reviews',
                                   headers=dict(access_token=result['token']))

        self.assertIn(u'Business does not exist', response.data)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
