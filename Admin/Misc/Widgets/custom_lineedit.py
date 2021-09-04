from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from Admin.Misc.Functions.password import generate_password

class PasswordGenerator(QLineEdit):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.selectionChanged.connect(lambda: self.setSelection(0, 0))

    def mousePressEvent(self, event):
        self.setText(generate_password())
        super().mousePressEvent(event)





