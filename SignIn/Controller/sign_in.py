from Admin.Controller.controller import Controller as AdminController
from Teachers.Controller.controller import Controller as TeacherController
from Students.Controller.controller import Controller as StudentController
from SignIn.Misc.Functions.relative_path import relative_path
from SignIn.Misc.Functions.is_blank import is_blank
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtGui


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
        self.View.txt_input.setText("Admin")
        self.connect_signals()

        self.View.title_bar.title.setText("Horace")

        self.View.run()

    def connect_signals(self):
        self.View.txt_input.returnPressed.connect(self.sign_in)
        self.View.btn_next.clicked.connect(self.sign_in)
        self.View.btn_cancel.clicked.connect(self.View.first_state)

        self.View.lbl_forgot_password.operation.connect(
            self.init_forgot_password)

        self.get_user = Operation(self.Model.get_user)
        self.get_user.started.connect(self.View.LoadingScreen.run)
        self.get_user.operation.connect(self.is_user_admin)

        self.is_match = Validate(self.Model.is_match)
        self.is_match.started.connect(self.View.LoadingScreen.run)
        self.is_match.finished.connect(self.View.LoadingScreen.hide)
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
        self.User = user
        if not self.User:
            self.View.LoadingScreen.hide()
            self.View.invalid_input("Username invalid or non-existent")
            return

        if self.User.Privilege == "Admin":
            self.View.icon.setPixmap(QtGui.QPixmap(relative_path(
                "SignIn", ["Misc", "Resources"], "admin.png")))
            if not self.User.Hash:
                self.init_register_admin()
                return
            self.View.lbl_forgot_password.show()
        elif self.User.Privilege == "Teacher":
            self.View.icon.setPixmap(QtGui.QPixmap(relative_path(
                "SignIn", ["Misc", "Resources"], "teacher.png")))
        elif self.User.Privilege == "Student":
            self.View.icon.setPixmap(QtGui.QPixmap(relative_path(
                "SignIn", ["Misc", "Resources"], "login.png")))

        self.View.second_state()
        self.View.LoadingScreen.hide()
        self.View.txt_input.setText("TestTest!1")

    def input_password(self):
        password = self.View.txt_input.text()
        if is_blank(password):
            self.View.invalid_input("Password must be filled")
            self.View.txt_input.clear()
            return

        if self.User.Privilege == "Admin":
            self.is_match.operation.connect(self.init_admin)
        elif self.User.Privilege == "Teacher":
            self.is_match.operation.connect(self.init_teacher)
        elif self.User.Privilege == "Student":
            self.is_match.operation.connect(self.init_student)

        self.is_match.val = self.User.Salt, self.User.Hash, password
        self.is_match.start()

    def is_not_match(self):
        self.View.invalid_input("Password invalid")

    def init_register_admin(self):
        self.Controller.Model.init_register_admin()
        self.Controller.View.init_register_admin()
        self.Controller.init_register_admin()

    def init_forgot_password(self):
        self.View.LoadingScreen.show()
        self.Controller.Model.init_forgot_password()
        self.Controller.View.init_forgot_password()
        self.Controller.init_forgot_password()

    def init_admin(self):
        self.AdminController = AdminController(self.Controller, self.User)
        self.View.close()

    def init_teacher(self):
        self.TeacherController = TeacherController(self.Controller, self.User)
        self.View.close()

    def init_student(self):
        self.StudentController = StudentController(self.Controller, self.User)
        self.View.close()