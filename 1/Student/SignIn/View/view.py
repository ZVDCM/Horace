from SignIn.View.sign_in import SignIn

class View:

    def __init__(self):
        self.init_sign_in()

    def init_sign_in(self):
        self.SignIn = SignIn(self)
