from PyQt5 import QtCore, QtGui, QtWidgets
from Students.Misc.Functions.relative_path import relative_path


class AccountContextMenu(QtWidgets.QWidget):
    password = QtCore.pyqtSignal()
    sign_out = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.hovering = False
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(230, 190)
        Form.setMinimumSize(QtCore.QSize(230, 100))
        Form.setMaximumSize(QtCore.QSize(230, 100))
        Form.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.widget.setStyleSheet("QWidget {\n"
                                  "    background: #0B1A30;\n"
                                  "    color: white; \n"
                                  "    font-family: Barlow\n"
                                  "}\n"
                                  "")
        self.widget.setObjectName("widget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.w_password = QtWidgets.QWidget(self.widget)
        self.w_password.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.w_password.setObjectName('w_password')
        self.verticalLayout.addWidget(self.w_password)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.w_password)
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.w_password)
        self.label_9.setMinimumSize(QtCore.QSize(22, 22))
        self.label_9.setMaximumSize(QtCore.QSize(22, 22))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(relative_path(
            'Students', ['Misc', 'Resources'], 'user_edit.png')))
        self.label_9.setScaledContents(False)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.w_password)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("color: #083654")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.w_sign_out = QtWidgets.QWidget(self.widget)
        self.w_sign_out.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.w_sign_out.setObjectName('w_sign_out')
        self.verticalLayout.addWidget(self.w_sign_out)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.w_sign_out)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.w_sign_out)
        self.label_7.setMinimumSize(QtCore.QSize(22, 22))
        self.label_7.setMaximumSize(QtCore.QSize(22, 22))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(relative_path(
            'Students', ['Misc', 'Resources'], 'sign_out.png')))
        self.label_7.setScaledContents(False)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.w_sign_out)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_10.setText(_translate("Form", "Change Password"))
        self.label_8.setText(_translate("Form", "Sign out"))

    def connect_signals(self):
        self.w_password.mousePressEvent = self.password_pressed
        self.w_sign_out.mousePressEvent = self.sign_out_pressed

        self.w_password.mouseReleaseEvent = lambda e: self.item_released(
            e, self.w_password)
        self.w_sign_out.mouseReleaseEvent = lambda e: self.item_released(
            e, self.w_sign_out)

        self.w_password.enterEvent = lambda e: self.entered_item(
            e, self.w_password)
        self.w_sign_out.enterEvent = lambda e: self.entered_item(
            e, self.w_sign_out)

        self.w_password.leaveEvent = lambda e: self.left_item(
            e, self.w_password)
        self.w_sign_out.leaveEvent = lambda e: self.left_item(
            e, self.w_sign_out)

    def password_pressed(self, event):
        self.w_password.setStyleSheet("background: #081222;")
        self.password.emit()
        self.close()

    def sign_out_pressed(self, event):
        self.w_sign_out.setStyleSheet("background: #081222;")
        self.sign_out.emit()
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
