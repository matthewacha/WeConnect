import os
import unittest
import json
from app import app, users
from app.users import views as users
    

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        users.database = []

class TestUserApi(BaseTestCase):
    ################
    ##TEST ClASSES##
    ################
    def test_Users(self):
        user = users.User('james@gmail.com', 'latina' )
        self.assertEqual(user.email,'james@gmail.com' )

    def test_Businesses(self):
        business = users.Business("Fish To Go","We fish", "Kampala", "Foods",1111)
        self.assertEqual(business.name, "Fish To Go")
        new_name = business.change_name("Fishes")
        self.assertEqual(business.name, "Fishes")

    
    ################
    ##TEST SIGN UP##
    ################
    def test_sign_up_user(self):
        response = self.tester.post('/api/auth/register',content_type = 'application/json',
                                   data = json.dumps( dict(email='me@gmail.com',
                                                        password='greater')))
        self.assertIn(u'Successfully signed up', response.data)
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)



        ##############
        ##TEST LOGIN##
        ##############

    def test_incorrect_credential_login_failure(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        response = self.tester.post('/api/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='us@gmail.com',
                                                      password='amazon')))
        self.assertIn(u'Authorize with correct credentials',response.data)
        self.assertEqual(response.status_code, 401)

    def test_correct_credential_login(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        response = self.tester.post('/api/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='you@gmail.com',
                                                        password='lantern')))
        login = self.tester.post('/api/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='you@gmail.com',
                                                      password='lantern')))
        result = json.loads(login.data.decode())
        
        response = self.tester.post('/api/auth/reset-password',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'you@gmail.com',
                                                           old_password = 'lantern',
                                                           new_password = 'laters')),
                                    headers =dict(access_token = result['token'])
                                    )

        self.assertIn(u'Successfully changed password',response.data)
        self.assertEqual(response.status_code, 200)



    def test_logout_user(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        result = json.loads(login.data.decode())

        response = self.tester.post('/api/auth/logout',
                                    content_type = 'application/json',
                                    headers = dict(access_token = result['token']))
        
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'])
        self.assertIn(u'Successfully logged out', response.data)
        self.assertEqual(response.status_code, 200)

    #ensure user_token generated on login
    def test_token_generate(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/auth/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        result = json.loads(login.data.decode())
        self.assertTrue(result['token'])
        self.assertEqual(login.status_code, 200)

        #################
        ##TEST BUSINESS##
        #################

    def test_register_business(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/api/auth/login',
                                 content_type= 'application/json',
                                 data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        
        result = json.loads(login.data.decode())
        response = self.tester.post('/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Fish To Go',
                                                        description='We sell fishy stuff',
                                                          location = 'Kampala',
                                                          category = "Food")),
                                    headers =dict(access_token = result['token']))#pragma:no cover
        data = json.loads(response.data.decode())#pragma:no cover
        self.assertIn(u'Successfully added business',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 200)

    #ensure businesses can be viewed publicly
    def test_view_businesses(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers =dict(access_token=result['token']))
        self.tester.post('/api/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers=dict(access_token=result['token']))
        response = self.tester.get('/api/businesses',
                                  content_type='application/json',
                                   headers=dict(access_token=result['token']))
        

        #data = json.loads(response.data.decode())
        self.assertIn(u'School', response.data)
        self.assertEqual(response.status_code, 200)

    #ensure business Id cannot be viewed
    def test_view_wrong_business(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers =dict(access_token=result['token']))
        self.tester.post('/api/businesses',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate",
                                                          businessId = 123)),
                         headers=dict(access_token=result['token']))
        response = self.tester.get('/api/businesses/123',
                                  content_type='application/json',
                                   headers=dict(access_token=result['token']))
        
        data = json.loads(response.data.decode())
        self.assertIn(u'Id does not exist', response.data)
        self.assertEqual(response.status_code, 200)



    #ensure business can be edited by logged in user
    def test_edit_business(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='Restaurant',
                                                        description='We cook',
                                                          location = 'Kampala',
                                                          category = "Food")),
                         headers = dict(access_token=result['token']))
        
        self.tester.post('/api/businesses',content_type='application/json',
                                   data = json.dumps( dict(name='School',
                                                        description='We teach',
                                                          location = 'Kampala',
                                                          category = "Educate")),
                         headers = dict(access_token=result['token']))

        response = self.tester.put('/api/businesses/School', content_type='application/json',
                                   data = json.dumps( dict(new_name='School is us',
                                                        new_description='We teach',
                                                          new_location = 'Entebbe',
                                                          new_category = "Educate")),
                                   headers=dict(access_token=result['token']))#pragma:no cover
        
        #data = json.loads(response.data.decode())#pragma:no cover
        self.assertEqual(response.status_code, 200)#pragma:no cover
        self.assertIn(u'Successfully edited', response.data)#pragma:no cover

    #ensure reviews can be added for business
    def test_add_review(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        
        response = self.tester.post('/api/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "It's awesome")),
                                    headers = dict(access_token = result['token']))
        #data = json.loads(response.data.decode())
        self.assertIn(u'Successfully added review', response.data)
        self.assertEqual(response.status_code, 200)

    #ensure reviews can be viewed for business
    def test_view_reviews(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/businesses',content_type='application/json',
                         data = json.dumps( dict(name='Restaurant',
                                                 description='We cook',
                                                 location = 'Kampala',
                                                 category = "Food")),
                         headers = dict(access_token=result['token']))
        self.tester.post('/api/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "It's awesome")),
                                    headers = dict(access_token = result['token']))
        self.tester.post('/api/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "Amazing place")),
                                    headers = dict(access_token = result['token']))
        self.tester.post('/api/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(review = "Chef Rico is the best!")),
                                    headers = dict(access_token = result['token']))
        
        response = self.tester.get('/api/businesses/Restaurant/reviews',
                                    content_type = 'application/json',
                                    headers = dict(access_token = result['token']))
        #data = json.loads(response.data.decode())
        self.assertIn(u'Amazing place', response.data)
        self.assertEqual(response.status_code, 200)
"""
    #ensure business can be edited by logged in user
    def test_fail_edit_business(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/auth/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())
        self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='Church',
                                                        description='We pray')),
                         headers =dict(access_token = result))
        self.tester.post('/api/business', content_type='application/json',
                                   data =json.dumps( dict(name='Jumpers',
                                                        description='We rob')),
                         headers =dict(access_token=result))

        response = self.tester.put('/api/business/<name>', content_type='application/json',
                                   data=json.dumps(dict(name='Church',
                                                        new_name='We pray',
                                                        new_description='We raise too')),
                                   headers=dict(access_token=result))
        #data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn(u'"Business cannot be edited', response.data)

    #ensure  business can be deleted by logged in user
    def test_delete_business(self):
        self.tester.post('/api/auth/register',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/api/auth/login',
                                      content_type='application/json',
                                      data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())
        
        self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='baby seat')),
                         headers =dict(access_token=result))
        self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='Bank',
                                                        description='Sell money')),
                         headers =dict(access_token=result))
        response = self.tester.delete('/api/business/<name>', content_type='application/json',
                                   data=json.dumps(dict(name='Banking')),
                                      headers=dict(access_token=result))
        #data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'successfully deleted', response.data)"""


if __name__ == "__main__":
    unittest.main()
