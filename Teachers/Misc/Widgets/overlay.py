from Teachers.Misc.Functions.relative_path import relative_path
from PyQt5 import QtCore, QtGui, QtWidgets


class Overlay(QtWidgets.QWidget):
    reconnect = QtCore.pyqtSignal()
    disconnect = QtCore.pyqtSignal()
    freeze = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.is_connected = True
        self.setupUi(self)
        self.connect_signals()
        self.reconnect()
        self.hide()

        self.parent.resizeEvent = self.parent_resized
        self.parent.enterEvent = self.entered_parent
        self.parent.leaveEvent = self.left_parent

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(704, 496)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 80)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 482, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_reconnect_disconnect = QtWidgets.QPushButton(Form)
        self.btn_reconnect_disconnect.setMinimumSize(QtCore.QSize(50, 50))
        self.btn_reconnect_disconnect.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_reconnect_disconnect.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_reconnect_disconnect.setObjectName("btn_reconnect_disconnect")
        self.horizontalLayout.addWidget(self.btn_reconnect_disconnect)
        self.btn_freeze = QtWidgets.QPushButton(Form)
        self.btn_freeze.setMinimumSize(QtCore.QSize(50, 50))
        self.btn_freeze.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_freeze.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_freeze.setStyleSheet("""
            QPushButton{
                border-radius: 25px;
                background-color: #eee;
                background-repeat: none;
                background-image: url(%s);
                background-position: center center;
            }
            QPushButton:pressed {
                background-color: #ccc;
            }
        """  % relative_path('Teachers', ['Misc', 'Resources'], 'freeze.png'))
        self.btn_freeze.setObjectName("btn_freeze")
        self.horizontalLayout.addWidget(self.btn_freeze)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        gradient = QtGui.QLinearGradient(QtCore.QPoint(
            self.rect().bottomRight()), QtCore.QPoint(self.rect().topRight()))
        gradient.setColorAt(0.0, QtGui.QColor(0, 0, 0, 100))
        gradient.setColorAt(0.5, QtCore.Qt.transparent)
        gradient.setColorAt(1.0, QtCore.Qt.transparent)

        painter.setBrush(QtGui.QBrush(gradient))
        painter.drawRect(self.rect())

    def parent_resized(self, event):
        width, height = self.parent.frameGeometry(
        ).width(), self.parent.frameGeometry().height()

        self.setGeometry(-1, -1, width, height)

    def entered_parent(self, event):
        self.show()

    def left_parent(self, event):
        self.hide()

    def connect_signals(self):
        self.btn_reconnect_disconnect.clicked.connect(
            self.reconnect_disconnect)

    def reconnect_disconnect(self):
        if self.is_connected:
            self.disconnect()
        else:
            self.reconnect()

    def reconnect(self):
        self.is_connected = True
        self.btn_reconnect_disconnect.setStyleSheet("""
            QPushButton{
                border-radius: 25px;
                background: none;
                background-color: #eee;
                background-repeat: none;
                background-image: url(%s);
                background-position: center center;
            }
            QPushButton:pressed {
                background-color: #ccc;
            }
        """ % relative_path('Teachers', ['Misc', 'Resources'], 'disconnected.png'))

    def disconnect(self):
        self.is_connected = False
        self.btn_reconnect_disconnect.setStyleSheet("""
            QPushButton{
                border-radius: 25px;
                background: none;
                background-color: #eee;
                background-repeat: none;
                background-image: url(%s);
                background-position: center center;
            }
            QPushButton:pressed {
                background-color: #ccc;
            }
        """ % relative_path('Teachers', ['Misc', 'Resources'], 'connected.png'))
