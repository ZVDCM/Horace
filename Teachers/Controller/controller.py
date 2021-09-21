from Teachers.Model.model import Model
from Teachers.View.view import View
from Teachers.Controller.lobby import Lobby
from Teachers.Controller.meeting import Meeting
from Teachers.Controller.remote_desktop import RemoteDesktop

class Controller:

    def __init__(self, SignInController, User):
        self.SignInController = SignInController
        self.User = User
        self.Model = Model()
        self.View = View()

        self.init_lobby()

    def init_lobby(self):
        self.Lobby = Lobby(self)

    def init_meeting(self, Class):
        self.Meeting = Meeting(self, Class)

    def init_remote_desktop(self, name):
        self.RemoteDesktop = RemoteDesktop(self, name)