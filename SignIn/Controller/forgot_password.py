import queue
from PyQt5.QtCore import QThread, pyqtSignal
from SignIn.Misc.Functions.relative_path import relative_path
from SignIn.Misc.Functions.is_blank import is_blank
from PyQt5 import QtGui, QtWidgets, QtCore


class Operation(QThread):

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        self.fn(self.val)
        self.quit()

class GetQnA(QThread):
    operation = pyqtSignal(list)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        result = self.fn()
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

class ForgotPassword:

    def __init__(self, Controller):
        self.Model = Controller.Model.ForgotPassword
        self.View = Controller.View.ForgotPassword
        self.Controller = Controller

        self.questions = None
        self.salts = None
        self.hashes = None

        self.connect_signals()
        self.get_qna.start()
        self.View.run()

    def connect_signals(self):
        self.View.btn_reveal_password.clicked.connect(
            self.View.reveal_password)
        self.View.btn_reveal_repeat_password.clicked.connect(
            self.View.reveal_repeat_password)
        self.View.btn_next.clicked.connect(self.input_answer)
        self.View.btn_cancel.clicked.connect(self.View.decrement_page)

        self.View.txt_question_answer_1.returnPressed.connect(
            self.input_answer)
        self.View.txt_question_answer_2.returnPressed.connect(
            self.input_answer)
        self.View.txt_question_answer_3.returnPressed.connect(
            self.input_answer)
        self.View.txt_repeat_password.returnPressed.connect(
            self.increment_page)

        self.get_qna = GetQnA(self.Model.get_qna)
        self.get_qna.operation.connect(self.set_questions)

        self.is_match = Validate(self.Model.is_match)
        self.is_match.started.connect(self.View.run_loading_screen)
        self.is_match.finished.connect(self.View.stop_loading_screen)
        self.is_match.operation.connect(self.increment_page)
        self.is_match.validation.connect(self.is_not_match)

        self.update_admin = Operation(self.Model.update_admin)
        self.update_admin.finished.connect(
            self.Controller.View.SignIn.stop_loading_screen)
        self.update_admin.finished.connect( lambda: self.Controller.View.SignIn.txt_input.clear())
        self.update_admin.finished.connect( lambda: self.Controller.View.SignIn.switch_state())

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
                repeat_password = self.View.txt_repeat_password.text()
                if repeat_password != self.View.txt_password.text():
                    self.View.show_validation(
                        self.View.lbl_repeat_password_validation)
                    return
                if not self.View.is_password_valid:
                    return
                self.View.is_cancelled = False
                self.View.close()
                self.update_admin.val = repeat_password
                self.update_admin.start()
                return

            self.View.stackedWidget.setCurrentIndex(current_index+1)
            self.View.dots[current_index+1].setPixmap(QtGui.QPixmap(relative_path(
                "SignIn", ["Misc", "Resources"], "dot2.png")))
        except IndexError:
            return

    def input_answer(self):
        try:
            index = self.View.stackedWidget.currentIndex() + 1
            page = self.View.stackedWidget.findChild(QtWidgets.QWidget, f"page_{index}")

            target_txt = page.findChild(QtWidgets.QLineEdit, f"txt_question_answer_{index}")
            answer = target_txt.text()

            if is_blank(answer):
                target_lbl = page.findChild(
                    QtWidgets.QLabel, f"lbl_answer_validation_{index}")
                self.View.show_validation(target_lbl)
                return False

            self.is_match.val = self.salts[index-1], self.hashes[index-1], answer
            self.is_match.start()
        except AttributeError:
            self.increment_page()

    def is_not_match(self):
        index = self.View.stackedWidget.currentIndex() + 1
        page = self.View.stackedWidget.findChild(QtWidgets.QWidget, f"page_{index}")

        target_lbl = page.findChild(QtWidgets.QLabel, f"lbl_answer_validation_{index}")
        self.View.show_validation(target_lbl)

    def set_questions(self, qna):
        question_and_answers = qna
        self.questions = [question_and_answer[0] for question_and_answer in question_and_answers]
        self.salts = [question_and_answer[1] for question_and_answer in question_and_answers]
        self.hashes = [question_and_answer[2] for question_and_answer in question_and_answers]

        for index in range(1, self.View.stackedWidget.count()):
            page = self.View.stackedWidget.findChild(QtWidgets.QWidget, f"page_{index}")
            target_lbl_question = page.findChild(QtWidgets.QLabel, f"lbl_question_{index}")
            target_lbl_question.setText(self.questions[index-1])
            

