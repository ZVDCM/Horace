from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton


class Button(QPushButton):
    operation = pyqtSignal(int)

    def __init__(self, parent, target_index, is_active, active, inactive, hover):
        super().__init__(parent=parent)
        self.parent = parent
        self.target_index = target_index
        self.active = active
        self.inactive = inactive
        self.hover = hover
        self.is_active = is_active

        if self.is_active:
            self.activate()
        else:
            self.deactivate()

    def enterEvent(self, event):
        if not self.is_active:
            self.setStyleSheet("QPushButton{\n"
                               "    border: none;\n"
                               "    background: none;\n"
                               "    background-repeat: none;\n"
                               f"    background-image: url({self.hover});\n"
                               "    background-position: center center;\n"
                               "}\n")
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_active:
            self.deactivate()
        super().leaveEvent(event)

    def activate(self):
        self.is_active = True
        self.setStyleSheet("QPushButton{\n"
                           "    border: none;\n"
                           "    background: none;\n"
                           "    background-repeat: none;\n"
                           f"    background-image: url({self.active});\n"
                           "    background-position: center center;\n"
                           "}\n")

    def deactivate(self):
        self.is_active = False
        self.setStyleSheet("QPushButton{\n"
                           "    border: none;\n"
                           "    border-radius: none;\n"
                           "    background: none;\n"
                           "    background-repeat: none;\n"
                           f"    background-image: url({self.inactive});\n"
                           "    background-position: center center;\n"
                           "}\n")

    def mousePressEvent(self, event):
        if not self.is_active:
            self.operation.emit(self.target_index)
        super().mousePressEvent(event)
