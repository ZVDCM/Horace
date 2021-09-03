from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMovie, QPainter


class LoadingScreen(QWidget):

    def __init__(self, parent, photo):
        super().__init__(parent=parent)
        self.parent = parent
        self.setupUi(photo)

    def setupUi(self, photo):
        self.vbox = QHBoxLayout()

        self.lbl_loading = QLabel()
        self.lbl_loading.setStyleSheet("background-color: transparent")
        self.lbl_loading.setAlignment(Qt.AlignCenter)
        sizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_loading.setSizePolicy(sizePolicy)

        self.loading_animation = QMovie(photo)

        self.lbl_loading.setMovie(self.loading_animation)

        self.vbox.addWidget(self.lbl_loading)
        self.setLayout(self.vbox)

        self.hide()

    def run(self):
        self.raise_()
        self.show()

    def showEvent(self, event):
        self.loading_animation.start()
        self.resize_loader()
        self.parent.setEnabled(False)
        super().showEvent(event)

    def hideEvent(self, event):
        self.loading_animation.stop()
        self.parent.setEnabled(True)
        super().hideEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setOpacity(0.7)
        painter.setBrush(Qt.black)
        painter.drawRect(self.rect())

        super().paintEvent(event)

    def resize_loader(self):
        width, height = self.parent.frameGeometry(
        ).width(), self.parent.frameGeometry().height()
        self.setGeometry(-1, -1, width+1, height+1)
