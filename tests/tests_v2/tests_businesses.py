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

    def test_register_business(self):
        """tests that a business can be created"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/v2/auth/login',
                                 content_type= 'application/json',
                                 data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        
        result = json.loads(login.data.decode())
        response = self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Fishes',
                                                        description='We deal fishy stuff',
                                                          location = 'Jinja',
                                                          category = "Foods")),
                                    headers =dict(access_token = result['token']))#pragma:no cover
        self.assertIn(u'Successfully added business',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 200)

    def test_fail_register_business(self):
        """tests that a business cannot be created if it exists"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/v2/auth/login',
                                 content_type= 'application/json',
                                 data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        
        result = json.loads(login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Fishes',
                                                        description='We deal fishy stuff',
                                                          location = 'Jinja',
                                                          category = "Foods")),
                                    headers =dict(access_token = result['token']))
        response = self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Fishes',
                                                        description='We deal fishy stuff',
                                                          location = 'Jinja',
                                                          category = "Foods")),
                                    headers =dict(access_token = result['token']))#pragma:no cover
        self.assertIn(u'Business already exists',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 401)

    def test_view_businesses(self):
        """Tests if businesses can be viewed"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers =dict(access_token=result['token']))
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers=dict(access_token=result['token']))
        response = self.tester.get('/api/v2/businesses',
                                  content_type='application/json',
                                   headers=dict(access_token=result['token']))
        self.assertIn(u'School', response.data)
        self.assertEqual(response.status_code, 200)
        

    def test_view_business(self):
        """Test retrieve business by id"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers =dict(access_token=result['token']))
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers=dict(access_token=result['token']))
        response = self.tester.get('/api/v2/businesses/2',
                                  content_type='application/json',
                                   headers=dict(access_token=result['token']))
        self.assertIn(u'School', response.data)
        self.assertEqual(response.status_code, 200)

    def test_fail_view_business(self):
        """Test fail to find a business with wrong id"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers =dict(access_token=result['token']))
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers=dict(access_token=result['token']))
        response = self.tester.get('/api/v2/businesses/5',
                                  content_type='application/json',
                                   headers=dict(access_token=result['token']))
        self.assertIn(u'Business does not exist', response.data)
        self.assertEqual(response.status_code, 401)


    def test_edit_business(self):
        """Test update business profile"""
        self.tester.post('/api/v2/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v2/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers =dict(access_token=result['token']))
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers=dict(access_token=result['token']))

        response = self.tester.put('/api/v2/businesses/2', content_type='application/json',
                                   data = json.dumps( dict(new_name='School is us',
                                                        new_description='We teach',
                                                          new_location = 'Entebbe',
                                                          new_category = "Educate")),
                                   headers=dict(access_token=result['token']))#pragma:no cover
        
        self.assertEqual(response.status_code, 200)#pragma:no cover
        self.assertIn(u'Successfully updated', response.data)#pragma:no cover


    def test_delete_business(self):
        """tests that a business can be deleted"""
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
        
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers = dict(access_token=result['token']))

        response = self.tester.delete('/api/v2/businesses/2', content_type='application/json',
                                   headers=dict(access_token=result['token']))#pragma:no cover
        
        self.assertEqual(response.status_code, 200)#pragma:no cover
        self.assertIn(u'Successfully deleted', response.data)#pragma:no cover

    def test_fail_delete_business(self):
        """tests that a non existent business cannot be deleted"""
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
        
        self.tester.post('/api/v2/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers = dict(access_token=result['token']))

        response = self.tester.delete('/api/v2/businesses/5', content_type='application/json',
                                   headers=dict(access_token=result['token']))#pragma:no cover
        
        self.assertEqual(response.status_code, 401)#pragma:no cover
        self.assertIn(u'Business does not exist', response.data)#pragma:no cover
"""
    #ensure  business can be deleted by user who registered it
    def test_delete_business_by_user_id(self):
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        self.tester.post('/api/v1/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='me@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/v1/auth/login',
                                      content_type='application/json',
                                      data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers = dict(access_token=result['token']))
        self.tester.post('/api/v1/auth/logout',
                         content_type = 'application/json',
                         headers = dict(access_token = result['token']))
        login = self.tester.post('/api/v1/auth/login',
                                 content_type='application/json',
                                 data=json.dumps(dict(email='me@gmail.com',password='amazon')))
        
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers = dict(access_token=result['token']))

        response = self.tester.delete('/api/v1/businesses/Restaurant', content_type='application/json',
                                      headers=dict(access_token=result['token']))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Successfully deleted', response.data)"""

if __name__ == "__main__":
    unittest.main()
