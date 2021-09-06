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