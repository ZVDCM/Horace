from SignIn.Model.database import Database
from SignIn.Misc.Functions.hash import *


class Model:

    class User:
        def __init__(self, ID, Username, Privilege, Salt, Hash):
            self.ID = ID
            self.Username = Username
            self.Privilege = Privilege
            self.Salt = Salt
            self.Hash = Hash

        def __str__(self):
            return f"User(ID={self.ID}, Username={self.Username}, Privilege={self.Privilege}, Salt={self.Salt}, Hash={self.Hash})"

    def __init__(self, Controller):
        self.Controller = Controller
        self.Database = Database()

    def get_user(self, username):
        db = self.Database.connect('horace')
        cursor = db.cursor()

        select_query = 'SELECT * FROM Users WHERE Username=%s'
        cursor.execute(select_query, (username,))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            self.Controller.SignIn.results.put(self.User(*user))
        else:
            self.Controller.SignIn.results.put(None)

    def register_admin(self, password):
        db = self.Database.connect('horace')
        cursor = db.cursor()

        salt = generate_salt()
        hashed_password = get_hashed_password(password, salt)

        insert_query = 'UPDATE Users SET Salt=%s, Hash=%s WHERE Privilege=%s'
        cursor.execute(insert_query, (salt, hashed_password, 'Admin'))
        db.commit()

        cursor.close()
        db.close()

    def register_admin_qna(self, qna):
        db = self.Database.connect('horace')
        cursor = db.cursor()

        for question, answer in qna.items():
            salt = generate_salt()
            hashed_password = get_hashed_password(answer, salt)
            insert_query = 'INSERT INTO security_questions ( Admin, Question, Salt, Hash ) VALUES ( %s, %s, %s, %s )'
            cursor.execute(
                insert_query, ("Admin", question, salt, hashed_password))
            db.commit()

        cursor.close()
        db.close()
