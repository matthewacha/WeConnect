import os
import unittest
import json
from app import app
from app.v1 import users
from app.v1.users import views as users
from app.v1.models import Business, User
    

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        users.database = []
        users.Business = []

class TestUserApi(BaseTestCase):
    def test_Users(self):
        """Test user model"""
        user = User('james@gmail.com', 'latina' )
        self.assertEqual(user.email,'james@gmail.com' )

    def test_Businesses(self):
        """Tests business class"""
        business = Business("Fish To Go","We fish", "Kampala", "Foods",1111)
        self.assertEqual(business.name, "Fish To Go")
        new_name = business.change_name("Fishes")
        self.assertEqual(business.name, "Fishes")

    def test_register_business(self):
        """Tests that a business can be registered"""
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/v1/auth/login',
                                 content_type= 'application/json',
                                 data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        
        result = json.loads(login.data.decode())
        response = self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Fish To Go',
                                                        description='We sell fishy stuff',
                                                          location = 'Kampala',
                                                          category = "Food")),
                                    headers =dict(access_token = result['token']))#pragma:no cover
        self.assertIn(u'Successfully added business',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 200)

    def test_register_unique_business(self):
        """Test unique business is added"""
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/v1/auth/login',
                                 content_type= 'application/json',
                                 data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        
        result = json.loads(login.data.decode())
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Fish To Go',
                                                        description='We fishy',
                                                          location = 'Kampala',
                                                          category = "Food")),
                                    headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Fish To Go',
                                                        description='We sell fishy stuff',
                                                          location = 'Kampala',
                                                          category = "Food")),
                                    headers =dict(access_token = result['token']))#pragma:no cover
        self.assertIn(u'Business already exists, try another',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 401)

    def test_view_businesses(self):
        """tests businesses can be viewed by all users"""
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v1/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers =dict(access_token=result['token']))
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers=dict(access_token=result['token']))
        response = self.tester.get('/api/v1/businesses',
                                  content_type='application/json',
                                   headers=dict(access_token=result['token']))
        
        self.assertIn(u'School', response.data)
        self.assertEqual(response.status_code, 200)

    def test_view_wrong_business(self):
        """Tests that attempting to view noon existent business returns an error"""
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v1/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers =dict(access_token=result['token']))
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate",
                                                          businessId = 123)),
                         headers=dict(access_token=result['token']))
        response = self.tester.get('/api/v1/businesses/123',
                                  content_type='application/json',
                                   headers=dict(access_token=result['token']))
        
        data = json.loads(response.data.decode())
        self.assertIn(u'Business does not exist', response.data)
        self.assertEqual(response.status_code, 200)

    def test_edit_business(self):
        """Tests business can be edited by logged in user"""
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


        response = self.tester.put('/api/v1/businesses/1', content_type='application/json',
                                   data = json.dumps( dict(new_name='School is us',
                                                        new_description='We teach',
                                                          new_location = 'Entebbe',
                                                          new_category = "Educate")),
                                   headers=dict(access_token=result['token']))#pragma:no cover
        
        self.assertEqual(response.status_code, 200)#pragma:no cover
        self.assertIn(u'Successfully edited', response.data)#pragma:no cover



    def test_delete_business(self):
        """Tests that a business can be deleted by logged in user"""
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


        response = self.tester.delete('/api/v1/businesses/1',
                                      headers=dict(access_token=result['token']))#pragma:no cover
    
        self.assertEqual(response.status_code, 200)#pragma:no cover
        self.assertIn(u'Successfully deleted', response.data)#pragma:no cover



if __name__ == "__main__":
    unittest.main()
