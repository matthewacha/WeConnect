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
    #ensure reviews can be added for business
    def test_add_review(self):
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v1/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v1/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        
        response = self.tester.post('/api/v1/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "It's awesome")),
                                    headers = dict(access_token = result['token']))
        #data = json.loads(response.data.decode())
        self.assertIn(u'Successfully added review', response.data)
        self.assertEqual(response.status_code, 200)

    #ensure reviews can be viewed for business
    def test_view_reviews(self):
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v1/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v1/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        self.tester.post('/api/v1/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "It's awesome")),
                                    headers = dict(access_token = result['token']))
        self.tester.post('/api/v1/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "Amazing place")),
                                    headers = dict(access_token = result['token']))
        self.tester.post('/api/v1/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "Chef Rico is the best!")),
                                    headers = dict(access_token = result['token']))
        
        response = self.tester.get('/api/v1/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    headers = dict(access_token = result['token']))

        self.assertIn(u'Amazing place', response.data)
        self.assertEqual(response.status_code, 200)
