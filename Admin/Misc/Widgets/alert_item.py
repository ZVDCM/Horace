from PyQt5 import QtCore, QtGui, QtWidgets
from Students.Misc.Functions.relative_path import relative_path


class AlertItem(QtWidgets.QWidget):

    def __init__(self, parent, photo, message):
        super().__init__()
        self.parent = parent
        self.photo = photo
        self.message = message
        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(296, 78)
        Form.setMinimumSize(QtCore.QSize(296, 78))
        Form.setMaximumSize(QtCore.QSize(296, 78))
        Form.setStyleSheet("background: #256eff")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 8, 0, 8)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon = QtWidgets.QLabel(Form)
        self.icon.setMinimumSize(QtCore.QSize(50, 0))
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], self.photo)))
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName("icon")
        self.horizontalLayout.addWidget(self.icon)
        self.title = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(14)
        self.title.setFont(font)
        self.title.setStyleSheet("padding-bottom: 3px; color: white;")
        self.title.setIndent(10)
        self.title.setObjectName("title")
        self.horizontalLayout.addWidget(self.title)
        self.lbl_close = QtWidgets.QLabel(Form)
        self.lbl_close.setMinimumSize(QtCore.QSize(50, 0))
        self.lbl_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lbl_close.setText("")
        self.lbl_close.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_close.setObjectName("lbl_close")
        self.horizontalLayout.addWidget(self.lbl_close)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.title.setText(_translate("Form", self.message))

    def connect_signals(self):
        self.lbl_close.mousePressEvent = self.close_alert_clicked

    def close_alert_clicked(self, event):
        self.close()
        super(QtWidgets.QLabel, self.lbl_close).mousePressEvent(event)

    def enterEvent(self, event):
        self.lbl_close.setPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'close_2.png')))
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.lbl_close.clear()
        super().leaveEvent(event)

    def closeEvent(self, event):
        self.parent.items -= 1
        if self.parent.items < 1:
            self.parent.close()
        super().closeEvent(event)

    def showEvent(self, event):
        QtCore.QTimer.singleShot(5000, self.close)
        super().showEvent(event)
