from Admin.Misc.Functions.hash import *


class SectionStudent:

    def __init__(self, Model):
        self.Model = Model
        self.SectionStudent = Model.SectionStudent
        self.Section = Model.Section
        self.Student = Model.Student
        self.TableModel = Model.TableModel
        self.ListModel = Model.ListModel
        self.Database = Model.Database

    # Section Student
    def get_all_section_student(self, Section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Section_Students WHERE Section=%s ORDER BY ID DESC"
        cursor.execute(select_query, (Section.Name,))

        section_students = cursor.fetchall()

        cursor.close()
        db.close()

        if section_students:
            return [self.SectionStudent(*section_student) for section_student in section_students]
        return []

    def get_section_student(self, Section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Section_Students WHERE Section=%s"
        cursor.execute(select_query, (Section.Name,))

        section_student = cursor.fetchone()

        cursor.close()
        db.close()

        if section_student:
            return self.SectionStudent(*section_student)
        return ()

    def get_student_section(self, Student):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Section_Students WHERE Student=%s"
        cursor.execute(select_query, (Student.Username,))

        section_student = cursor.fetchone()
        section = None

        if section_student:
            select_query = "SELECT * FROM Sections WHERE Name=%s"
            cursor.execute(select_query, (section_student[1],))
            section = cursor.fetchone()

        cursor.close()
        db.close()

        if section:
            return self.Section(*section)
        return None

    def get_all_unassigned_students(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = """SELECT UserID, Username, Salt, Hash FROM Users WHERE Privilege='Student' AND Username NOT IN (
            SELECT Student FROM Section_Students)"""
        cursor.execute(select_query)

        students = cursor.fetchall()

        cursor.close()
        db.close()

        if students:
            return [self.Student(*student) for student in students]
        return []

    def assign_student_section(self, section_students):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        insert_query = "INSERT INTO Section_Students (Section, Student) VALUES (%s, %s)"
        cursor.executemany(insert_query, (section_students))
        db.commit()

        res = 'successful'

        cursor.close()
        db.close()

        return res

    def delete_section_student(self, section_students):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Section_Students WHERE Section=%s AND Student=%s"
        cursor.executemany(delete_query, (section_students))
        db.commit()

        res = 'successful'

        cursor.close()
        db.close()

        return res

    def remove_all_section_students(self, section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Section_Students WHERE Section=%s"
        cursor.execute(delete_query, (section,))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

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

        select_query = "SELECT * FROM Sections WHERE Name=%s"
        cursor.execute(select_query, (name,))

        section_exists = cursor.fetchone()
        res = "exists"

        if not section_exists:
            insert_query = "INSERT INTO Sections (Name) VALUES (%s)"
            cursor.execute(insert_query, (name,))
            db.commit()

            res = 'successful'

        cursor.close()
        db.close()

        return res

    def edit_section(self, id, section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Sections WHERE Name=%s"
        cursor.execute(select_query, (section,))

        section_exists = cursor.fetchone()
        res = "exists"

        if not section_exists:
            update_query = "UPDATE Sections SET Name=%s WHERE ID=%s"
            cursor.execute(update_query, (section, id))
            db.commit()

            cursor.close()
            db.close()
            res = "successful"

        return res

    def delete_section(self, Section):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Sections WHERE ID=%s"
        cursor.execute(delete_query, (Section.ID,))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

    def delete_many_sections(self, sections):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Sections WHERE ID=%s"
        cursor.executemany(delete_query, (sections))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

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

    def create_student(self, section, username, password):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Users WHERE Username=%s"
        cursor.execute(select_query, (username,))

        student_exist = cursor.fetchone()
        res = "exists"

        if not student_exist:
            select_query = "SELECT * FROM Section_Students WHERE Student=%s"
            cursor.execute(select_query, (username,))

            student_in_section = cursor.fetchone()
            res = "section exists"

            if not student_in_section:
                salt = generate_salt()
                hashed_password = get_hashed_password(password, salt)

                insert_query = "INSERT INTO Users (Username, Privilege, Salt, Hash) VALUES (%s,%s,%s,%s)"
                cursor.execute(
                    insert_query, (username, 'Student', salt, hashed_password))
                db.commit()

                if section:
                    insert_query = "INSERT INTO Section_Students (Section, Student) VALUES (%s,%s)"
                    cursor.execute(insert_query, (section, username))
                    db.commit()

                res = "successful"

        cursor.close()
        db.close()

        return res

    def edit_student(self, userid, username, salt, hash, password):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Users WHERE Username=%s"
        cursor.execute(select_query, (username,))

        student_exist = cursor.fetchone()
        res = "exists"

        if not student_exist:
            if password != str(salt + hash):
                salt = generate_salt()
                hash = get_hashed_password(password, salt)

            update_query = "UPDATE Users SET Username=%s, Salt=%s, Hash=%s WHERE UserID=%s AND Privilege=%s"
            cursor.execute(update_query, (username, salt, hash, userid, "Student"))
            db.commit()

            res = 'successful'

        cursor.close()
        db.close()

        return res

    def delete_student(self, Student):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Users WHERE UserID=%s AND Privilege=%s"
        cursor.execute(delete_query, (Student.UserID, 'Student'))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'
    
    def delete_many_students(self, students):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Users WHERE Privilege='Student' AND UserID=%s"
        cursor.executemany(delete_query, (students))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'