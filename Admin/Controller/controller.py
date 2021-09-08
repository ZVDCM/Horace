from Admin.Model.model import Model
from Admin.View.view import View
from Admin.Controller.admin import Admin

class Controller:

    def __init__(self, SignInController, User):
        self.SignInController = SignInController
        self.User = User
        self.Model = Model()
        self.View = View()

        self.init_admin()

    def init_admin(self):
        self.Admin = Admin(self)