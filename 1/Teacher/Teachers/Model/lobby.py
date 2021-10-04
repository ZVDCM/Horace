from Teachers.Misc.Functions.hash import check_password, generate_salt, get_hashed_password

class Lobby:

    def __init__(self, Model):
        self.Model = Model
        self.Class = Model.Class
        self.ListModel = Model.ListModel
        self.TableModel = Model.TableModel
        self.Database = Model.Database

    def get_all_class(self, User):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = """
            SELECT * FROM Classes 
                WHERE Code IN (
                        SELECT Code FROM Class_Teachers WHERE Teacher=%s)
                    AND Start IN (
                        SELECT Start FROM Class_Teachers WHERE Teacher=%s);
        """
        cursor.execute(select_query, (User.Username,User.Username))

        classes = cursor.fetchall()

        cursor.close()
        db.close()

        if classes:
            return [self.Class(*_class) for _class in classes]
        return []

    def set_class_teacher_address(self, address, Class, Teacher):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        update_query = "UPDATE Class_Teachers SET Host_Address=INET_ATON(%s) WHERE Code=%s AND Teacher=%s"
        cursor.execute(update_query, (address, Class.Code, Teacher.Username))
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
            return [attendance[0] for attendance in attendances]
        return []

    def get_attendance_data(self, User, attendance):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT File FROM Attendances WHERE Teacher=%s and Name=%s"
        cursor.execute(select_query, (User.Username, attendance))

        attendance = cursor.fetchone()

        cursor.close()
        db.close()

        if attendance:
            return attendance[0]
        return None

    def update_password(self, username, password):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        salt = generate_salt()
        hashed_password = get_hashed_password(password, salt)

        update_query = "UPDATE Users SET Salt=%s, Hash=%s WHERE Username=%s"
        cursor.execute(update_query, (salt, hashed_password, username))
        db.commit()
        
        cursor.close()
        db.close()
        
        return True

    def is_match(self, salt, _hash, password):
        hashed_password = salt+_hash
        return check_password(password, hashed_password) 