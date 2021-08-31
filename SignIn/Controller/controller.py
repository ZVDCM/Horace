from SignIn.View.view import View 
from SignIn.Model.model import Model 
from SignIn.Controller.sign_in import SignIn
from SignIn.Controller.register_admin import RegisterAdmin

class Controller:

    def __init__(self):
        self.Model = Model(self)
        self.View = View(self)

        self.init_sign_in()
        
    def init_sign_in(self):
        self.SignIn = SignIn(self)

    def init_register_admin(self):
        self.RegisterAdmin = RegisterAdmin(self)