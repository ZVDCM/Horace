from SignIn.Model.database import Database
from SignIn.Model.sign_in import SignIn
from SignIn.Model.register_admin import RegisterAdmin
from SignIn.Model.forgot_password import ForgotPassword
from SignIn.Misc.Functions.hash import *

class User:
        def __init__(self, ID, Username, Privilege, Salt, Hash):
            self.ID = ID
            self.Username = Username
            self.Privilege = Privilege
            self.Salt = Salt
            self.Hash = Hash

        def __str__(self):
            return f"User(ID={self.ID}, Username={self.Username}, Privilege={self.Privilege}, Salt={self.Salt}, Hash={self.Hash})"

class Model:

    def __init__(self):
        self.Database = Database()
        self.User = User
        self.init_sign_in()

    def init_sign_in(self):
        self.SignIn = SignIn(self)

    def init_register_admin(self):
        self.RegisterAdmin = RegisterAdmin(self)
    
    def init_forgot_password(self):
        self.ForgotPassword = ForgotPassword(self)