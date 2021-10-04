from SignIn.Model.model import Model 
from SignIn.View.view import View 
from SignIn.Controller.sign_in import SignIn

class Controller:

    def __init__(self):
        self.Model = Model()
        self.View = View()

        self.init_sign_in()
        
    def init_sign_in(self):
        self.SignIn = SignIn(self)
