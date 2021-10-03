import os
import mysql.connector as mc


class Database:

    def connect(self):
        try:
            return mc.connect(
                user="root",
                host="127.0.0.1",
                database="Horace"
            )
        except mc.Error as e:
            print(e)

    def load_backup(self, path):
        db = self.connect()
        cursor = db.cursor()
        
        admin = self.get_admin()
        security_questions = self.get_admin_security_questions()

        cursor.close()
        db.close()

        self.drop_database()

        os.system(f'mysql -u root Horace < {path}')

        self.set_admin(admin, security_questions)

    def drop_database(self):
        db = mc.connect(
                user="root",
                host="127.0.0.1"
        )
        cursor = db.cursor()

        sql_query = """
                DROP DATABASE Horace;
                CREATE DATABASE Horace;
                """
        cursor.execute(sql_query)
        
        cursor.close()
        db.close()

    def get_admin(self):
        db = self.connect()
        cursor = db.cursor()

        select_query = "SELECT Username, Privilege, Salt, Hash FROM Users WHERE Privilege='Admin'"
        cursor.execute(select_query)

        admin = cursor.fetchone()

        cursor.close()
        db.close()

        return admin

    def get_admin_security_questions(self):
        db = self.connect()
        cursor = db.cursor()

        select_query = "SELECT Admin, Question, Salt, Hash FROM Security_Questions"
        cursor.execute(select_query)

        security_questions = cursor.fetchall()

        cursor.close()
        db.close()

        return security_questions

    def set_admin(self, admin, security_questions):
        db = self.connect()
        cursor = db.cursor()

        insert_query = "INSERT INTO Users (Username, Privilege, Salt, Hash) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_query, (*admin,))
        db.commit()

        cursor.close()
        db.close()

        self.set_admin_security_questions(security_questions)

    def set_admin_security_questions(self, security_questions):
        db = self.connect()
        cursor = db.cursor()

        insert_query = "INSERT INTO Security_Questions (Admin, Question, Salt, Hash) VALUES (%s,%s,%s,%s)"
        cursor.executemany(insert_query, (security_questions))
        db.commit()

        cursor.close()
        db.close()

   