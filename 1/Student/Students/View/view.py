from Students.View.lobby import Lobby
from Students.View.meeting import Meeting

class View:

    def __init__(self):
        self.init_lobby()

    def init_lobby(self):
        self.Lobby = Lobby(self)
    
    def init_meeting(self):
        self.Meeting = Meeting(self)