
from PyQt5 import QtCore, QtGui, QtWidgets
from Admin.Misc.Functions.relative_path import relative_path
import os


class GeneratedUserPass(QtWidgets.QWidget):

    def __init__(self, parent, controller):
        super().__init__()
        self.parent = parent
        self.controller = controller
        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        Form.setFixedSize(287, 400)
        Form.setStyleSheet("QWidget {\n"
                           "    background: #0B1A30;\n"
                           "    color: white; \n"
                           "    font-family: Barlow\n"
                           "}\n"
                           "")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setStyleSheet("QLineEdit {\n"
                                  "      padding: 1px 5px;\n"
                                  "      border: 1px solid #0e4884;\n"
                                  "      border-radius: 5px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton {\n"
                                  "  padding: 5px;\n"
                                  "  border: 1px solid #0e4884;\n"
                                  "  border-radius: 5px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton::disabled {\n"
                                  "  border: none"
                                  "}\n"
                                  "\n"
                                  "QPushButton:focus,\n"
                                  "QPushButton:hover {\n"
                                  "  border: 1px solid #256eff;\n"
                                  "  outline: none;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed {\n"
                                  "  background-color: #072f49;\n"
                                  "}\n"
                                  "\n"
                                  "QScrollBar:vertical{\n"
                                  "    width: 18px;\n"
                                  "    border-radius: 5px;\n"
                                  "}\n"
                                  "\n"
                                  "QScrollBar::handle:vertical{\n"
                                  "    background-color: #97b9f4;    \n"
                                  "    min-height: 5px;\n"
                                  "    margin-left: 10px;"
                                  "}\n"
                                  "\n"
                                  "QScrollBar::sub-line:vertical{\n"
                                  "     height: 0;\n"
                                  "     width: 0;\n"
                                  "}\n"
                                  "\n"
                                  "QScrollBar::add-line:vertical{\n"
                                  "        height: 0;\n"
                                  "     width: 0;\n"
                                  "}\n"
                                  "\n"
                                  "QScrollBar::add-page:vertical{\n"
                                  "    background: #0b1a30;\n"
                                  "    margin-top: -3px;\n"
                                  " }\n"
                                  "\n"
                                  "QScrollBar::sub-page:vertical{\n"
                                  "      background: #0b1a30;\n"
                                  "    margin-bottom: -3px;\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'download.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'download_2.png')),
                       QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.btn_download = QtWidgets.QPushButton(self.widget)
        self.btn_download.setDisabled(True)
        self.btn_download.setIcon(icon)
        self.btn_download.setIconSize(QtCore.QSize(20, 20))
        self.btn_download.setMinimumSize(QtCore.QSize(33, 33))
        self.btn_download.setMaximumSize(QtCore.QSize(33, 33))
        self.btn_download.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_download.setText("")
        self.btn_download.setObjectName("btn_download")
        self.horizontalLayout.addWidget(self.btn_download)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setStyleSheet("border: none;")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 257, 318))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", "Generated User Passwords"))

    def hideEvent(self, event):
        for i in range(self.verticalLayout_3.count()-2):
            self.verticalLayout_3.removeWidget(
                self.verticalLayout_3.itemAt(i).widget())
        return super().hideEvent(event)

    def connect_signals(self):
        self.btn_download.clicked.connect(self.download_passwords)

    def download_passwords(self):
        password_data = "Username,Password\n"
        for user, _pass in self.parent.temp_passwords.items():
            password_data += f"{user},{_pass}\n"
        path = os.path.join(os.path.expanduser(
            '~/Documents'), "temporary_passwords.csv")
        ext = "csv"
        path = QtWidgets.QFileDialog.getSaveFileName(
            self.parent, 'Save File', path, ext)[0]
        if path:
            self.controller.SignInController.SignIn.show_alert(
                'file', 'Downloading file...')
            with open(path, 'w') as file:
                file.write(password_data)
            self.controller.SignInController.SignIn.show_alert(
                'file', 'File downloaded')

    def input_user_pass(self, user_pass):
        if len(user_pass):
            self.btn_download.setDisabled(False)
        else:
            self.btn_download.setDisabled(True)

        for user, _pass in user_pass.items():
            target = self.scrollAreaWidgetContents.findChild(QtWidgets.QWidget, user+_pass)
            if target:
                continue
            
            widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
            widget.setObjectName(user+_pass)
            vbox = QtWidgets.QVBoxLayout(widget)
            vbox.setContentsMargins(0, 0, 0, 0)
            font = QtGui.QFont()
            font.setFamily("Barlow")
            font.setPointSize(10)
            label = QtWidgets.QLabel(user)
            label.setIndent(0)
            label.setFont(font)
            vbox.addWidget(label)
            lineedit = QtWidgets.QLineEdit(_pass)
            lineedit.setFont(font)
            lineedit.setMinimumSize(QtCore.QSize(0, 30))
            lineedit.setStyleSheet("Background: #081425")
            lineedit.setReadOnly(True)
            vbox.addWidget(lineedit)
            self.verticalLayout_3.insertWidget(0, widget)
