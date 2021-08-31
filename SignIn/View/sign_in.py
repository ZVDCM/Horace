from PyQt5 import QtCore, QtGui, QtWidgets
from SignIn.Misc.Widgets.title_bar import TitleBar
from SignIn.Misc.Widgets.loading_screen import LoadingScreen
from SignIn.Misc.Widgets.active_overlay import ActiveOverlay
from SignIn.Misc.Widgets.custom_label import ForgotPassword
from SignIn.Misc.Functions.relative_path import relative_path


class SignIn(QtWidgets.QWidget):

    def __init__(self, View, Controller):
        super().__init__()
        self.View = View
        self.Controller = Controller
        self.setupUi(self)
        self.in_username = True
        self.is_admin = False
        self.switch_state()

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)

        self.LoadingScreen = LoadingScreen(self.widget, relative_path('SignIn', ['Misc', 'Resources'], 'loading_squares.gif'))
        self.ActiveOverlay = ActiveOverlay(self)
        
    def run(self):
        self.raise_()
        self.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(337, 455)
        Form.setMinimumSize(QtCore.QSize(337, 455))
        Form.setMaximumSize(QtCore.QSize(337, 455))
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setStyleSheet("QWidget{\n"
                           "    background: #102542; color: white\n"
                           "}\n"
                           "\n"
                           "QLineEdit {\n"
                           "     padding: 1px 5px;\n"
                           "     border: 1px solid #0e4884;\n"
                           "     border-radius: 5px;\n"
                           "}\n"
                           "\n"
                           "QPushButton {\n"
                           "    padding: 5px;\n"
                           "    border: 1px solid #0d3c6e;\n"
                           "    border-radius: 5px;\n"
                           "    background-color: #0d3c6e;\n"
                           "    letter-spacing: 1px\n"
                           "}\n"
                           "\n"
                           "QPushButton#btn_cancel:pressed,\n"
                           "QPushButton:pressed {\n"
                           "    background-color: #083654;\n"
                           "}\n"
                           "\n"
                           "QPushButton#btn_cancel {\n"
                           "      background-color: none;\n"
                           "}\n"
                           "\n"
                           "QLineEdit:focus,\n"
                           "QLineEdit:hover,\n"
                           "QPushButton:focus,\n"
                           "QPushButton:hover{\n"
                           "  border: 1px solid #256eff;\n"
                           "  outline: none;\n"
                           "}")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.title_bar = TitleBar(Form, True)
        self.title_bar.setMinimumSize(QtCore.QSize(0, 30))
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title_bar.setStyleSheet("background: #102542")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_6.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_5.setContentsMargins(25, 25, 25, 25)
        self.verticalLayout_5.setSpacing(25)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.icon = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setStyleSheet("padding-right: 5px")
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap(relative_path("SignIn", ["Misc", "Resources"], "login.png")))
        self.icon.setScaledContents(False)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName("icon")
        self.verticalLayout_4.addWidget(self.icon)
        self.lbl_sign_in = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_sign_in.sizePolicy().hasHeightForWidth())
        self.lbl_sign_in.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow ExtraBold")
        font.setPointSize(22)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lbl_sign_in.setFont(font)
        self.lbl_sign_in.setStyleSheet("letter-spacing: 5px")
        self.lbl_sign_in.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sign_in.setIndent(0)
        self.lbl_sign_in.setObjectName("lbl_sign_in")
        self.verticalLayout_4.addWidget(self.lbl_sign_in)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_tag = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_tag.sizePolicy().hasHeightForWidth())
        self.lbl_tag.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.lbl_tag.setFont(font)
        self.lbl_tag.setIndent(1)
        self.lbl_tag.setObjectName("lbl_tag")
        self.verticalLayout_2.addWidget(self.lbl_tag)
        self.txt_input = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_input.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_input.setFont(font)
        self.txt_input.setObjectName("txt_input")
        self.verticalLayout_2.addWidget(self.txt_input)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.widget1 = QtWidgets.QWidget(self.widget)
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_validation = QtWidgets.QLabel(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_validation.sizePolicy().hasHeightForWidth())
        self.lbl_validation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_validation.setFont(font)
        self.lbl_validation.setStyleSheet("color: #bd2000")
        self.lbl_validation.setIndent(1)
        self.lbl_validation.setObjectName("lbl_validation")
        self.horizontalLayout.addWidget(self.lbl_validation)
        self.lbl_forgot_password = ForgotPassword()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_forgot_password.sizePolicy().hasHeightForWidth())
        self.lbl_forgot_password.setSizePolicy(sizePolicy)
        self.lbl_forgot_password.setMinimumSize(QtCore.QSize(100, 17))
        self.lbl_forgot_password.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_forgot_password.setFont(font)
        self.lbl_forgot_password.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_forgot_password.setIndent(1)
        self.lbl_forgot_password.setObjectName("lbl_forgot_password")
        self.horizontalLayout.addWidget(self.lbl_forgot_password)
        self.verticalLayout_3.addWidget(self.widget1)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_next = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_next.setFont(font)
        self.btn_next.setStyleSheet("padding: 5px;")
        self.btn_next.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_next.setObjectName("btn_next")
        self.verticalLayout.addWidget(self.btn_next)
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setStyleSheet("padding: 5px;")
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setObjectName("btn_cancel")
        self.verticalLayout.addWidget(self.btn_cancel)
        spacerItem = QtWidgets.QSpacerItem(
            20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_6.addWidget(self.widget)

        self.retranslateUi(Form)
        self.lbl_forgot_password.hide()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_sign_in.setText(_translate("Form", "SIGN IN"))
        self.lbl_forgot_password.setText(_translate("Form", "Forgot Password"))
        self.btn_next.setText(_translate("Form", "Next"))
        self.btn_cancel.setText(_translate("Form", "Cancel"))

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.show()
        else:
            self.ActiveOverlay.hide()

    def switch_state(self):
        if len(self.lbl_validation.text()) > 0:
            self.lbl_validation.clear()
            
        if self.in_username:
            self.first_state()
        else:
            self.second_state()

        if self.is_admin:
            self.is_admin = False
            self.lbl_forgot_password.show()
        else:
            self.lbl_forgot_password.hide()

    def invalid_input(self, message):
        self.lbl_validation.setText(message)
        self.lbl_validation.show()

    def first_state(self):
        self.in_username = False
        self.lbl_tag.setText("Username")
        self.txt_input.clear()
        self.txt_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.btn_next.setText("Next")
        self.btn_cancel.hide()

    def second_state(self):
        self.in_username = True
        self.lbl_tag.setText("Password")
        self.txt_input.clear()
        self.txt_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_next.setText("Sign In")
        self.btn_cancel.show()

    def run_loading_screen(self):
        self.LoadingScreen.run()

    def stop_loading_screen(self):
        self.LoadingScreen.hide()