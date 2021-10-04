from Students.Misc.Functions.relative_path import relative_path
from PyQt5 import QtCore, QtGui, QtWidgets


class ClassItem(QtWidgets.QWidget):
    operation = QtCore.pyqtSignal(object)
    
    def __init__(self, parent, Class):
        super().__init__(parent=parent)
        self.Class = Class
        self.setupUi(self)
        self.is_active = True

    def setupUi(self, Form):
        Form.setObjectName(self.Class.Code)
        Form.setMinimumSize(QtCore.QSize(201, 171))
        Form.setMaximumSize(QtCore.QSize(201, 171))
        Form.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        Form.setStyleSheet("QWidget{\n"
                           "    background: #102542;\n"
                           "    color: white; \n"
                           "    font-family: Barlow\n"
                           "}")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("letter-spacing: 1px")
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setIndent(0)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: gray")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: gray")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", self.Class.Code))
        self.label_2.setText(_translate(
            "Form", self.Class.Name))
        self.label_3.setText(_translate("Form", self.Class.Start))
        self.label_4.setText(_translate("Form", self.Class.End))

    def disable(self):
        self.is_active = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setStyleSheet("QWidget{\n"
                           "    background: #6b6b6b;\n"
                           "    color: #363636; \n"
                           "    font-family: Barlow\n"
                           "}")
        self.label_3.setStyleSheet("color: #363636")
        self.label_4.setStyleSheet("color: #363636")
    
    def activate(self):
        self.is_active = True
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet("QWidget{\n"
                           "    background: #102542;\n"
                           "    color: white; \n"
                           "    font-family: Barlow\n"
                           "}")
        self.label_3.setStyleSheet("color: gray")
        self.label_4.setStyleSheet("color: gray")

    def enterEvent(self, event):
        if self.is_active:
            self.widget.setStyleSheet("QWidget#widget{\n"
                                    "    border: 1px solid #256eff; \n"
                                    "}")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.widget.setStyleSheet("QWidget#widget{\n"
                                  "    border: none; \n"
                                  "}")
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.is_active:
            self.operation.emit(self.Class)
        super().mousePressEvent(event)