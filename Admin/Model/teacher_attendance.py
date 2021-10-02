from Admin.Misc.Functions.hash import *
import mysql

class TeacherAttendance:

    def __init__(self, Model):
        self.Model = Model
        self.Teacher = Model.Teacher
        self.Attendance = Model.Attendance
        self.TableModel = Model.TableModel
        self.ListModel = Model.ListModel
        self.Database = Model.Database

    def import_teacher_table(self, teachers):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        try:
            insert_query = "INSERT INTO Users (Username, Privilege, Salt, Hash) VALUES (%s,%s,%s,%s)"
            cursor.executemany(insert_query, (teachers))
            db.commit()
            res = 'successful'
        except mysql.connector.errors.ProgrammingError:
            res = 'programming error'
        except mysql.connector.errors.InterfaceError:
            res = 'programming error'
        except mysql.connector.errors.IntegrityError:
            res = 'integrity error'

        cursor.close()
        db.close()

        return res

    def export_teacher_table(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Users WHERE Privilege='Teacher'"
        cursor.execute(select_query)
        teachers = cursor.fetchall()

        cursor.close()
        db.close()

        return [teachers]

    def clear_teacher_table(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Users WHERE Privilege='Teacher'"
        cursor.execute(delete_query)
        db.commit()

        res = 'successful'

        cursor.close()
        db.close()

        return res

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

    def get_all_attendances(self, User):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT Name FROM Attendances WHERE Teacher=%s"
        cursor.execute(select_query, (User.Username,))

        attendances = cursor.fetchall()

        cursor.close()
        db.close()

        if attendances:
            return [self.Attendance(*attendance) for attendance in attendances]
        return []
    
    def delete_teacher_attendances(self, attendances):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Attendances WHERE Name=%s"
        cursor.executemany(delete_query, (attendances))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'

    def clear_teacher_attendances(self, teacher):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Attendances WHERE Teacher=%s"
        cursor.execute(delete_query, (teacher,))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'