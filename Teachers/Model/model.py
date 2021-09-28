from Teachers.Model.lobby import Lobby
from Teachers.Model.meeting import Meeting
from Teachers.Model.database import Database
from Teachers.Model.list_model import ListModel, ReadOnlyListModel
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


class _SectionStudent:
    def __init__(self, ID, Section, Student):
        self.ID = ID
        self.Section = Section
        self.Student = Student

    def __str__(self):
        return f"SectionStudent(ID={self.ID}, Section={self.Section}, Student={self.Student})"

    @staticmethod
    def get_headers():
        return ("ID", "Section", "Student")

    def get_values(self):
        return (self.ID, self.Section, self.Student)

    def get_display(self):
        return self.Student


class Section:
    def __init__(self, ID, Name):
        self.ID = ID
        self.Name = Name

    def __str__(self):
        return f"Section(ID={self.ID}, Name={self.Name})"

    @staticmethod
    def get_headers():
        return ("ID", "Name")

    def get_values(self):
        return (self.ID, self.Name)


class Model:

    def __init__(self):
        self.Class = Class
        self.Section = Section
        self.SectionStudent = _SectionStudent
        self.ListModel = ListModel
        self.ReadOnlyListModel = ReadOnlyListModel
        self.TableModel = TableModel
        self.Class = Class
        self.Database = Database()

        self.init_lobby()

    def init_lobby(self):
        self.Lobby = Lobby(self)

    def init_meeting(self):
        self.Meeting = Meeting(self)
