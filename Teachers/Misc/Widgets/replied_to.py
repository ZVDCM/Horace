from Teachers.Misc.Functions.relative_path import relative_path
from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.custom_text_edit import TextEdit

class RepliedMessageSent(QtWidgets.QWidget):

    def __init__(self, parent, target, text):
        super().__init__(parent=parent)
        self.parent = parent
        self.target = target
        self.setupUi(self)
        self.textEdit.append(text)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 106)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(15, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 12, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(13, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        self.label_2.setFont(font)
        self.label_2.setPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'replied_to.png')))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lbl_target = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_target.sizePolicy().hasHeightForWidth())
        self.lbl_target.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        self.lbl_target.setFont(font)
        self.lbl_target.setStyleSheet("color: #6b6b6b")
        self.lbl_target.setObjectName("lbl_target")
        self.horizontalLayout.addWidget(self.lbl_target)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = TextEdit(Form)
        self.textEdit.setMinimumLines(1)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("border-radius: 5px; background-color: #256eff; padding: 10px; color: white;")
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit.setAlignment(QtCore.Qt.AlignRight)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_target.setText(_translate("Form", f"You replied to {self.target}"))
