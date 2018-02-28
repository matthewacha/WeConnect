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
    ################
    ##TEST ClASSES##
    ################
    def test_Users(self):
        user = User('james@gmail.com', 'latina' )
        self.assertEqual(user.email,'james@gmail.com' )

    def test_Businesses(self):
        business = Business("Fish To Go","We fish", "Kampala", "Foods",1111)
        self.assertEqual(business.name, "Fish To Go")
        new_name = business.change_name("Fishes")
        self.assertEqual(business.name, "Fishes")

    
    ################
    ##TEST SIGN UP##
    ################
    def test_sign_up_user(self):
        response = self.tester.post('/api/v1/auth/register',content_type = 'application/json',
                                   data = json.dumps( dict(email='mem@gmail.com',
                                                        password='greater')))
        self.assertIn(u'Successfully signed up', response.data)
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)


        #################
        ##TEST BUSINESS##
        #################

    def test_register_business(self):
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
        #data = json.loads(response.data.decode())#pragma:no cover
        self.assertIn(u'Successfully added business',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 200)

    #ensure businesses can be viewed publicly
    def test_view_businesses(self):
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
        

        #data = json.loads(response.data.decode())
        self.assertIn(u'School', response.data)
        self.assertEqual(response.status_code, 200)

    #ensure business Id cannot be viewed
    def test_view_wrong_business(self):
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



    #ensure business can be edited by logged in user
    def test_edit_business(self):
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
        
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers = dict(access_token=result['token']))

        response = self.tester.put('/api/v1/businesses/School', content_type='application/json',
                                   data = json.dumps( dict(new_name='School is us',
                                                        new_description='We teach',
                                                          new_location = 'Entebbe',
                                                          new_category = "Educate")),
                                   headers=dict(access_token=result['token']))#pragma:no cover
        
        self.assertEqual(response.status_code, 200)#pragma:no cover
        self.assertIn(u'Successfully edited', response.data)#pragma:no cover

    ##ensure  business can be deleted by user who registered it
    def test_fail_edit_business(self):
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
        
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers = dict(access_token=result['token']))

        response = self.tester.put('/api/v1/businesses/Minimart', content_type='application/json',
                                   data = json.dumps( dict(new_name='School is us',
                                                        new_description='We teach',
                                                          new_location = 'Entebbe',
                                                          new_category = "Educate")),
                                   headers=dict(access_token=result['token']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'"Business does not exist', response.data)



    #ensure business can be deleted by logged in user
    def test_delete_business(self):
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
        
        self.tester.post('/api/v1/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers = dict(access_token=result['token']))

        response = self.tester.delete('/api/v1/businesses/School', content_type='application/json',
                                   headers=dict(access_token=result['token']))#pragma:no cover
        
        #data = json.loads(response.data.decode())#pragma:no cover
        self.assertEqual(response.status_code, 200)#pragma:no cover
        self.assertIn(u'Successfully deleted', response.data)#pragma:no cover

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
        self.assertIn(u'Successfully deleted', response.data)

if __name__ == "__main__":
    unittest.main()
