from Admin.Misc.Functions.hash import *


class ClassMember:

    def __init__(self, Model):
        self.Model = Model
        self.Class = Model.Class
        self.TableModel = Model.TableModel
        self.ListModel = Model.ListModel
        self.Database = Model.Database

    def get_all_class(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Classes ORDER BY ID"
        cursor.execute(select_query)

        classes = cursor.fetchall()

        cursor.close()
        db.close()

        if classes:
            return [self.Class(*_class) for _class in classes]
        return []

    def create_class(self, code, name, start, end):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Classes WHERE Code=%s"
        cursor.execute(select_query, (code,))

        class_exist = cursor.fetchone()
        res = "exists"

        if not class_exist:
            insert_query = "INSERT INTO Classes (Code, Name, Start, End) VALUES (%s,%s,%s,%s)"
            cursor.execute(
                insert_query, (code, name, start, end))
            db.commit()

            res = "successful"

        cursor.close()
        db.close()

        return res

    def edit_class(self, id, code, name, start, end):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Classes WHERE Code=%s"
        cursor.execute(select_query, (code,))

        class_exist = cursor.fetchone()
        res = "exists"

        if not class_exist:
            update_query = "UPDATE Classes SET Code=%s, Name=%s, Start=%s, End=%s WHERE ID=%s"
            cursor.execute(update_query, (code, name, start, end, id))
            db.commit()

            res = "successful"

        cursor.close()
        db.close()

        return res

    def delete_class(self, Class):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        delete_query = "DELETE FROM Classes WHERE ID=%s AND Code=%s"
        cursor.execute(delete_query, (Class.ID, Class.Code))
        db.commit()

        cursor.close()
        db.close()

        return 'successful'