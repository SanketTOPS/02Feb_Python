class master:
    def signup(self,unm,pas):
        print("Username:",unm)
        print("Password:",pas)
        print("Signup Successfull!")
        
        
    def login(self,unm,pas):
        print("Login Successfull!")

class home(master):
    def signup(self, unm, pas):
        return super().signup(unm, pas)
    
    def login(self, unm, pas):
        return super().login(unm, pas)
    
class about(master):
    def signup(self, unm, pas):
        return super().signup(unm, pas)
    
    def login(self, unm, pas):
        return super().login(unm, pas)