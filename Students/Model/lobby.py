class Lobby:

    def __init__(self, Model):
        self.Model = Model
        self.Database = Model.Database
        self.Class = Model.Class

    def get_all_class(self, User):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = """
          SELECT * FROM Classes WHERE Code IN (
            SELECT Code FROM Class_Sections WHERE Section IN (
                SELECT Section From Section_Students WHERE Student=%s
                )
            );
        """
        cursor.execute(select_query, (User.Username,))

        classes = cursor.fetchall()

        cursor.close()
        db.close()

        if classes:
            return [self.Class(*_class) for _class in classes]
        return []