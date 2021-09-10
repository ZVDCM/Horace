from Students.Model.database import Database
from Students.Model.lobby import Lobby
from Students.Model.meeting import Meeting
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


class ClassTeacher:
    def __init__(self, ID, Code, Teacher, HostAddress):
        self.ID = ID
        self.Code = Code
        self.Teacher = Teacher
        self.HostAddress = HostAddress

    def __str__(self):
        return f"ClassTeacher(ID={self.ID}, Code={self.Code}, Teacher={self.Teacher}, HostAddress={self.HostAddress})"

    @staticmethod
    def get_headers():
        return ("ID", "Code", "Teacher", "Host Address")

    def get_values(self):
        return (self.ID, self.Code, self.Teacher, self.HostAddress)

    def get_display(self):
        return self.Teacher

class Model:

    def __init__(self):
        self.Class = Class
        self.ClassTeacher = ClassTeacher  
        self.Database = Database()
        self.init_lobby()

    def init_lobby(self):
        self.Lobby = Lobby(self)
    
    def init_meeting(self):
        self.Meeting = Meeting(self)