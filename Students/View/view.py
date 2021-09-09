from Students.View.lobby import Lobby

class View:

    def __init__(self):
        self.init_lobby()

    def init_lobby(self):
        self.Lobby = Lobby(self)