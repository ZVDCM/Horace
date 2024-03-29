from SignIn.Model.model import Model 
from SignIn.View.view import View 
from SignIn.Controller.sign_in import SignIn
from SignIn.Controller.register_admin import RegisterAdmin
from SignIn.Controller.forgot_password import ForgotPassword

class Controller:

    def __init__(self):
        self.Model = Model()
        self.View = View()

        self.init_sign_in()
        
    def init_sign_in(self):
        self.SignIn = SignIn(self)

    def init_register_admin(self):
        self.RegisterAdmin = RegisterAdmin(self)

    def init_forgot_password(self):
        self.ForgotPassword = ForgotPassword(self)