from Admin.Misc.Functions.is_blank import is_blank
from Admin.Misc.Functions.relative_path import relative_path
from Admin.Misc.Widgets.custom_lineedit import PasswordGenerator
from PyQt5 import QtCore, QtGui, QtWidgets


class StudentItem(QtWidgets.QWidget):
    search = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, w_student_item):
        w_student_item.setObjectName("w_student_item")
        w_student_item.resize(601, 147)
        w_student_item.setMinimumHeight(147)
        w_student_item.setMaximumHeight(147)
        w_student_item.setStyleSheet("QLineEdit {\n"
                                     "      padding: 1px 5px;\n"
                                     "      border: 1px solid #0e4884;\n"
                                     "      border-radius: 5px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton {\n"
                                     "  padding: 5px;\n"
                                     "  border: 1px solid #0e4884;\n"
                                     "  background-color: #0e4884;\n"
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
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(w_student_item)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(w_student_item)
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet("QWidget#widget {\n"
                                     "  padding: 1px 5px;\n"
                                     "  border: 1px solid #083654;\n"
                                     "  border-radius: 5px;\n"
                                     "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_32.setSpacing(0)
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.label_38 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_38.setFont(font)
        self.label_38.setIndent(1)
        self.label_38.setObjectName("label_38")
        self.horizontalLayout_32.addWidget(self.label_38)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_32.addItem(spacerItem)
        self.btn_student_item_close = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_student_item_close.sizePolicy().hasHeightForWidth())
        self.btn_student_item_close.setSizePolicy(sizePolicy)
        self.btn_student_item_close.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_student_item_close.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_student_item_close.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_student_item_close.setStyleSheet("QPushButton{\n"
                                                  "    border: none;\n"
                                                  "    border-radius: none;\n"
                                                  "    background: none;\n"
                                                  "    background-repeat: none;\n"
                                                  f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'close.png')});\n"
                                                  "    background-position: center center;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover{\n"
                                                  "    background: none;\n"
                                                  "    background-repeat: none;\n"
                                                  f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'close_2.png')});\n"
                                                  "    background-position: center center;\n"
                                                  "}")
        self.btn_student_item_close.setObjectName("btn_student_item_close")
        self.horizontalLayout_32.addWidget(self.btn_student_item_close)
        self.verticalLayout.addLayout(self.horizontalLayout_32)
        self.txt_student_item_username = QtWidgets.QLineEdit(self.widget)
        self.txt_student_item_username.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_student_item_username.setFont(font)
        self.txt_student_item_username.setObjectName(
            "txt_student_item_username")
        self.verticalLayout.addWidget(self.txt_student_item_username)
        self.label_33 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_33.setFont(font)
        self.label_33.setIndent(1)
        self.label_33.setObjectName("label_33")
        self.verticalLayout.addWidget(self.label_33)
        self.txt_student_item_password = PasswordGenerator(self.widget)
        self.txt_student_item_password.operation.emit()
        self.txt_student_item_password.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_student_item_password.setFont(font)
        self.txt_student_item_password.setObjectName(
            "txt_student_item_password")
        self.verticalLayout.addWidget(self.txt_student_item_password)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(w_student_item)
        QtCore.QMetaObject.connectSlotsByName(w_student_item)

    def retranslateUi(self, w_student_item):
        _translate = QtCore.QCoreApplication.translate
        self.label_38.setText(_translate("w_student_item", "Username"))
        self.label_33.setText(_translate("w_student_item", "Password"))

    def connect_signals(self):
        self.btn_student_item_close.clicked.connect(self.close_item)

    def close_item(self):
        self.parent.verticalLayout_38.removeWidget(self)
        if self.parent.verticalLayout_38.count() == 1:
            self.parent.btn_add_student_bulk.setDisabled(True)

    def get_value(self):
        return self.parent.section_combobox.currentText(), self.txt_student_item_username.text(),  self.txt_student_item_password.text()
