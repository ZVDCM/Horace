from PyQt5 import QtCore, QtGui, QtWidgets
from Students.Misc.Widgets.custom_text_edit import TextEdit

class MessageReceived(QtWidgets.QWidget):

    def __init__(self, parent, text, sender):
        super().__init__(parent=parent)
        self.parent = parent
        self.sender = sender
        self.setupUi(self)
        self.textEdit.append(text)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 104)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 15, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_sender = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_sender.sizePolicy().hasHeightForWidth())
        self.lbl_sender.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        self.lbl_sender.setFont(font)
        self.lbl_sender.setStyleSheet("color: #6b6b6b; padding-left: 10px")
        self.lbl_sender.setObjectName("lbl_sender")
        self.verticalLayout.addWidget(self.lbl_sender)

        self.textEdit = TextEdit(Form)
        self.textEdit.setMinimumLines(1)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("border-radius: 5px; background-color: #0e4884; padding: 10px; color: white;")
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAlignment(QtCore.Qt.AlignLeft)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_sender.setText(_translate("Form", self.sender))
