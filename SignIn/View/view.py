from SignIn.View.sign_in import SignIn
from SignIn.View.register_admin import RegisterAdmin
from SignIn.View.forgot_password import ForgotPassword

class View:

    def __init__(self):
        self.init_sign_in()

    def init_sign_in(self):
        self.SignIn = SignIn(self)

    def init_register_admin(self):
        self.RegisterAdmin = RegisterAdmin(self)

    def init_forgot_password(self):
        self.ForgotPassword = ForgotPassword(self)
