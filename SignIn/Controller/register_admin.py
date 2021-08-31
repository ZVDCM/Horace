import queue
from PyQt5.QtCore import QThread
from SignIn.Misc.Functions.relative_path import relative_path
from PyQt5 import QtGui


class Operation(QThread):

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        self.fn(self.val)
        self.quit()


class RegisterAdmin:

    def __init__(self, Controller):
        self.Model = Controller.Model.RegisterAdmin
        self.View = Controller.View.RegisterAdmin
        self.Controller = Controller

        self.results = queue.Queue()

        self.connect_signals()
        self.View.run()

    def connect_signals(self):
        self.View.btn_reveal_password.clicked.connect(
            self.View.reveal_password)
        self.View.btn_reveal_repeat_password.clicked.connect(
            self.View.reveal_repeat_password)
        self.View.btn_next.clicked.connect(self.increment_page)
        self.View.btn_cancel.clicked.connect(self.View.decrement_page)

        self.View.txt_repeat_password.returnPressed.connect(
            self.increment_page)
        self.View.txt_question_answer_2.returnPressed.connect(
            self.increment_page)
        self.View.txt_question_answer_3.returnPressed.connect(
            self.increment_page)
        self.View.txt_question_answer_4.returnPressed.connect(
            self.increment_page)

        self.register_admin = Operation(self.Model.register_admin)
        self.register_admin_qna = Operation(self.Model.register_admin_qna)
        self.register_admin_qna.finished.connect(
            self.Controller.View.SignIn.stop_loading_screen)

    def increment_page(self):
        try:
            current_index = self.View.stackedWidget.currentIndex()

            if not self.View.store_qna(current_index + 1):
                return

            if current_index == 0:
                if self.View.txt_repeat_password.text() != self.View.txt_password.text():
                    self.View.show_validation(
                        self.View.lbl_repeat_password_validation)
                    return
                if not self.View.is_password_valid:
                    return
                self.View.btn_cancel.setText("Back")

            if current_index == 2:
                self.View.btn_next.setText("Sign Up")

            if current_index == 3:
                self.View.is_cancelled = False
                self.View.close()
                self.register_admin.val = self.View.txt_repeat_password.text()
                self.register_admin_qna.val = self.View.question_and_answer
                self.register_admin.start()
                self.register_admin_qna.start()
                return

            self.View.stackedWidget.setCurrentIndex(current_index+1)
            self.View.dots[current_index+1].setPixmap(QtGui.QPixmap(relative_path(
                "SignIn", ["Misc", "Resources"], "dot2.png")))
            self.View.hide_validations()
        except IndexError:
            return
