from PyQt5 import QtCore, QtGui, QtWidgets
from win32api import GetSystemMetrics

class Alert(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.items = 0

    def run(self):
        self.raise_()
        self.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(326, 203)
        Form.setMinimumSize(QtCore.QSize(326, 203))
        Form.setMaximumSize(QtCore.QSize(326, 203))
        Form.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool |
                              QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        Form.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def showEvent(self, event):
        screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)
        widget_width, widget_height = self.frameGeometry().width(), self.frameGeometry().height()
        x, y = ((screen_width - widget_width) - 20, (screen_height - widget_height) - 55)
        self.move(QtCore.QPoint(x, y))
        super().showEvent(event)

    def add_item(self, item):
        self.verticalLayout.insertWidget(self.verticalLayout.count(), item)
        self.items += 1
