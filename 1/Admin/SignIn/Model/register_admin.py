from SignIn.Misc.Functions.hash import *


class RegisterAdmin:

    def __init__(self, Model):
        self.Model = Model
        self.Database = Model.Database

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
