from Teachers.Model.lobby import Lobby
from Teachers.Model.meeting import Meeting
from Teachers.Model.database import Database
from Teachers.Model.list_model import ListModel
from Teachers.Model.table_model import TableModel
from datetime import datetime


class Class:
    def __init__(self, ID, Code, Name, Start, End):
        self.ID = ID
        self.Code = Code
        self.Name = Name
        self._Start = Start
        self._End = End

    def __str__(self):
        return f"Class(ID={self.ID}, Name={self.Name}, Start={self._Start}, End={self._End})"

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
        self.ListModel = ListModel
        self.TableModel = TableModel
        self.Class = Class
        self.Database = Database()

        self.init_lobby()

    def init_lobby(self):
        self.Lobby = Lobby(self)

    def init_meeting(self):
        self.Meeting = Meeting(self)
