
from SignIn.Misc.Functions.relative_path import relative_path
from PyQt5 import QtGui


class ForgotPassword:

    def __init__(self, Controller):
        self.Model = Controller.Model
        self.View = Controller.View.ForgotPassword
        self.Controller = Controller

        self.connect_signals()
        self.View.run()

    def connect_signals(self):
        self.View.btn_reveal_password.clicked.connect(
            self.View.reveal_password)
        self.View.btn_reveal_repeat_password.clicked.connect(
            self.View.reveal_repeat_password)
        self.View.btn_next.clicked.connect(self.increment_page)
        self.View.btn_cancel.clicked.connect(self.View.decrement_page)

        self.View.txt_question_answer_1.returnPressed.connect(
            self.increment_page)
        self.View.txt_question_answer_2.returnPressed.connect(
            self.increment_page)
        self.View.txt_question_answer_3.returnPressed.connect(
            self.increment_page)
        self.View.txt_repeat_password.returnPressed.connect(
            self.increment_page)

    def increment_page(self):
        try:
            current_index = self.View.stackedWidget.currentIndex()
            self.View.hide_validations()


            if current_index == 0:
                self.View.btn_cancel.setText("Back")

            if current_index == 2:
                self.View.show_password_validations()
                self.View.btn_next.setText("Update")

            if current_index == 3:
                if self.View.txt_repeat_password.text() != self.View.txt_password.text():
                    self.View.show_validation(
                        self.View.lbl_repeat_password_validation)
                    return
                if not self.View.is_password_valid:
                    return

                return

            self.View.stackedWidget.setCurrentIndex(current_index+1)
            self.View.dots[current_index+1].setPixmap(QtGui.QPixmap(relative_path(
                "SignIn", ["Misc", "Resources"], "dot2.png")))
        except IndexError:
            return
