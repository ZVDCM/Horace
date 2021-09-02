from Admin.Model.database import Database
from Admin.Model.student_section import StudentSection


class Model:

    class Student:
        def __init__(self, ID, Username, Salt, Hash):
            self.ID = ID
            self.Username = Username
            self.Salt = Salt
            self.Hash = Hash

        def __str__(self):
            return f"Student(ID={self.ID}, Username={self.Username}, Salt={self.Salt}, Hash={self.Hash})"

    class Section:
        def __init__(self, ID, Section):
            self.ID = ID
            self.Section = Section

        def __str__(self):
            return f"Section(ID={self.ID}, Section={self.Username})"

    def __init__(self):
        self.Database = Database()
        self.init_student_section()

    def init_student_section(self):
        self.StudentSection = StudentSection(self)
