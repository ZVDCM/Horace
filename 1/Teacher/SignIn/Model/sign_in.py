from SignIn.Misc.Functions.hash import check_password


class SignIn:

    def __init__(self, Model):
        self.Model = Model
        self.Database = Model.Database

    def get_user(self, username):
        db = self.Database.connect()
        cursor = db.cursor()

        select_query = "SELECT * FROM Users WHERE Username=%s AND Privilege='Teacher'"
        cursor.execute(select_query, (username,))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:
            return self.Model.User(*user)
        return None   

    def is_match(self, salt, _hash, password):
        hashed_password = salt+_hash
        return check_password(password, hashed_password)         