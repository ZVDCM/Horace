from Teachers.Misc.Functions.relative_path import relative_path
from PyQt5 import QtWidgets, QtCore, QtGui


class TargetStudent(QtWidgets.QWidget):

    def __init__(self, parent, name):
        super().__init__(parent=parent)
        self.parent = parent
        self.name = name
        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, Form):
        Form.setMaximumSize(QtCore.QSize(16777215, 40))
        Form.setObjectName("Form")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setSpacing(0)

        self.widget = QtWidgets.QWidget()
        self.widget.setStyleSheet("background: #072f49")
        self.horizontalLayout.addWidget(self.widget)

        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_16.setSpacing(8)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_16.addWidget(self.label_4)
        self.btn_close_target = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_close_target.sizePolicy().hasHeightForWidth())
        self.btn_close_target.setSizePolicy(sizePolicy)
        self.btn_close_target.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_close_target.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_close_target.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close_target.setStyleSheet("QPushButton{\n"
                                            "    border: none;\n"
                                            "    border-radius: none;\n"
                                            "    background: none;\n"
                                            "    background-repeat: none;\n"
                                            f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close_small.png')});\n"
                                            "    background-position: center center;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "    background: none;\n"
                                            "    background-repeat: none;\n"
                                            f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close_small_2.png')});\n"
                                            "    background-position: center center;\n"
                                            "}")
        self.btn_close_target.setObjectName("btn_close_target")
        self.horizontalLayout_16.addWidget(self.btn_close_target)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_4.setText(_translate("Form", self.name))

    def connect_signals(self):
        self.btn_close_target.clicked.connect(self.remove_self)

    def remove_self(self):
        try:
            self.parent.targets.remove(self.name)
        except ValueError:
            pass
        self.setParent(None)
        if len(self.parent.targets) == 0:
            self.parent.w_reply.hide()
