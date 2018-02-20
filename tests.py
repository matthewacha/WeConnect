import os
import unittest
import json
from app import app, users


    

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        users.database = []

class TestUserApi(BaseTestCase):
    ###TEST SIGN UP###
    
    def test_sign_up_user(self):
        response = self.tester.post('/api/user',content_type = 'application/json',
                                   data = json.dumps( dict(email='me@gmail.com',
                                                        password='greater')))
        self.assertIn(u'Successfully signed up', response.data)
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
        self.assertIn(u'Authorize with correct password',response.data)
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

    #ensure user_token generated on login
    def test_token_generate(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='laters')))
        response = self.tester.post('/login',
                                    content_type='application/json',
                                   data=json.dumps(dict(email='jh@gmail.com',
                                                      password='laters')))
        data = json.loads(response.data.decode())
        self.assertTrue(data['token'])
        self.assertEqual(response.status_code, 200)

        #################
        ##TEST BUSINESS##
        #################

    def test_register_business(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(email='jh@gmail.com',
                                                        password='amazons')))
        login = self.tester.post('/login',
                                 content_type= 'application/json',
                                 data=json.dumps(dict(email='jh@gmail.com',
                                                      password='amazons')))
        
        result = json.loads(login.data.decode())
        response = self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='Fish To Go',
                                                        description='We sell fishy stuff')),
                                    headers =dict(a_access_token = result))#pragma:no cover
        #data = json.loads(response.data.decode())#pragma:no cover
        self.assertIn(u'Successfully added business',response.data)#pragma:no cover
        self.assertEqual(response.status_code, 200)

    #ensure businesses can be viewed publicly
    def test_view_businesses(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))

        result = json.loads(user_login.data.decode())
        self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook')),
                         headers =dict(access_token=result))
        self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach')),
                         headers=dict(access_token=result))
        response = self.tester.get('/api/business',
                                  content_type='application/json')
        #data = json.loads(response.data.decode())
        self.assertIn(u'School', response.data)
        self.assertEqual(response.status_code, 200)

    #ensure single business can be viewed
    def test_view_single_business(self):
        self.tester.post('/api/user',content_type='application/json',
                                   data =json.dumps( dict(
                                                        email='jh@gmail.com',
                                                        password='amazon')))
        user_login = self.tester.post('/login',content_type='application/json',
                         data=json.dumps(dict(email='jh@gmail.com',password='amazon')))
        result = json.loads(user_login.data.decode())
        self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='School',
                                                        description='We teach')),
                         headers =dict(access_token=result))
        self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='Restaurant',
                                                        description='We cook')),
                         headers =dict(access_token=result))
        self.tester.post('/api/business',content_type='application/json',
                                   data =json.dumps( dict(name='Bookshop',
                                                        description='We read')),
                         headers =dict(access_token=result))
        response = self.tester.get('/api/recipe/<name>',
                                   content_type='application/json',
                                   data = json.dumps(dict(name='School')))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'We teach', response.data)


if __name__ == "__main__":
    unittest.main()
