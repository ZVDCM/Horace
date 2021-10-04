from PyQt5 import QtCore, QtGui, QtWidgets


class Nav(QtWidgets.QWidget):
    operation = QtCore.pyqtSignal(int)

    def __init__(self, parent, target_index, title, active_icon, inactive_icon, hover_icon, is_active):
        super().__init__(parent=parent)
        self.parent = parent
        self.target_index = target_index
        self.title = title
        self.inactive_icon = inactive_icon
        self.setupUi(self)
        self.active_icon = active_icon
        self.hover_icon = hover_icon
        self.is_active = is_active

        if self.is_active:
            self.activate()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(94, 71)
        Form.setWindowTitle("")
        Form.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 8, 0, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_icon = QtWidgets.QLabel(self.widget)
        self.lbl_icon.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_icon.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lbl_icon.setStyleSheet("QLabel{\n"
                                        "    background: none;\n"
                                        "    background-repeat: none;\n"
                                        f"   background-image: url({self.inactive_icon});\n"
                                        "    background-position: center center;\n"
                                        "}"
                                        "")
        self.lbl_icon.setText("")
        self.lbl_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_icon.setObjectName("lbl_icon")
        self.verticalLayout.addWidget(self.lbl_icon)
        self.lbl_title = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_title.sizePolicy().hasHeightForWidth())
        self.lbl_title.setSizePolicy(sizePolicy)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setStyleSheet("color: #6b6b6b")
        self.lbl_title.setObjectName("lbl_title")
        self.verticalLayout.addWidget(self.lbl_title)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_title.setText(_translate("Form", self.title))

    def enterEvent(self, event):
        if not self.is_active:
            self.hovering()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_active:
           self.deactivate()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if not self.is_active:
            self.operation.emit(self.target_index)
        super().mousePressEvent(event)

    def activate(self):
        self.is_active = True
        self.widget.setStyleSheet('background: #256eff')
        self.lbl_icon.setStyleSheet("QLabel{\n"
                                    "    background: none;\n"
                                    "    background-repeat: none;\n"
                                    f"   background-image: url({self.active_icon});\n"
                                    "    background-position: center center;\n"
                                    "}"
                                    "")
        self.lbl_title.setStyleSheet("color: white")

    def deactivate(self):
        self.is_active = False
        self.widget.setStyleSheet('background: none')
        self.lbl_icon.setStyleSheet("QLabel{\n"
                                        "    background: none;\n"
                                        "    background-repeat: none;\n"
                                        f"   background-image: url({self.inactive_icon});\n"
                                        "    background-position: center center;\n"
                                        "}"
                                        "")
        self.lbl_title.setStyleSheet("color: #6b6b6b")

    def hovering(self):
        self.lbl_icon.setStyleSheet("QLabel{\n"
                                        "    background: none;\n"
                                        "    background-repeat: none;\n"
                                        f"   background-image: url({self.hover_icon});\n"
                                        "    background-position: center center;\n"
                                        "}"
                                        "")
        self.lbl_title.setStyleSheet("color: #256eff")

    