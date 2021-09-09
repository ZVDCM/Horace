from Students.View.lobby import Lobby
from Students.Model.model import Model
from Students.View.view import View
from Students.Controller.lobby import Lobby

class Controller:

    def __init__(self, SignInController, User):
        self.SignInController = SignInController
        self.User = User
        self.Model = Model()
        self.View = View()

        self.init_lobby()

    def init_lobby(self):
        self.Lobby = Lobby(self)