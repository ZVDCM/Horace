from Teachers.Model.lobby import Lobby
from Teachers.Model.meeting import Meeting
from Admin.Model.database import Database
from Teachers.Model.database import Database
from datetime import datetime

class Class:
    def __init__(self, ID, Code, Name, HostAddress, Start, End):
        self.ID = ID
        self.Code = Code
        self.Name = Name
        self.HostAddress = HostAddress
        self._Start = Start
        self._End = End

    def __str__(self):
        return f"Class(ID={self.ID}, Name={self.Name}, HostAddress={self.HostAddress}, Start={self._Start}, End={self._End})"

    @property
    def Start(self):
        time = datetime.strptime(str(self._Start), "%H:%M:%S")
        return time.strftime("%I:%M %p")

    @property
    def End(self):
        time = datetime.strptime(str(self._End), "%H:%M:%S")
        return time.strftime("%I:%M %p")

class Model:

    def __init__(self):
        self.Class = Class
        self.Database = Database()

        self.init_lobby()

    def init_lobby(self):
        self.Lobby = Lobby(self)

    def init_meeting(self):
        self.Meeting = Meeting(self)

