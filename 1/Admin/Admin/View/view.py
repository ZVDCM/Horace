from Admin.View.admin import Admin

class View:

    def __init__(self):
        self.init_admin()

    def init_admin(self):
        self.Admin = Admin(self)
