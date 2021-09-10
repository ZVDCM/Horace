class Lobby:

    def __init__(self, Model):
        self.Model = Model
        self.Class = Model.Class
        self.Database = Model.Database

    def get_all_class(self, User):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = """
            SELECT * FROM Classes WHERE Code IN 
            (SELECT Code FROM Class_Teachers WHERE Teacher=%s);
        """
        cursor.execute(select_query, (User.Username,))

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