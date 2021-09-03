from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen


class ActiveOverlay(QWidget):
    resized = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.width, self.height = self.parent.frameGeometry(
        ).width(), self.parent.frameGeometry().height()

        self.is_focused = True

        self.parent.resizeEvent = self.resize
        self.resized.connect(self.resize_loader)

    def showEvent(self, event):
        self.resized.emit()
        super().showEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.is_focused:
            painter.setPen(QPen(QColor("#256eff"), 1, Qt.SolidLine))
        else:
            painter.setPen(QPen(QColor("#0e4177"), 1, Qt.SolidLine))
        painter.drawRect(0, 0, self.width-1, self.height-1)

        super().paintEvent(event)

    @QtCore.pyqtSlot()
    def resize_loader(self):
        self.width, self.height = self.parent.frameGeometry(
        ).width(), self.parent.frameGeometry().height()
        self.setGeometry(0, 0, self.width, self.height)
        self.update()

    def resize(self, _):
        self.resized.emit()
