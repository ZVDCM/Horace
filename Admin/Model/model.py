from Admin.Model.database import Database
from Admin.Model.section_student import SectionStudent
from Admin.Model.teacher_attendance import TeacherAttendance
from Admin.Model.blacklist_url import BlacklistURL
from Admin.Model.class_member import ClassMember
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

    @staticmethod
    def get_headers():
        return ("ID", "Code", "Name", "HostAddress", "Start", "End")
    
    @property
    def Start(self):
        return [int(i) for i in str(self._Start).split(':')]

    @property
    def End(self):
        return [int(i) for i in str(self._End).split(':')]

    def get_values(self):
        return (self.ID, self.Code, self.Name, self.HostAddress, self._Start, self._End)

class ClassTeacher:
    def __init__(self, ID, Code, Teacher):
        self.ID = ID
        self.Code = Code
        self.Teacher = Teacher

    def __str__(self):
        return f"ClassTeacher(ID={self.ID}, Code={self.Code}, Teacher={self.Teacher})"

    @staticmethod
    def get_headers():
        return ("ID", "Code", "Teacher")

    def get_values(self):
        return (self.ID, self.Code, self.Teacher)

    def get_display(self):
        return self.Teacher

class ClassSection:
    def __init__(self, ID, Code, Teacher, Section):
        self.ID = ID
        self.Code = Code
        self.Teacher = Teacher
        self.Section = Section

    def __str__(self):
        return f"ClassSection(ID={self.ID}, Code={self.Code}, Teacher={self.Teacher}, Section={self.Section})"

    @staticmethod
    def get_headers():
        return ("ID", "Code", "Teacher", "Section")

    def get_values(self):
        return (self.ID, self.Code, self.Teacher, self.Section)

    def get_display(self):
        return self.Section

class Url:
    def __init__(self, ID, Domain):
        self.ID = ID
        self.Domain = Domain

    def __str__(self):
        return f"URL(ID={self.ID}, Domain={self.Domain})"

    @staticmethod
    def get_headers():
        return ("ID", "Domain")

    def get_values(self):
        return (self.ID, self.Domain)

    def get_display(self):
        return self.Domain

class Model:

    def __init__(self):
        self.TableModel = TableModel
        self.ListModel = ListModel
        self.SectionStudent = _SectionStudent
        self.Section = Section
        self.Student = User
        self.Teacher = User
        self.Attendance = Attendance
        self.Class = Class
        self.ClassTeacher = ClassTeacher
        self.ClassSection = ClassSection
        self.Url = Url
        self.Database = Database()

        self.SectionStudent = SectionStudent(self)
        self.TeacherAttendance = TeacherAttendance(self)
        self.ClassMember = ClassMember(self)
        self.BlacklistURL = BlacklistURL(self)
