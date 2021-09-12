from Teachers.Misc.Functions.relative_path import relative_path
from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.custom_text_edit import TextEdit


class FileMessageReceived(QtWidgets.QWidget):
    download = QtCore.pyqtSignal(bytearray, str)
    reply = QtCore.pyqtSignal(str)

    def __init__(self, parent, sender, filename, data):
        super().__init__(parent=parent)
        self.parent = parent
        self.sender = sender
        self.filename = filename
        self.data = data
        self.setupUi(self)
        self.textEdit.append(filename)
        self.textEdit.mousePressEvent = self.file_pressed
        self.lbl_reply.mousePressEvent = self.reply_pressed

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(348, 89)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 15, 0)
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

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(40, 0))
        self.label.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label.setStyleSheet(
            "background: #06293f; border-radius: 0; border-top-left-radius: 5px;  border-bottom-left-radius: 5px;")
        self.label.setPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'clip_2.png')))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textEdit = TextEdit(Form)
        self.textEdit.setMinimumLines(1)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textEdit.setStyleSheet(
            "border-top-right-radius: 5px;  border-bottom-right-radius: 5px; background-color: #0e4884; padding: 10px; color: white;")
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit.setUndoRedoEnabled(True)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.lbl_reply = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_reply.sizePolicy().hasHeightForWidth())
        self.lbl_reply.setSizePolicy(sizePolicy)
        self.lbl_reply.setMinimumSize(QtCore.QSize(25, 0))
        self.lbl_reply.setMaximumSize(QtCore.QSize(25, 16777215))
        self.lbl_reply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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
        self.lbl_reply.setObjectName("lbl_reply")
        self.horizontalLayout.addWidget(self.lbl_reply)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_sender.setText(_translate("Form", self.sender))

    def file_pressed(self, event):
        self.download.emit(self.data, self.filename)

    def reply_pressed(self, event):
        self.reply.emit(self.sender)
