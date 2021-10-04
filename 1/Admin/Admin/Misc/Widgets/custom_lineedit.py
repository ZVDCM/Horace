from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from Admin.Misc.Functions.password import generate_password
from string import punctuation
from re import search

class PasswordGenerator(QLineEdit):
    operation = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.operation.connect(self.set_text)
        self.operation.emit()

    def set_text(self):
        self.setText(generate_password())

    def mousePressEvent(self, event):
        self.operation.emit()
        super().mousePressEvent(event)

class AdminPassword(QLineEdit):
    regex = "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[%s])[A-Za-z\d%s]+$" % (
        punctuation, punctuation)

    at_least_8_characters = pyqtSignal()
    less_than_128_characters = pyqtSignal()
    has_1_upper_lower_special = pyqtSignal()

    less_than_8_characters = pyqtSignal()
    more_than_128_characters = pyqtSignal()
    no_1_upper_lower_special = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.at_least_8_characters.connect(self.parent.at_least_8_characters)
        self.less_than_128_characters.connect(
            self.parent.less_than_128_characters)
        self.has_1_upper_lower_special.connect(
            self.parent.has_1_upper_lower_special)

        self.less_than_8_characters.connect(self.parent.less_than_8_characters)
        self.more_than_128_characters.connect(
            self.parent.more_than_128_characters)
        self.no_1_upper_lower_special.connect(
            self.parent.no_1_upper_lower_special)

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.parent.txt_repeat_password.setFocus(True)

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        password = self.text()

        if len(password) >= 8:
            self.at_least_8_characters.emit()
        else:
            self.less_than_8_characters.emit()
            self.parent.show_password_validations()

        if len(password) <= 128:
            self.less_than_128_characters.emit()
        else:
            self.more_than_128_characters.emit()
            self.parent.show_password_validations()

        if search(self.regex, password):
            self.has_1_upper_lower_special.emit()
        else:
            self.no_1_upper_lower_special.emit()
            self.parent.show_password_validations()

        self.parent.update_validations()

        super().keyReleaseEvent(event)






