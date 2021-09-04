from Admin.Model.database import Database
from Admin.Model.section_student import SectionStudent
from Admin.Model.table_model import TableModel


class Model:

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

    class Student:
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

    def __init__(self):
        self.TableModel = TableModel
        self.Database = Database()
        self.init_section_student()

    def init_section_student(self):
        self.SectionStudent = SectionStudent(self)
