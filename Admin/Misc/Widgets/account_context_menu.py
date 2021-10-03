from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Functions.relative_path import relative_path


class AccountContextMenu(QtWidgets.QWidget):
    _create = QtCore.pyqtSignal()
    _load = QtCore.pyqtSignal()
    _change = QtCore.pyqtSignal()
    _sign_out = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.hovering = False
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(230, 190)
        Form.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setStyleSheet("QWidget {\n"
                                  "    background: #0B1A30;\n"
                                  "    color: white; \n"
                                  "    font-family: Barlow\n"
                                  "}\n")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.create = QtWidgets.QWidget(self.widget)
        self.create.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.create.setObjectName("create")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.create)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.create)
        self.label_5.setMinimumSize(QtCore.QSize(22, 22))
        self.label_5.setMaximumSize(QtCore.QSize(22, 22))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'create backup.png')))
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.create)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.verticalLayout.addWidget(self.create)
        self.load = QtWidgets.QWidget(self.widget)
        self.load.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load.setObjectName("load")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.load)
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.load)
        self.label_9.setMinimumSize(QtCore.QSize(22, 22))
        self.label_9.setMaximumSize(QtCore.QSize(22, 22))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'load backup.png')))
        self.label_9.setScaledContents(False)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.load)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)
        self.verticalLayout.addWidget(self.load)
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("color: #083654;")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.change = QtWidgets.QWidget(self.widget)
        self.change.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.change.setObjectName("change")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.change)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.change)
        self.label_7.setMinimumSize(QtCore.QSize(22, 22))
        self.label_7.setMaximumSize(QtCore.QSize(22, 22))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'user_edit.png')))
        self.label_7.setScaledContents(False)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.change)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.verticalLayout.addWidget(self.change)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("color: #083654;")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.signout = QtWidgets.QWidget(self.widget)
        self.signout.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.signout.setObjectName("signout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.signout)
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_11 = QtWidgets.QLabel(self.signout)
        self.label_11.setMinimumSize(QtCore.QSize(22, 22))
        self.label_11.setMaximumSize(QtCore.QSize(22, 22))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'sign_out.png')))
        self.label_11.setScaledContents(False)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.signout)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.verticalLayout.addWidget(self.signout)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("Form", "Create Backup"))
        self.label_10.setText(_translate("Form", "Load Backup"))
        self.label_8.setText(_translate("Form", "Change Password"))
        self.label_12.setText(_translate("Form", "Sign out"))

    def connect_signals(self):
        self.create.mousePressEvent = self.create_pressed
        self.load.mousePressEvent = self.load_pressed
        self.change.mousePressEvent = self.change_pressed
        self.signout.mousePressEvent = self.sign_out_pressed

        self.create.mouseReleaseEvent = lambda e: self.item_released(
            e, self.create)
        self.load.mouseReleaseEvent = lambda e: self.item_released(
            e, self.load)
        self.change.mouseReleaseEvent = lambda e: self.item_released(
            e, self.change)
        self.signout.mouseReleaseEvent = lambda e: self.item_released(
            e, self.signout)

        self.create.enterEvent = lambda e: self.entered_item(
            e, self.create)
        self.load.enterEvent = lambda e: self.entered_item(
            e, self.load)
        self.change.enterEvent = lambda e: self.entered_item(
            e, self.change)
        self.signout.enterEvent = lambda e: self.entered_item(
            e, self.signout)

        self.create.leaveEvent = lambda e: self.left_item(
            e, self.create)
        self.load.leaveEvent = lambda e: self.left_item(
            e, self.load)
        self.change.leaveEvent = lambda e: self.left_item(
            e, self.change)
        self.signout.leaveEvent = lambda e: self.left_item(
            e, self.signout)

    def create_pressed(self, event):
        self.create.setStyleSheet("background: #081222;")
        self._create.emit()
        self.close()

    def load_pressed(self, event):
        self.load.setStyleSheet("background: #081222;")
        self._load.emit()
        self.close()

    def change_pressed(self, event):
        self.change.setStyleSheet("background: #081222;")
        self._change.emit()
        self.close()

    def sign_out_pressed(self, event):
        self.signout.setStyleSheet("background: #081222;")
        self._sign_out.emit()
        self.close()

    def item_released(self, event, item):
        item.setStyleSheet("background: transparent;")
        if self.hovering:
            item.setStyleSheet("background: #06293f;")

    def entered_item(self, event, item):
        self.hovering = True
        item.setStyleSheet("background: #06293f;")

    def left_item(self, event, item):
        self.hovering = False
        item.setStyleSheet("background: transparent;")