from Admin.Misc.Functions.is_blank import is_blank
from Admin.Misc.Functions.relative_path import relative_path
from PyQt5 import QtCore, QtGui, QtWidgets


class SectionItem(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, w_section_item):
        w_section_item.resize(653, 93)
        w_section_item.setMinimumHeight(93)
        w_section_item.setMaximumHeight(93)
        w_section_item.setStyleSheet("QLineEdit {\n"
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
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(w_section_item)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(w_section_item)
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet("QWidget#widget {\n"
                                     "  padding: 1px 5px;\n"
                                     "  border: 1px solid #083654;\n"
                                     "  border-radius: 5px;\n"
                                     "}")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_36.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_36.setSpacing(0)
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.label_43 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_43.setFont(font)
        self.label_43.setIndent(1)
        self.label_43.setObjectName("label_43")
        self.horizontalLayout_36.addWidget(self.label_43)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_36.addItem(spacerItem)
        self.btn_section_item_close = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_section_item_close.sizePolicy().hasHeightForWidth())
        self.btn_section_item_close.setSizePolicy(sizePolicy)
        self.btn_section_item_close.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_section_item_close.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_section_item_close.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_section_item_close.setStyleSheet("QPushButton{\n"
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
        self.btn_section_item_close.setObjectName("btn_section_item_close")
        self.horizontalLayout_36.addWidget(self.btn_section_item_close)
        self.verticalLayout.addLayout(self.horizontalLayout_36)
        self.txt_section_item_name = QtWidgets.QLineEdit(self.widget)
        self.txt_section_item_name.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_section_item_name.setFont(font)
        self.txt_section_item_name.setObjectName("txt_section_item_name")
        self.verticalLayout.addWidget(self.txt_section_item_name)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(w_section_item)
        QtCore.QMetaObject.connectSlotsByName(w_section_item)

    def retranslateUi(self, w_section_item):
        _translate = QtCore.QCoreApplication.translate
        self.label_43.setText(_translate("w_section_item", "Name"))

    def connect_signals(self):
        self.btn_section_item_close.clicked.connect(self.close_item)

    def close_item(self):
        self.parent.verticalLayout_53.removeWidget(self)
        if self.parent.verticalLayout_53.count() == 1:
            self.parent.btn_add_section_bulk.setDisabled(True)

    def get_value(self):
        return self.txt_section_item_name.text()