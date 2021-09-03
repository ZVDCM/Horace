from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit

class SearchTarget(QLineEdit):
    operation = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def focusOutEvent(self, event):
        self.operation.emit()
        super().focusOutEvent(event)



