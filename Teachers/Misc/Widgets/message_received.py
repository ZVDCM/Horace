from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.custom_text_edit import TextEdit
from Teachers.Misc.Functions.relative_path import relative_path


class MessageReceived(QtWidgets.QWidget):
    operation = QtCore.pyqtSignal(str)

    def __init__(self, parent, text, sender):
        super().__init__(parent=parent)
        self.parent = parent
        self.sender = sender
        self.setupUi(self)
        self.textEdit.append(text)

        self.lbl_reply.mousePressEvent = self.lbl_clicked

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(174, 130)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_sender = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_sender.sizePolicy().hasHeightForWidth())
        self.lbl_sender.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        self.lbl_sender.setFont(font)
        self.lbl_sender.setStyleSheet("color: #6b6b6b; padding-left: 10px")
        self.lbl_sender.setObjectName("lbl_sender")
        self.verticalLayout.addWidget(self.lbl_sender)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.textEdit = TextEdit(Form)
        self.textEdit.setMinimumLines(1)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet(
            "border-radius: 5px; background-color: #0e4884; padding: 10px; color: white;")
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.lbl_reply = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_reply.sizePolicy().hasHeightForWidth())
        self.lbl_reply.setSizePolicy(sizePolicy)
        self.lbl_reply.setMinimumSize(QtCore.QSize(25, 0))
        self.lbl_reply.setMaximumSize(QtCore.QSize(25, 16777215))
        self.lbl_reply.setStyleSheet("QLabel{\n"
                                     "    background: none;\n"
                                     "    background-repeat: none;\n"
                                     f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'reply.png')});\n"
                                     "    background-position: center center;\n"
                                     "}\n"
                                     "\n"
                                     "QLabel:hover{\n"
                                     "    background: none;\n"
                                     "    background-repeat: none;\n"
                                     f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'reply_2.png')});\n"
                                     "    background-position: center center;\n"
                                     "}\n"
                                     "")
        self.lbl_reply.setText("")
        self.lbl_reply.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_reply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lbl_reply.setObjectName("lbl_reply")
        self.horizontalLayout.addWidget(self.lbl_reply)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_sender.setText(_translate("Form", self.sender))

    def lbl_clicked(self, event):
        self.operation.emit(self.sender)
