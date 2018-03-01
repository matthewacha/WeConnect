import random
database = []

def generate_id():
        id = random.uniform(5,500000)
        id *= 100000
        id = int(id)
        return id
def generate_bizId(list):
        count = len(list)
        count += 1
        return count

class User(object):
        def __init__(self, email, password):
                self.email = email
                self.password = password

        def change_password(self, new_password):
                self.password = new_password
               
        def email(self):
                return self.email
        
        def password(self):
                return self.password

class Business(object):
        def __init__(self, name,description, location, category, user_id):
                self.name = name
                self.description = description
                self.location = location
                self.category = category
                self.user_id = user_id

        def change_name(self,new_name):
                self.name = new_name
                
        def change_location(self,new_location):
                self.location = location
                
        def change_category(self,new_category):
                self.category = new_category
