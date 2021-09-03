from Admin.Model.database import Database
from Admin.Model.section_student import SectionStudent


class Model:

    class Section:
        def __init__(self, ID, Section):
            self.ID = ID
            self.Section = Section

        def __str__(self):
            return f"Section(ID={self.ID}, Section={self.Username})"

    class Student:
        def __init__(self, ID, Username, Salt, Hash):
            self.ID = ID
            self.Username = Username
            self.Salt = Salt
            self.Hash = Hash

        def __str__(self):
            return f"Student(ID={self.ID}, Username={self.Username}, Salt={self.Salt}, Hash={self.Hash})"

    def __init__(self):
        self.Database = Database()
        self.init_section_student()

    def init_section_student(self):
        self.SectionStudent = SectionStudent(self)
