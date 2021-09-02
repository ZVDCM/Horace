from SignIn.Misc.Functions.hash import *

class ForgotPassword:

    def __init__(self, Model):
        self.Model = Model
        self.Database = Model.Database

    def get_qna(self):
        db = self.Database.connect('horace')
        cursor = db.cursor()

        select_query = 'SELECT Question, Salt, Hash FROM Security_Questions'
        cursor.execute(select_query)

        qnas = cursor.fetchall()

        cursor.close()
        db.close()

        if qnas:
            return qnas
        else:
            return None

    def is_match(self, salt, _hash, password):
        hashed_password = salt+_hash
        return check_password(password, hashed_password)

    def update_admin(self, password):
        db = self.Database.connect('horace')
        cursor = db.cursor()

        salt = generate_salt()
        hashed_password = get_hashed_password(password, salt)

        insert_query = 'UPDATE Users SET Salt=%s, Hash=%s WHERE Privilege=%s'
        cursor.execute(insert_query, (salt, hashed_password, 'Admin'))
        db.commit()

        cursor.close()
        db.close()



