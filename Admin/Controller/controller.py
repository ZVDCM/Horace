from Admin.Model.model import Model
from Admin.View.view import View
from Admin.Controller.admin import Admin

class Controller:

    def __init__(self, SignInController):
        self.SignInController = SignInController
        self.Model = Model()
        self.View = View()

        self.init_admin()

    def init_admin(self):
        self.Admin = Admin(self)