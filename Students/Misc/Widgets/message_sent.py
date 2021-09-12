from PyQt5 import QtCore, QtGui, QtWidgets
from Students.Misc.Widgets.custom_text_edit import TextEdit

class MessageSent(QtWidgets.QWidget):

    def __init__(self, parent, text):
        super().__init__(parent=parent)
        self.parent = parent
        self.setupUi(self)
        self.textEdit.append(text)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 89)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(15, 15, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.textEdit = TextEdit(Form)
        self.textEdit.setMinimumLines(1)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet(
            "border-radius: 10px; background-color: #256eff; padding: 10px; color: white;")
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit.setReadOnly(True)
        self.textEdit.setAlignment(QtCore.Qt.AlignRight)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        QtCore.QMetaObject.connectSlotsByName(Form)
