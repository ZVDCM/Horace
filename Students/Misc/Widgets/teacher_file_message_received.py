from Students.Misc.Functions.relative_path import relative_path
from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.custom_text_edit import TextEdit


class FileMessageReceived(QtWidgets.QWidget):
    operation = QtCore.pyqtSignal(bytearray, str)

    def __init__(self, parent, filename, data):
        super().__init__(parent=parent)
        self.parent = parent
        self.filename = filename
        self.data = data
        self.setupUi(self)
        self.textEdit.append(filename)
        self.textEdit.mousePressEvent = self.pressed

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 89)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 15, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(40, 0))
        self.label.setMaximumSize(QtCore.QSize(40, 16777215))
        self.label.setStyleSheet("background: #06293f; border-radius: 0; border-top-left-radius: 5px;  border-bottom-left-radius: 5px;")
        self.label.setPixmap(QtGui.QPixmap(relative_path('Students', ['Misc', 'Resources'], 'clip_2.png')))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textEdit = TextEdit(Form)
        self.textEdit.setMinimumLines(1)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textEdit.setStyleSheet("border-top-right-radius: 5px;  border-bottom-right-radius: 5px; background-color: #0e4884; padding: 10px; color: white;")
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.verticalLayout.addWidget(self.widget)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def pressed(self, event):
        self.operation.emit(self.data, self.filename)