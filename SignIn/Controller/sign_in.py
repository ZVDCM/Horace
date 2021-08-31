from SignIn.Misc.Functions.relative_path import relative_path
import queue
from PyQt5 import QtGui

from PyQt5.QtCore import QThread, pyqtSignal
from SignIn.Misc.Functions.is_blank import is_blank


class Operation(QThread):
    operation = pyqtSignal(object)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        result = self.fn(self.val)
        self.operation.emit(result)
        self.quit()

class Validate(QThread):
    operation = pyqtSignal()
    validation = pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        is_valid = self.fn(*self.val)
        if is_valid:
            self.operation.emit()
        else:
            self.validation.emit()
        self.quit()

class SignIn:

    def __init__(self, Controller):
        self.Model = Controller.Model.SignIn
        self.View = Controller.View.SignIn
        self.Controller = Controller

        self.User = None

        self.connect_signals()

        self.View.run()

    def connect_signals(self):
        self.View.txt_input.returnPressed.connect(self.sign_in)
        self.View.btn_next.clicked.connect(self.sign_in)
        self.View.btn_cancel.clicked.connect(self.View.first_state)

        self.View.lbl_forgot_password.operation.connect(
            self.init_forgot_password)

        self.get_user = Operation(self.Model.get_user)
        self.get_user.started.connect(self.View.run_loading_screen)
        self.get_user.operation.connect(self.is_user_admin)

        self.is_match = Validate(self.Model.is_match)
        self.is_match.started.connect(self.View.run_loading_screen)
        self.is_match.finished.connect(self.View.stop_loading_screen)
        self.is_match.operation.connect(self.init_admin)
        self.is_match.validation.connect(self.is_not_match)

    def sign_in(self):
        if len(self.View.lbl_validation.text()) > 0:
            self.View.lbl_validation.clear()

        if self.View.in_username:
            self.input_username()
        else:
            self.input_password()

    def input_username(self):
        username = self.View.txt_input.text()
        if is_blank(username):
            self.View.invalid_input("Username must be filled")
            self.View.txt_input.clear()
            return

        self.get_user.val = username
        self.get_user.start()

    def is_user_admin(self, user):
        self.View.stop_loading_screen()
        self.User = user
        if not self.User:
            self.View.invalid_input("Username invalid or non-existent")
            return

        if self.User.Username == "Admin":
            self.View.icon.setPixmap(QtGui.QPixmap(relative_path(
                "SignIn", ["Misc", "Resources"], "crown.png")))
            if not self.User.Hash:
                self.init_register_admin()
                return
            self.View.lbl_forgot_password.show()
            
        self.View.second_state()

    def init_register_admin(self):
        self.Controller.Model.init_register_admin()
        self.Controller.View.init_register_admin()
        self.Controller.init_register_admin()

    def init_forgot_password(self):
        self.View.run_loading_screen()
        self.Controller.Model.init_forgot_password()
        self.Controller.View.init_forgot_password()
        self.Controller.init_forgot_password()

    def init_admin(self):
        print("Sign In Finished")
        self.View.close()

    def input_password(self):
        password = self.View.txt_input.text()
        if is_blank(password):
            self.View.invalid_input("Password must be filled")
            self.View.txt_input.clear()
            return
        
        self.is_match.val = self.User.Salt, self.User.Hash, password
        self.is_match.start()

    def is_not_match(self):
        self.View.invalid_input("Password invalid")