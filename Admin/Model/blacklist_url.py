from Admin.Misc.Functions.hash import *


class BlacklistURL:

    def __init__(self, Model):
        self.Model = Model
        self.Url = Model.Url
        self.TableModel = Model.TableModel
        self.ListModel = Model.ListModel
        self.Database = Model.Database

    def get_all_url(self):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Urls ORDER BY ID"
        cursor.execute(select_query)

        Urls = cursor.fetchall()

        cursor.close()
        db.close()

        if Urls:
            return [self.Url(*url) for url in Urls]
        return []
