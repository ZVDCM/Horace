from Admin.Misc.Functions.hash import *

class SectionStudent:

    def __init__(self, Model):
        self.Model = Model
        self.SectionStudent = Model.SectionStudentModel
        self.Section = Model.SectionModel
        self.Student = Model.StudentModel
        self.TableModel = Model.TableModel
        self.ListModel = Model.ListModel
        self.Database = Model.Database

    # Section Student
    def get_all_section_student(self, Section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT Student FROM Section_Students WHERE Section=%s ORDER BY ID DESC"
        cursor.execute(select_query, (Section.Name,))

        section_students = cursor.fetchall()

        cursor.close()
        db.close()

        if section_students:
            return [section_student[0] for section_student in section_students]
        return ()

    def get_section_student(self, Section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Section_Students WHERE Section=%s"
        cursor.execute(select_query, (Section.Name,))

        section_student = cursor.fetchone()

        cursor.close()
        db.close()

        if section_student:
            return section_student
        return ()
    
    def get_student_section(self, username):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT Section FROM Section_Students WHERE Student=%s"
        cursor.execute(select_query, (username,))

        student_section = cursor.fetchone()

        cursor.close()
        db.close()

        if student_section:
            return student_section[0]
        return None

    # Section
    def get_all_section(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Sections ORDER BY ID"
        cursor.execute(select_query)

        sections = cursor.fetchall()

        cursor.close()
        db.close()

        if sections:
            return [self.Section(*section) for section in sections]
        return []
    
    def get_section(self, name):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Sections WHERE Name=%s"
        cursor.execute(select_query, (name,))

        section = cursor.fetchone()

        cursor.close()
        db.close()

        if section:
            return self.Section(*section)
        return None

    def create_section(self, name):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        insert_query = "INSERT INTO Sections (Name) VALUES (%s)"
        cursor.execute(insert_query, (name,))
        db.commit()

        cursor.close()
        db.close()

    def edit_section(self, Section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        update_query = "UPDATE Sections SET Name=%s WHERE ID=%s"
        cursor.execute(update_query, (Section.Name, Section.ID))
        db.commit()

        cursor.close()
        db.close()

    def delete_section(self, Section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Sections WHERE ID=%s"
        cursor.execute(delete_query, (Section.ID,))
        db.commit()

        cursor.close()
        db.close()

    # Student
    def get_all_student(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT UserID, Username, Salt, Hash FROM Users WHERE Privilege=%s ORDER BY UserID"
        cursor.execute(select_query, ("Student",))

        students = cursor.fetchall()

        cursor.close()
        db.close()

        if students:
            return [self.Student(*student) for student in students]
        return []
    
    def get_student(self, username):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT UserID, Username, Salt, Hash FROM Users WHERE Privilege=%s AND Username=%s"
        cursor.execute(select_query, ('Student', username))

        student = cursor.fetchone()

        cursor.close()
        db.close()

        if student:
            return self.Student(*student)
        return None

    def create_student(self, username, password):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        salt = generate_salt()
        hashed_password = get_hashed_password(password, salt)

        insert_query = "INSERT INTO Users (Username, Privilege, Salt, Hash) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_query, (username, 'Student', salt, hashed_password))
        db.commit()

        cursor.close()
        db.close()

    def register_student_section(self, section, username):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Section_Students WHERE Student=%s"
        cursor.execute(select_query, (username,))

        student = cursor.fetchone()

        if not student:
            insert_query = "INSERT INTO Section_Students (Section, Student) VALUES (%s,%s)"
            cursor.execute(insert_query, (section, username))
            db.commit()

            res = True
        else:
            res = False

        cursor.close()
        db.close()

        return res

    def edit_student(self, UserID, Username, Salt, Hash, password):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        salt = Salt
        hash = Hash
        if password != str(salt + hash):
            salt = generate_salt()
            hash = get_hashed_password(password, salt)

        update_query = "UPDATE Users SET Username=%s, Salt=%s, Hash=%s WHERE UserID=%s AND Privilege=%s"
        cursor.execute(update_query, (Username, salt, hash, UserID, "Student"))
        db.commit()

        cursor.close()
        db.close()

    def edit_student_section(self, section, username):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        update_query = "UPDATE Section_Students SET Section=%s WHERE Student=%s"
        cursor.execute(update_query, (section, username))
        db.commit()

        cursor.close()
        db.close()

    def delete_student(self, Student):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Users WHERE UserID=%s AND Privilege=%s"
        cursor.execute(delete_query, (Student.UserID, 'Student'))
        db.commit()

        cursor.close()
        db.close()