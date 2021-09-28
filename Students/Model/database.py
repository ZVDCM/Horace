import mysql.connector as mc


class Database:

    def connect(self):
        try:
            return mc.connect(
                user="root",
                password="root123",
                host="192.168.0.100",
                database="Horace"
            )
        except mc.Error as e:
            print(e)
