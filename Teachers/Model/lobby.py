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