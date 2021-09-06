from Admin.Misc.Functions.hash import *


class TeacherAttendance:

    def __init__(self, Model):
        self.Model = Model
        self.Teacher = Model.Teacher
        self.Attendance = Model.Attendance
        self.TableModel = Model.TableModel
        self.ListModel = Model.ListModel
        self.Database = Model.Database

    def get_all_teacher(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT UserID, Username, Salt, Hash FROM Users WHERE Privilege=%s ORDER BY UserID"
        cursor.execute(select_query, ("Teacher",))

        teachers = cursor.fetchall()

        cursor.close()
        db.close()

        if teachers:
            return [self.Teacher(*teacher) for teacher in teachers]
        return []

    def create_teacher(self, username, password):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Users WHERE Username=%s"
        cursor.execute(select_query, (username,))

        teacher_exist = cursor.fetchone()
        res = "exists"

        if not teacher_exist:
            salt = generate_salt()
            hashed_password = get_hashed_password(password, salt)

            insert_query = "INSERT INTO Users (Username, Privilege, Salt, Hash) VALUES (%s,%s,%s,%s)"
            cursor.execute(
                insert_query, (username, 'Teacher', salt, hashed_password))
            db.commit()

            res = "successful"

        cursor.close()
        db.close()

        return res
