from Students.Misc.Functions.relative_path import relative_path
from PyQt5 import QtCore, QtGui, QtWidgets
from Students.Misc.Widgets.dialog_title_bar import TitleBar
from Students.Misc.Widgets.active_overlay import ActiveOverlay
from Students.Misc.Widgets.custom_lineedit import AdminPassword
from Students.Misc.Widgets.loading_screen import LoadingScreen
from Students.Misc.Functions.is_blank import is_blank


class Operation(QtCore.QThread):
    operation = QtCore.pyqtSignal()
    validation = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        is_valid = self.fn(*self.val)
        if is_valid:
            self.operation.emit()
        else:
            self.validation.emit()
        self.quit()

class ChangePassword(QtWidgets.QDialog):

    def __init__(self, Lobby, parent, User, Model):
        super().__init__()
        self.Lobby = Lobby
        self.parent = parent
        self.User = User
        self.Model = Model
        self.setupUi(self)

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)
        self.validations = ["Password requirements:\n",
                            "        🗴  Password must be at least 8 characters in length.\n",
                            "        🗸  Password must be no more than 128 characters in length.\n",
                            "        🗴  Password must contain at least 1 english uppercase,\n",
                            "             english lowercase, numbers (0-9), and non-alphanumeric\n",
                            "             characters (!, $, %, etc.)."]
        self.is_password_valid = False

        self.LoadingScreen = LoadingScreen(self.widget_2, relative_path('Teachers', ['Misc', 'Resources'], 'loading_bars.gif'))

        self.title_bar.title.setText("Change Password")
        self.connect_signals()

    def run(self):
        self.activateWindow()
        self.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setFixedSize(QtCore.QSize(494, 200))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                              QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        Dialog.setStyleSheet("QWidget{\n"
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
                             "QPushButton:hover {\n"
                             "      border: 1px solid #256eff;\n"
                             "      outline: none;\n"
                             "}\n"
                             "\n"
                             "QPushButton#btn_reveal_repeat_password,\n"
                             "QPushButton#btn_reveal_new_password,\n"
                             "QPushButton#btn_reveal_old_password{\n"
                             "    border-radius: 0px;\n"
                             "    border-top-right-radius: 5px;\n"
                             "    border-bottom-right-radius: 5px;\n"
                             "}\n"
                             "\n"
                             "QLineEdit#txt_repeat_password,\n"
                             "QLineEdit#txt_new_password,\n"
                             "QLineEdit#txt_old_password{\n"
                             "    border-radius: 0px;\n"
                             "    border-top-left-radius: 5px;\n"
                             "    border-bottom-left-radius: 5px;\n"
                             "}")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.title_bar = TitleBar(Dialog)
        self.title_bar.setStyleSheet("background: #102542")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_3.addWidget(self.title_bar)
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(25, 10, 25, 25)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget_2)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setVerticalSpacing(15)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.lbl_old_password_validation = QtWidgets.QLabel(self.page)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_old_password_validation.sizePolicy().hasHeightForWidth())
        self.lbl_old_password_validation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_old_password_validation.setFont(font)
        self.lbl_old_password_validation.setStyleSheet("color: #bd2000")
        self.lbl_old_password_validation.setTextFormat(
            QtCore.Qt.PlainText)
        self.lbl_old_password_validation.setIndent(1)
        self.lbl_old_password_validation.setObjectName(
            "lbl_old_password_validation")
        self.gridLayout_5.addWidget(
            self.lbl_old_password_validation, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.txt_old_password = QtWidgets.QLineEdit(self.page)
        self.txt_old_password.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_old_password.setFont(font)
        self.txt_old_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_old_password.setObjectName("txt_old_password")
        self.horizontalLayout_5.addWidget(self.txt_old_password)
        self.btn_reveal_old_password = QtWidgets.QPushButton(self.page)
        self.btn_reveal_old_password.setMinimumSize(QtCore.QSize(35, 30))
        self.btn_reveal_old_password.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_reveal_old_password.setFont(font)
        self.btn_reveal_old_password.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_reveal_old_password.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'show.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_reveal_old_password.setIcon(icon)
        self.btn_reveal_old_password.setIconSize(QtCore.QSize(20, 20))
        self.btn_reveal_old_password.setObjectName("btn_reveal_old_password")
        self.horizontalLayout_5.addWidget(self.btn_reveal_old_password)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.page)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setIndent(1)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setIndent(1)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txt_new_password = AdminPassword(self)
        self.txt_new_password.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_new_password.setFont(font)
        self.txt_new_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_new_password.setObjectName("txt_new_password")
        self.horizontalLayout_3.addWidget(self.txt_new_password)
        self.btn_reveal_new_password = QtWidgets.QPushButton(self.page_2)
        self.btn_reveal_new_password.setMinimumSize(QtCore.QSize(35, 30))
        self.btn_reveal_new_password.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_reveal_new_password.setFont(font)
        self.btn_reveal_new_password.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_reveal_new_password.setText("")
        self.btn_reveal_new_password.setIcon(icon)
        self.btn_reveal_new_password.setIconSize(QtCore.QSize(20, 20))
        self.btn_reveal_new_password.setObjectName("btn_reveal_new_password")
        self.horizontalLayout_3.addWidget(self.btn_reveal_new_password)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.lbl_new_password_validation = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_new_password_validation.sizePolicy().hasHeightForWidth())
        self.lbl_new_password_validation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_new_password_validation.setFont(font)
        self.lbl_new_password_validation.setStyleSheet("color: #bd2000")
        self.lbl_new_password_validation.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_new_password_validation.setIndent(1)
        self.lbl_new_password_validation.setObjectName("lbl_new_password_validation")
        self.gridLayout.addWidget(self.lbl_new_password_validation, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.txt_repeat_password = QtWidgets.QLineEdit(self.page_2)
        self.txt_repeat_password.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_repeat_password.setFont(font)
        self.txt_repeat_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_repeat_password.setObjectName("txt_repeat_password")
        self.horizontalLayout_4.addWidget(self.txt_repeat_password)
        self.btn_reveal_repeat_password = QtWidgets.QPushButton(self.page_2)
        self.btn_reveal_repeat_password.setMinimumSize(QtCore.QSize(35, 30))
        self.btn_reveal_repeat_password.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_reveal_repeat_password.setFont(font)
        self.btn_reveal_repeat_password.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_reveal_repeat_password.setText("")
        self.btn_reveal_repeat_password.setIcon(icon)
        self.btn_reveal_repeat_password.setIconSize(QtCore.QSize(20, 20))
        self.btn_reveal_repeat_password.setObjectName(
            "btn_reveal_repeat_password")
        self.horizontalLayout_4.addWidget(self.btn_reveal_repeat_password)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setIndent(1)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.lbl_repeat_password_validation = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_repeat_password_validation.sizePolicy().hasHeightForWidth())
        self.lbl_repeat_password_validation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_repeat_password_validation.setFont(font)
        self.lbl_repeat_password_validation.setStyleSheet("color: #bd2000")
        self.lbl_repeat_password_validation.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_repeat_password_validation.setIndent(1)
        self.lbl_repeat_password_validation.setObjectName(
            "lbl_repeat_password_validation")
        self.gridLayout.addWidget(
            self.lbl_repeat_password_validation, 5, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, 25, 0, 10)
        self.horizontalLayout_2.setSpacing(25)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_cancel = QtWidgets.QPushButton(self.widget_2)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setStyleSheet("padding: 5px;")
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_2.addWidget(self.btn_cancel)
        self.btn_next = QtWidgets.QPushButton(self.widget_2)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_next.setFont(font)
        self.btn_next.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_next.setStyleSheet("padding: 5px;")
        self.btn_next.setObjectName("btn_next")
        self.horizontalLayout_2.addWidget(self.btn_next)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.widget_2)

        self.retranslateUi(Dialog)
        self.stackedWidget.setCurrentIndex(0)
        self.lbl_new_password_validation.hide()
        self.lbl_old_password_validation.hide()
        self.lbl_repeat_password_validation.hide()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_old_password_validation.setText(
            _translate("Dialog", "Password is incorrect"))
        self.label_10.setText(_translate("Dialog", "Old Password"))
        self.label_8.setText(_translate("Dialog", "New Password"))
        self.lbl_new_password_validation.setText(_translate("Dialog", "Password requirements:\n"
                                                        "        🗴  Password must be at least 8 characters in length.\n"
                                                        "        🗸  Password must be no more than 128 characters in length.\n"
                                                        "        🗴  Password must contain at least 1 english uppercase,\n"
                                                        "             english lowercase, numbers (0-9), and non-alphanumeric\n"
                                                        "             characters (!, $, %, etc.)."))
        self.label_9.setText(_translate("Dialog", "Repeat Password"))
        self.lbl_repeat_password_validation.setText(
            _translate("Dialog", "Passwords does not match"))
        self.btn_cancel.setText(_translate("Dialog", "Cancel"))
        self.btn_next.setText(_translate("Dialog", "Next"))

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()
    
    def keyPressEvent(self, event):
        if event.key() == 16777220:
            return
        super().keyPressEvent(event)

    def connect_signals(self):
        self.btn_reveal_old_password.clicked.connect(lambda: self.reveal_password(self.txt_old_password, self.btn_reveal_old_password))
        self.btn_reveal_new_password.clicked.connect(lambda: self.reveal_password(self.txt_new_password, self.btn_reveal_new_password))
        self.btn_reveal_repeat_password.clicked.connect(lambda: self.reveal_password(self.txt_repeat_password, self.btn_reveal_repeat_password))

        self.is_match = Operation(self.Model.is_match)
        self.is_match.started.connect(self.LoadingScreen.show)
        self.is_match.finished.connect(self.LoadingScreen.hide)
        self.is_match.operation.connect(lambda: self.btn_next.setText('Update'))
        self.is_match.operation.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.is_match.operation.connect(self.show_password_validations)
        self.is_match.validation.connect(lambda: self.show_validation(self.lbl_old_password_validation, 'Password is incorrect'))

        self.txt_old_password.returnPressed.connect(self.increment_page)
        self.txt_new_password.returnPressed.connect(lambda: self.txt_repeat_password.setFocus(True) if self.is_password_valid else self.txt_new_password.setFocus(True))
        self.txt_repeat_password.returnPressed.connect(self.increment_page)
        self.btn_next.clicked.connect(self.increment_page)
        self.btn_cancel.clicked.connect(self.close)

        self.update_password = Operation(self.Model.update_password)
        self.update_password.started.connect(self.LoadingScreen.show)
        self.update_password.finished.connect(self.LoadingScreen.hide)
        self.update_password.operation.connect(self.close)
        self.update_password.operation.connect(lambda: self.Lobby.set_lobby_status_handler('Password updated successfully'))

    def reveal_password(self, target_text, target_btn):
        icon = QtGui.QIcon()
        if target_text.echoMode() == QtWidgets.QLineEdit.Password:
            target_text.setEchoMode(QtWidgets.QLineEdit.Normal)
            icon.addPixmap(QtGui.QPixmap(relative_path('SignIn', ['Misc', 'Resources'], 'hide.png')),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            target_text.setEchoMode(QtWidgets.QLineEdit.Password)
            icon.addPixmap(QtGui.QPixmap(relative_path('SignIn', ['Misc', 'Resources'], 'show.png')),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        target_btn.setIcon(icon)
    
    def at_least_8_characters(self):
        self.validations[1] = "        🗸  Password must be at least 8 characters in length.\n"
        self.is_password_valid = True

    def less_than_128_characters(self):
        self.validations[2] = "        🗸  Password must be no more than 128 characters in length.\n"
        self.is_password_valid = True

    def has_1_upper_lower_special(self):
        self.validations[3] = "        🗸  Password must contain at least 1 english uppercase,\n"
        self.is_password_valid = True

    def less_than_8_characters(self):
        self.validations[1] = "        🗴  Password must be at least 8 characters in length.\n"
        self.is_password_valid = False

    def more_than_128_characters(self):
        self.validations[2] = "        🗴  Password must be no more than 128 characters in length.\n"
        self.is_password_valid = False

    def no_1_upper_lower_special(self):
        self.validations[3] = "        🗴  Password must contain at least 1 english uppercase,\n"
        self.is_password_valid = False

    def update_validations(self):
        self.lbl_new_password_validation.setText("".join(self.validations))
    
    def show_password_validations(self):
        if self.lbl_new_password_validation.isHidden():
            self.setFixedSize(494, 444)
        self.lbl_new_password_validation.show()

    def show_validation(self, label, text=None):
        if label.isHidden():
            self.setFixedSize(494, self.height()+40)
        if text:
            label.setText(text)
        label.show()

    def increment_page(self):
        index = self.stackedWidget.currentIndex()
        if index == 0:
            self.valid_old_password()
        elif index == 1:
            self.valid_new_password()
            
    def valid_old_password(self):
        password = self.txt_old_password.text()
        if is_blank(password):
            self.show_validation(self.lbl_old_password_validation, 'Password must be filled')
            return

        self.is_match.val = self.User.Salt, self.User.Hash, password
        self.is_match.start()

    def valid_new_password(self):
        password = self.txt_new_password.text()
        repeat_password = self.txt_repeat_password.text()

        if is_blank(repeat_password):
            self.show_validation(self.lbl_repeat_password_validation, 'Password must be filled')
            return

        if not self.is_password_valid:
            return

        if password != repeat_password:
            self.show_validation(self.lbl_repeat_password_validation, 'Passwords does not match')
            return
        
        self.update_password.val = self.User.Username, repeat_password
        self.update_password.start()