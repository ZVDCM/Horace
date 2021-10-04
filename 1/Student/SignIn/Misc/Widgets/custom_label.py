from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel

class ForgotPassword(QLabel):
    operation = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QLabel:hover{
                color: #256eff;
            }
        """)

        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def mousePressEvent(self, event):
        self.operation.emit()
        super().mousePressEvent(event)
