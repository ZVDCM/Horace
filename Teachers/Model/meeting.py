class Meeting:

    def __init__(self, Model):
        self.Model = Model
        self.ListModel = Model.ListModel
        self.Database = Model.Database

    def create_attendance(self, teacher, name, file, date):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Attendances WHERE Name=%s"
        cursor.execute(select_query, (name,))

        attendance = cursor.fetchone()

        if attendance:
            update_query = "UPDATE Attendances SET Teacher=%s, File=%s, Date=%s WHERE Name=%s"
            cursor.execute(update_query, (teacher, bytes(file), date, name))
        else:
            insert_query = "INSERT INTO Attendances (Teacher, Name, File, Date) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (teacher, name, bytes(file), date))

        db.commit()

        cursor.close()
        db.close()

        return 'successful'

    def get_blacklisted_urls(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT Domain FROM Urls"
        cursor.execute(select_query)

        urls = cursor.fetchall()

        cursor.close()
        db.close()

        return [url[0] for url in urls]