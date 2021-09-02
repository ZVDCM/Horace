from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel

class SideNav(QLabel):
    operation = QtCore.pyqtSignal(int)


    def __init__(self, parent, is_active, target_index):
        super().__init__(parent=parent)
        self.parent = parent
        self.is_active = is_active
        self.target_index = target_index

    def mousePressEvent(self, event):
        self.operation.emit(self.target_index)
        super().mousePressEvent(event)

    def activate(self):
        self.is_active = True
        self.setStyleSheet("padding: 10px;\n"
                           "border-left: 5px solid #71A0F8;\n"
                           "background: #256EFF;")

    def deactivate(self):
        self.is_active = False
        self.setStyleSheet("padding: 10px")


