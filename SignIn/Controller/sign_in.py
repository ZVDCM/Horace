import queue

from PyQt5.QtCore import QThread
from SignIn.Misc.Functions.is_blank import is_blank

class Operation(QThread):
  
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        self.fn(self.val)


class SignIn:

    def __init__(self, Controller):
        self.Model = Controller.Model
        self.View = Controller.View.SignIn
        self.Controller = Controller

        self.results = queue.Queue()
        self.User = None

        self.connect_signals()
        
        self.View.run()

    def connect_signals(self):
        self.View.txt_input.returnPressed.connect(self.input_username)
        self.View.btn_next.clicked.connect(self.input_username)
        self.View.btn_cancel.clicked.connect(self.View.switch_state)

        self.View.lbl_forgot_password.operation.connect(self.input_password)
        self.get_user = Operation(self.Model.get_user)

    def input_username(self):
        username = self.View.txt_input.text()
        if is_blank(username):
            self.View.invalid_input("Username must be filled")
            self.View.txt_input.clear()
            return

        self.get_user.val = username
        self.get_user.start()
        self.User = self.results.get()
        if not self.User:
            self.View.invalid_input("Username invalid or non-existent")
            return

        if self.User.Username == "Admin":
            if not self.User.Hash:
                self.View.run_loading_screen()
                self.View.txt_input.clear()
                self.Controller.View.init_register_admin()
                self.Controller.init_register_admin()
                return
            self.View.is_admin = True

        self.View.switch_state()

    def input_password(self):
        print(1)

