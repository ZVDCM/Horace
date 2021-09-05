from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from Admin.Misc.Functions.password import generate_password

class PasswordGenerator(QLineEdit):
    operation = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.selectionChanged.connect(lambda: self.setSelection(0, 0))
        self.operation.connect(self.set_text)
        self.operation.emit()

    def set_text(self):
        self.setText(generate_password())

    def mousePressEvent(self, event):
        self.operation.emit()
        super().mousePressEvent(event)





