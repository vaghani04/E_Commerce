from bson import ObjectId

class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        
    def to_dict(self):
        return {
            'name' : self.name,
            'email' : self.email,
            'password' : self.password,
            'role' : self.role
        }
       
        
    