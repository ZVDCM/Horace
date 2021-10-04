from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPainter, QPen


class BadgeOverlay(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setGeometry(self.parent.geometry())
        self.initUi()
        self.hide()
        self.connect_signals()

    def initUi(self):
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0,0,0,0)
        self.horizontal_layout.setSpacing(0)
        
        self.label = QLabel('0', self)
        font = QFont()
        font.setFamily("Barlow SemiBold")
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setMinimumSize(16,16)
        self.label.setMaximumSize(16,16)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('background: #256eff; border-radius: 8px; padding-bottom: 2px')
        self.horizontal_layout.addWidget(self.label, alignment=Qt.AlignTop | Qt.AlignRight)

    def connect_signals(self):
        self.label.hideEvent = self.label_hid

    def label_hid(self, event):
        self.label.setText('0')
        super(QLabel, self.label).hideEvent(event)

    def increment(self):
        if self.parent.is_active:
            return
        self.show()
        num = int(self.label.text())
        num += 1
        self.label.setText(str(num)) 
