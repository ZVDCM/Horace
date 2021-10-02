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

        if not username:
            return "Null"

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

    def edit_teacher(self, userid, username, salt, hash, password):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Users WHERE Username=%s"
        cursor.execute(select_query, (username,))

        teacher_exist = cursor.fetchone()
        res = "exists"

        if not teacher_exist:
            if password != str(salt + hash):
                salt = generate_salt()
                hash = get_hashed_password(password, salt)

            update_query = "UPDATE Users SET Username=%s, Salt=%s, Hash=%s WHERE UserID=%s AND Privilege=%s"
            cursor.execute(update_query, (username, salt, hash, userid, "Teacher"))
            db.commit()

            res = 'successful'

        cursor.close()
        db.close()

        return res

    def delete_teacher(self, Teacher):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Users WHERE UserID=%s AND Privilege=%s"
        cursor.execute(delete_query, (Teacher.UserID, 'Teacher'))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

    def delete_many_teachers(self, teachers):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Users WHERE Privilege='Teacher' AND UserID=%s"
        cursor.executemany(delete_query, (teachers))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'