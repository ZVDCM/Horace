from Teachers.Misc.Widgets.target_student import TargetStudent
from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Functions.relative_path import relative_path

class ChatInput(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.setupUi(self)
        self.targets = []

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(425, 127)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.w_reply = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.w_reply.sizePolicy().hasHeightForWidth())
        self.w_reply.setSizePolicy(sizePolicy)
        self.w_reply.setMaximumSize(QtCore.QSize(16777215, 60))
        self.w_reply.setStyleSheet("")
        self.w_reply.setObjectName("w_reply")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.w_reply)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setSpacing(10)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.sa_targets = QtWidgets.QScrollArea(self.w_reply)
        self.sa_targets.setStyleSheet("QScrollBar:horizontal{\n"
                                        "    height: 12px;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::handle:horizontal{\n"
                                        "    background-color: #97b9f4;    \n"
                                        "    margin-top: 5px;\n"
                                        "    min-width: 5px;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::sub-line:horizontal{\n"
                                        "     height: 0;\n"
                                        "     width: 0;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::add-line:horizontal{\n"
                                        "     height: 0;\n"
                                        "     width: 0;\n"
                                        "}\n"
                                        "\n"
                                        "QScrollBar::add-page:horizontal{\n"
                                        "     background: none;\n"
                                        " }\n"
                                        "\n"
                                        "QScrollBar::sub-page:horizontal{\n"
                                        "     background: none;\n"
                                        "}")
        self.sa_targets.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_targets.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.sa_targets.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.sa_targets.setWidgetResizable(True)
        self.sa_targets.setObjectName("sa_targets")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(
            QtCore.QRect(0, 0, 395, 41))
        self.scrollAreaWidgetContents_4.setObjectName(
            "scrollAreaWidgetContents_4")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(
            self.scrollAreaWidgetContents_4)
        self.horizontalLayout_15.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setSpacing(8)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        spacerItem = QtWidgets.QSpacerItem(
            106, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem)
        self.sa_targets.setWidget(self.scrollAreaWidgetContents_4)
        self.horizontalLayout_12.addWidget(self.sa_targets)
        self.btn_close_reply = QtWidgets.QPushButton(self.w_reply)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_close_reply.sizePolicy().hasHeightForWidth())
        self.btn_close_reply.setSizePolicy(sizePolicy)
        self.btn_close_reply.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_close_reply.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_close_reply.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close_reply.setStyleSheet("QPushButton{\n"
                                            "    border: none;\n"
                                            "    border-radius: none;\n"
                                            "    background: none;\n"
                                            "    background-repeat: none;\n"
                                            f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close.png')});\n"
                                            "    background-position: center center;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "    background: none;\n"
                                            "    background-repeat: none;\n"
                                            f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close_2.png')});\n"
                                            "    background-position: center center;\n"
                                            "}")
        self.btn_close_reply.setObjectName("btn_close_reply")
        self.horizontalLayout_12.addWidget(self.btn_close_reply)
        self.verticalLayout.addWidget(self.w_reply)
       
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setSpacing(6)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.txt_message = QtWidgets.QLineEdit(Form)
        self.txt_message.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_message.setFont(font)
        self.txt_message.setObjectName("txt_message")
        self.verticalLayout_12.addWidget(self.txt_message)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.btn_file = QtWidgets.QPushButton(Form)
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
        self.horizontalLayout_18.addWidget(self.btn_file)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem1)
        self.btn_send = QtWidgets.QPushButton(Form)
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
        self.horizontalLayout_18.addWidget(self.btn_send)
        self.verticalLayout_12.addLayout(self.horizontalLayout_18)
        self.verticalLayout.addLayout(self.verticalLayout_12)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.txt_message.setPlaceholderText(
            _translate("Form", "Type Something..."))

    def hide_targets(self):
        self.targets = []
        for i in range(self.horizontalLayout_15.count()-1):
            self.horizontalLayout_15.itemAt(i).widget().deleteLater()
        self.w_reply.hide()

    def add_student(self, name):
        if self.scrollAreaWidgetContents_4.findChild(QtWidgets.QWidget, name):
            return
        target_student = TargetStudent(self, name)
        target_student.setObjectName(name)
        self.horizontalLayout_15.insertWidget(self.horizontalLayout_15.count()-1,target_student)
        self.targets.append(name)
