from Admin.Model.database import Database
from Admin.Model.section_student import SectionStudent
from Admin.Model.teacher_attendance import TeacherAttendance
from Admin.Model.table_model import TableModel
from Admin.Model.list_model import ListModel


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


class User:
    def __init__(self, UserID, Username, Salt, Hash):
        self.UserID = UserID
        self.Username = Username
        self.Salt = Salt
        self.Hash = Hash

    def __str__(self):
        return f"User(ID={self.UserID}, Username={self.Username}, Salt={self.Salt}, Hash={self.Hash})"

    @staticmethod
    def get_headers():
        return ("ID", "Username", "Salt", "Hash")

    def get_values(self):
        return (self.UserID, self.Username, self.Salt, self.Hash)


class Attendance:

    def __init__(self, ID, Teacher, Name, File, Date):
        self.ID = ID
        self.Teacher = Teacher
        self.Name = Name
        self.File = File
        self.Date = Date

    def __str__(self):
        return f"Attendance(ID={self.ID}, Teacher={self.Teacher}, Name={self.Name}, File={self.File}, Date={self.Date},)"

    @staticmethod
    def get_headers():
        return ("ID", "Teacher", "Name", "File", "Date")

    def get_values(self):
        return (self.ID, self.Teacher, self.Name, self.File, self.Date)

    def get_display(self):
        return self.Name


class Model:

    def __init__(self):
        self.TableModel = TableModel
        self.ListModel = ListModel
        self.SectionStudent = _SectionStudent
        self.Section = Section
        self.Student = User
        self.Teacher = User
        self.Attendance = Attendance
        self.Database = Database()

        self.SectionStudent = SectionStudent(self)
        self.TeacherAttendance = TeacherAttendance(self)
