from Teachers.Misc.Functions.relative_path import relative_path
from Teachers.Misc.Widgets.active_overlay import ActiveOverlay
from Teachers.Misc.Widgets.dialog_title_bar import TitleBar
from Teachers.Misc.Widgets.custom_list_view import ListView
from PyQt5 import QtCore, QtGui, QtWidgets


class MessageTarget(QtWidgets.QDialog):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.targets = []
        self.setupUi(self)
        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)

    def run(self):
        self.activateWindow()
        self.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setMinimumSize(QtCore.QSize(553, 282))
        Dialog.setMaximumSize(QtCore.QSize(553, 282))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                              QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setStyleSheet("background: #102542")
        Dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.title_bar = TitleBar(self)
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_5.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setStyleSheet("QWidget{\n"
                                  "    background: #102542; color: white\n"
                                  "}\n"
                                  "\n"
                                  "QComboBox,\n"
                                  "QLineEdit {\n"
                                  "     padding: 1px 5px;\n"
                                  "     border: 1px solid #0e4884;\n"
                                  "     border-radius: 5px;\n"
                                  "}\n"
                                  "\n"
                                  "QComboBox QAbstractItemView {\n"
                                  "    outline: none;\n"
                                  "}\n"
                                  "\n"
                                  "QComboBox::drop-down {\n"
                                  "      subcontrol-origin: padding;\n"
                                  "     subcontrol-position: top right;\n"
                                  "      border: none;\n"
                                  "}\n"
                                  "\n"
                                  "QComboBox::down-arrow {\n"
                                  "    image: url(:/icons/down.png);\n"
                                  "    padding-right: 5px;\n"
                                  "}\n"
                                  "\n"
                                  "QGroupBox {\n"
                                  "    border: 1px solid #083654;\n"
                                  "    border-radius: 5px;\n"
                                  "    margin-top: 15px;\n"
                                  "}\n"
                                  "\n"
                                  "QGroupBox::title{\n"
                                  "    subcontrol-origin: margin;\n"
                                  "    subcontrol-position: top left;\n"
                                  "    margin-top: 7px;\n"
                                  "    margin-left: 15px;\n"
                                  "    background-color: transparent;\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(20, 10, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lv_target_student = ListView(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lv_target_student.setFont(font)
        self.lv_target_student.setObjectName("lv_target_student")
        self.verticalLayout_2.addWidget(self.lv_target_student)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, 15, -1, -1)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(11)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.txt_message = QtWidgets.QLineEdit(self.widget)
        self.txt_message.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_message.setFont(font)
        self.txt_message.setObjectName("txt_message")
        self.verticalLayout_3.addWidget(self.txt_message)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.btn_file = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_file.sizePolicy().hasHeightForWidth())
        self.btn_file.setSizePolicy(sizePolicy)
        self.btn_file.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_file.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_file.setStyleSheet("QPushButton{\n"
                                      "    border: none;\n"
                                      "    border-radius: none;\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'clip.png')});\n"
                                      "    background-position: center center;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover{\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'clip_2.png')});\n"
                                      "    background-position: center center;\n"
                                      "}")
        self.btn_file.setObjectName("btn_file")
        self.horizontalLayout_17.addWidget(self.btn_file)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem)
        self.btn_send = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_send.sizePolicy().hasHeightForWidth())
        self.btn_send.setSizePolicy(sizePolicy)
        self.btn_send.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_send.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_send.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_send.setStyleSheet("QPushButton{\n"
                                      "    border: none;\n"
                                      "    border-radius: none;\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'send.png')});\n"
                                      "    background-position: center center;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover{\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'send_2.png')});\n"
                                      "    background-position: center center;\n"
                                      "}")
        self.btn_send.setObjectName("btn_send")
        self.horizontalLayout_17.addWidget(self.btn_send)
        self.verticalLayout_3.addLayout(self.horizontalLayout_17)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("color: #083654;")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setEnabled(True)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("Dialog", "Send to:"))
        self.txt_message.setPlaceholderText(
            _translate("Dialog", "Type Something..."))
        self.checkBox.setText(_translate("Dialog", "Popup"))
        self.comboBox.setItemText(0, _translate("Dialog", "Information"))
        self.comboBox.setItemText(1, _translate("Dialog", "Question"))
        self.comboBox.setItemText(2, _translate("Dialog", "Warning"))
        self.comboBox.setItemText(3, _translate("Dialog", "Critical"))

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    def set_model(self, table_model):
        self.lv_target_student.setModel(table_model)
        self.targets = table_model.getData()