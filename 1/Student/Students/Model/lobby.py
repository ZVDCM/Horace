from Students.Misc.Functions.hash import check_password, generate_salt, get_hashed_password


class Lobby:

    def __init__(self, Model):
        self.Model = Model
        self.Database = Model.Database
        self.Class = Model.Class
        self.ClassTeacher = Model.ClassTeacher

    def get_all_class(self, User):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = """
            SELECT * FROM Classes 
                WHERE Code IN (
                    SELECT Code FROM Class_Sections WHERE Section IN (
                        SELECT Section From Section_Students WHERE Student=%s
                        )
                    )
                    AND Start IN (
                        SELECT Start FROM Class_Sections WHERE Section IN (
                            SELECT Section From Section_Students WHERE Student=%s
                        )
                    );
        """
        cursor.execute(select_query, (User.Username, User.Username))

        classes = cursor.fetchall()

        cursor.close()
        db.close()

        if classes:
            return [self.Class(*_class) for _class in classes]
        return []

    def get_class_section_address(self, Class, Student):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = """
            SELECT ID, Code, Teacher, INET_NTOA(Host_Address) FROM class_teachers 
                WHERE Code IN (
                    SELECT Code FROM Class_Sections WHERE Code=%s AND Section IN (
                            SELECT Section From Section_Students WHERE Student=%s
                        )
                )
                    AND Start IN (
                        SELECT Start FROM Class_Sections WHERE Code=%s AND Start=%s AND Section IN (
                            SELECT Section From Section_Students WHERE Student=%s
                        )
                    );
        """
        cursor.execute(select_query, (Class.Code, Student.Username, Class.Code, Class.Raw_Start, Student.Username,))

        _class = cursor.fetchone()

        cursor.close()
        db.close()

        if _class:
            return self.ClassTeacher(*_class)
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