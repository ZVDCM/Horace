import mysql.connector as mc


class Database:

    def connect(self):
        try:
            return mc.connect(
                user="root",
                password="root123",
                host="127.0.0.1",
                database="Horace"
            )
        except mc.Error as e:
            print(e)
