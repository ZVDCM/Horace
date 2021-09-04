from Admin.Model.database import Database
from Admin.Model.section_student import SectionStudent
from Admin.Model.table_model import TableModel
from Admin.Model.list_model import ListModel


class SectionStudentModel:
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


class SectionModel:
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


class StudentModel:
    def __init__(self, UserID, Username, Salt, Hash):
        self.UserID = UserID
        self.Username = Username
        self.Salt = Salt
        self.Hash = Hash
        self.Section = None

    def __str__(self):
        return f"Student(ID={self.UserID}, Username={self.Username}, Salt={self.Salt}, Hash={self.Hash}, Section={self.Section})"

    @staticmethod
    def get_headers():
        return ("ID", "Username", "Salt", "Hash")

    def get_values(self):
        return (self.UserID, self.Username, self.Salt, self.Hash)


class Model:

    def __init__(self):
        self.TableModel = TableModel
        self.ListModel = ListModel
        self.SectionStudentModel = SectionStudentModel
        self.SectionModel = SectionModel
        self.StudentModel = StudentModel
        self.Database = Database()
        self.init_section_student()

    def init_section_student(self):
        self.SectionStudent = SectionStudent(self)
