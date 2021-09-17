from Admin.Misc.Functions.relative_path import relative_path
from Admin.Misc.Widgets.active_overlay import ActiveOverlay
from PyQt5 import QtCore, QtGui, QtWidgets


class Popup(QtWidgets.QDialog):
    def __init__(self, parent, icon):
        super().__init__()
        self.parent = parent
        self.icon = icon
        self.setupUi(self)
        self.set_icon()
        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self.widget)
        self.btn_ok.clicked.connect(self.close)

    def run(self):
        self.activateWindow()
        QtWidgets.QApplication.instance().beep()
        self.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(299, 139)
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                              QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        Dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        Dialog.setStyleSheet("QWidget{\n"
                             "    background: #0B1A30;\n"
                             "    color: white; \n"
                             "    font-family: Barlow;\n"
                             "}\n"
                             "\n"
                             "QPushButton {\n"
                             "    padding: 5px;\n"
                             "    border-radius: 5px;\n"
                             "    border: 1px solid #0e4884;\n"
                             "    background-color: #0e4884;\n"
                             "}")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_icon = QtWidgets.QLabel(self.widget)
        self.lbl_icon.setMinimumSize(QtCore.QSize(60, 60))
        self.lbl_icon.setMaximumSize(QtCore.QSize(60, 60))
        self.lbl_icon.setText("")
        self.lbl_icon.setScaledContents(False)
        self.lbl_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_icon.setObjectName("lbl_icon")
        self.verticalLayout.addWidget(self.lbl_icon)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.lbl_message = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.lbl_message.setFont(font)
        self.lbl_message.setStyleSheet("")
        self.lbl_message.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lbl_message.setWordWrap(True)
        self.lbl_message.setObjectName("lbl_message")
        self.horizontalLayout.addWidget(self.lbl_message)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_ok = QtWidgets.QPushButton(self.widget)
        self.btn_ok.setMinimumSize(QtCore.QSize(100, 0))
        self.btn_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout_2.addWidget(self.btn_ok)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl_message.setText(_translate(
            "Dialog", "Student fields must not be empty"))
        self.btn_ok.setText(_translate("Dialog", "Ok"))

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.start = self.mapToGlobal(event.pos())
            self.pressing = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.move(self.mapToGlobal(self.movement).x(),
                      self.mapToGlobal(self.movement).y())
            self.start = self.end
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressing = False
        super().mouseReleaseEvent(event)

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.show()
        else:
            self.ActiveOverlay.hide()

    def set_icon(self):
        self.lbl_icon.setPixmap(QtGui.QPixmap(relative_path(
            'Admin', ['Misc', 'Resources'], f'{self.icon}.png')))