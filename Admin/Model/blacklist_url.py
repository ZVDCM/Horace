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

    def create_url(self, domain):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Urls WHERE Domain=%s"
        cursor.execute(select_query, (domain,))

        domain_exist = cursor.fetchone()
        res = "exists"

        if not domain_exist:
            insert_query = "INSERT INTO Urls (Domain) VALUES (%s)"
            cursor.execute(
                insert_query, (domain,))
            db.commit()

            res = "successful"

        cursor.close()
        db.close()

        return res

    def edit_url(self, prev_domain, domain):
        db = self.Database.connect()
        cursor = db.cursor(buffered=True)

        select_query = "SELECT * FROM Urls WHERE Domain=%s"
        cursor.execute(select_query, (domain,))

        domain_exist = cursor.fetchone()
        res = "exists"

        if not domain_exist:
            update_query = "UPDATE Urls SET Domain=%s WHERE Domain=%s"
            cursor.execute(update_query, (domain, prev_domain))
            db.commit()

            res = "successful"

        cursor.close()
        db.close()

        return res