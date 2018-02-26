import unittest
import json
from app import app, db
from app.v1 import users
from app.v1.users import views as users
#from app.businesses import views as businesses

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    """Test that a new user can be added"""
    def test_add_user(self):
        response = self.tester.post('/api/v2/auth/register',
                               content_type = 'application/json',
                               data = json.dumps(dict(email = 'me@gmail.com',
                                                 password = 'animal')))
        
        self.assertIn(u'Successfully signed up', response.data)
        self.assertEqual(response.status_code, 200)

    """test that a user can signup with correct credentials"""
    def test_login_with_credentials(self):
        self.tester.post('/api/v2/auth/login',
                    content_type = 'application/json',
                    data = json.dumps(dict(email = 'me@gmail.com',
                                           password = 'animal')))
        response = self.tester.post('/api/v2/auth/login',
                                    content_type = 'application/json',
                                    data = json.dumps(dict(email = 'me@gmail.com',
                                                           password = 'animal')))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
