from Admin.Model.database import Database
from Admin.Model.admin import Admin

class Model:

    def __init__(self):
        self.Database = Database()
        self.init_admin()

    def init_admin(self):
        self.Admin = Admin(self)