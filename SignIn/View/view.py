from SignIn.View.sign_in import SignIn
from SignIn.View.register_admin import RegisterAdmin

class View:

    def __init__(self, Controller):
        self.Controller = Controller
        self.init_sign_in()

    def init_sign_in(self):
        self.SignIn = SignIn(self, self.Controller)

    def init_register_admin(self):
        self.RegisterAdmin = RegisterAdmin(self, self.Controller)
