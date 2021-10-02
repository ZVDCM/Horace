from Admin.Misc.Functions.is_blank import is_blank
from Admin.Misc.Functions.relative_path import relative_path
from Admin.Misc.Widgets.custom_lineedit import PasswordGenerator
from PyQt5 import QtCore, QtGui, QtWidgets


class ClassItem(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, w_class_item):
        w_class_item.setObjectName("w_class_item")
        w_class_item.resize(534, 265)
        w_class_item.setMinimumSize(QtCore.QSize(0, 265))
        w_class_item.setMaximumSize(QtCore.QSize(16777215, 265))
        w_class_item.setStyleSheet("QTimeEdit,\n"
                                   "QLineEdit {\n"
                                   "      padding: 1px 5px;\n"
                                   "      border: 1px solid #0e4884;\n"
                                   "      border-radius: 5px;\n"
                                   "}\n"
                                   "\n"
                                   "QTimeEdit:focus,\n"
                                   "QTimeEdit:hover,\n"
                                   "QLineEdit:focus,\n"
                                   "QLineEdit:hover {\n"
                                   "  border: 1px solid #256eff;\n"
                                   "  outline: none;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:pressed {\n"
                                   "  background-color: #072f49;\n"
                                   "}\n"
                                   "")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(w_class_item)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(w_class_item)
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet("QWidget#widget {\n"
                                     "  padding: 1px 5px;\n"
                                     "  border: 1px solid #083654;\n"
                                     "  border-radius: 5px;\n"
                                     "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_39.setSpacing(0)
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.label_45 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_45.setFont(font)
        self.label_45.setIndent(1)
        self.label_45.setObjectName("label_45")
        self.horizontalLayout_39.addWidget(self.label_45)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_39.addItem(spacerItem)
        self.btn_class_item_close = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_class_item_close.sizePolicy().hasHeightForWidth())
        self.btn_class_item_close.setSizePolicy(sizePolicy)
        self.btn_class_item_close.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_class_item_close.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_class_item_close.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_class_item_close.setStyleSheet("QPushButton{\n"
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
        self.btn_class_item_close.setObjectName("btn_class_item_close")
        self.horizontalLayout_39.addWidget(self.btn_class_item_close)
        self.verticalLayout.addLayout(self.horizontalLayout_39)
        self.txt_class_item_code = QtWidgets.QLineEdit(self.widget)
        self.txt_class_item_code.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_class_item_code.setFont(font)
        self.txt_class_item_code.setMaxLength(8)
        self.txt_class_item_code.setObjectName("txt_class_item_code")
        self.verticalLayout.addWidget(self.txt_class_item_code)
        self.label_41 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_41.setFont(font)
        self.label_41.setIndent(1)
        self.label_41.setObjectName("label_41")
        self.verticalLayout.addWidget(self.label_41)
        self.txt_class_item_name = QtWidgets.QLineEdit(self.widget)
        self.txt_class_item_name.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_class_item_name.setFont(font)
        self.txt_class_item_name.setObjectName("txt_class_item_name")
        self.verticalLayout.addWidget(self.txt_class_item_name)
        self.label_23 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_23.setFont(font)
        self.label_23.setIndent(1)
        self.label_23.setObjectName("label_23")
        self.verticalLayout.addWidget(self.label_23)
        self.te_class_start = QtWidgets.QTimeEdit(self.widget)
        self.te_class_start.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.te_class_start.setFont(font)
        self.te_class_start.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        self.te_class_start.setTime(QtCore.QTime(7, 0, 0))
        self.te_class_start.setObjectName("te_class_start")
        self.verticalLayout.addWidget(self.te_class_start)
        self.label_24 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_24.setFont(font)
        self.label_24.setIndent(1)
        self.label_24.setObjectName("label_24")
        self.verticalLayout.addWidget(self.label_24)
        self.te_class_end = QtWidgets.QTimeEdit(self.widget)
        self.te_class_end.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.te_class_end.setFont(font)
        self.te_class_end.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        self.te_class_end.setTime(QtCore.QTime(7, 0, 0))
        self.te_class_end.setObjectName("te_class_end")
        self.verticalLayout.addWidget(self.te_class_end)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(w_class_item)
        QtCore.QMetaObject.connectSlotsByName(w_class_item)

    def retranslateUi(self, w_class_item):
        _translate = QtCore.QCoreApplication.translate
        self.label_45.setText(_translate("w_class_item", "Code"))
        self.label_41.setText(_translate("w_class_item", "Name"))
        self.label_23.setText(_translate("w_class_item", "Start"))
        self.label_24.setText(_translate("w_class_item", "End"))

    def connect_signals(self):
        self.btn_class_item_close.clicked.connect(self.close_item)

    def close_item(self):
        self.parent.verticalLayout_50.removeWidget(self)
        if self.parent.verticalLayout_50.count() == 1:
            self.parent.btn_add_class_bulk.setDisabled(True)

    def get_value(self):
        start = self.te_class_start.time()
        start = ":".join([str(start.hour()), str(start.minute()), str(start.second())])
        end = self.te_class_end.time()
        end = ":".join([str(end.hour()), str(end.minute()), str(end.second())])
        return self.txt_class_item_code.text(), self.txt_class_item_name.text(), start, end
