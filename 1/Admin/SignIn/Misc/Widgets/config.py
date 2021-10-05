from PyQt5 import QtCore, QtGui, QtWidgets
from SignIn.Misc.Functions.is_blank import is_blank
from SignIn.Misc.Functions.relative_path import relative_path
from SignIn.Misc.Widgets.dialog_title_bar import TitleBar
from SignIn.Misc.Widgets.active_overlay import ActiveOverlay
from SignIn.Misc.Widgets.loading_screen import LoadingScreen


class Config(QtWidgets.QDialog):
    operation = QtCore.pyqtSignal()

    def __init__(self, parent, db_config):
        super().__init__()
        self.parent = parent
        self.db_config = db_config
        self.setupUi(self)
        self.connect_signals()

        self.title_bar.title.setText('Update config file')

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)

        self.LoadingScreen = LoadingScreen(self.widget, relative_path('SignIn', ['Misc', 'Resources'], 'loading_bars.gif'))

        self.set_fields()

    def run(self):
        self.activateWindow()
        self.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(422, 242)
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        Dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        Dialog.setStyleSheet("QWidget{\n"
                             "    background: #102542;\n"
                             "    color: white; \n"
                             "    font-family: Barlow\n"
                             "}\n"
                             "\n"
                             "QLineEdit {\n"
                             "      padding: 5px;\n"
                             "      border: 1px solid #0e4884;\n"
                             "      border-radius: 5px;\n"
                             "}\n"
                             "\n"
                             "QPushButton {\n"
                             "  padding: 5px 8px;\n"
                             "  border: 1px solid #0e4884;\n"
                             "  background-color: #0e4884;\n"
                             "}\n"
                             "\n"
                             "QPushButton::disabled {\n"
                             "  padding: 5px;\n"
                             " color: gray;\n"
                             "  border: 1px solid #0B1A30;\n"
                             "  background-color: #0B1A30;\n"
                             "}\n"
                             "\n"
                             "QLineEdit:focus,\n"
                             "QLineEdit:hover,\n"
                             "QPushButton:focus,\n"
                             "QPushButton:hover {\n"
                             "  border: 1px solid #256eff;\n"
                             "  outline: none;\n"
                             "}\n"
                             "\n"
                             "QPushButton:pressed {\n"
                             "  background-color: #072f49;\n"
                             "}\n"
                             "")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_bar = TitleBar(self)
        self.title_bar.setMinimumSize(QtCore.QSize(0, 30))
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title_bar.setStyleSheet("")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_2.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(20, 15, 20, 20)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txt_ip = QtWidgets.QLineEdit(self.widget)
        self.txt_ip.setPlaceholderText("127.0.0.1")
        self.txt_ip.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_ip.setObjectName("txt_ip")
        self.gridLayout.addWidget(self.txt_ip, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.txt_port = QtWidgets.QLineEdit(self.widget)
        self.txt_port.setPlaceholderText("3306")
        self.txt_port.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_port.setObjectName("txt_port")
        self.gridLayout.addWidget(self.txt_port, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.txt_username = QtWidgets.QLineEdit(self.widget)
        self.txt_username.setPlaceholderText("root")
        self.txt_username.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_username.setObjectName("txt_username")
        self.gridLayout.addWidget(self.txt_username, 1, 1, 1, 3)
        self.label_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.txt_password = QtWidgets.QLineEdit(self.widget)
        self.txt_password.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password.setObjectName("txt_password")
        self.gridLayout.addWidget(self.txt_password, 2, 1, 1, 3)
        self.gridLayout.setColumnStretch(1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(11)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setStyleSheet(
            "border-radius: 5px;    background-color: none;")
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_update = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(11)
        self.btn_update.setFont(font)
        self.btn_update.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_update.setStyleSheet("border-radius: 5px;")
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout.addWidget(self.btn_update)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Host"))
        self.label_2.setText(_translate("Dialog", ":"))
        self.label_3.setText(_translate("Dialog", "Username"))
        self.label_4.setText(_translate("Dialog", "Password"))
        self.btn_cancel.setText(_translate("Dialog", "Cancel"))
        self.btn_update.setText(_translate("Dialog", "Update"))

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            return
        super().keyPressEvent(event)

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    def connect_signals(self):
        self.btn_update.clicked.connect(self.update_config)
        self.btn_cancel.clicked.connect(self.close)

    def set_fields(self):
        self.txt_ip.setText(self.db_config['host'])
        self.txt_port.setText(self.db_config['port'])
        self.txt_username.setText(self.db_config['user'])
        self.txt_password.setText(self.db_config['password'])

    def update_config(self):
        ip = self.txt_ip.text()
        port = self.txt_port.text()
        username = self.txt_username.text()
        password = self.txt_password.text()

        if is_blank(ip) or is_blank(port) or is_blank(username) or is_blank(password):
            self.parent.run_popup("Config fields must be filled")
            return
        
        config_content = (
            "[client]\n",
            f"host = {ip}\n",
            f"port = {port}\n",
            f"user = {username}\n",
            f"password = {password}\n",
        )
        with open(relative_path('Config', [''], 'admin.ini'), 'w') as config:
            config.writelines(config_content)

        self.operation.emit()


