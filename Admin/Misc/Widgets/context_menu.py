from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Functions.relative_path import relative_path


class ContextMenu(QtWidgets.QWidget):
    delete = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.hovering = False
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(230, 190)
        Form.setMinimumSize(QtCore.QSize(230, 50))
        Form.setMaximumSize(QtCore.QSize(230, 50))
        Form.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setStyleSheet("QWidget {\n"
                                  "    background: #0B1A30;\n"
                                  "    color: white; \n"
                                  "    font-family: Barlow\n"
                                  "}\n"
                                  "")
        self.widget.setObjectName("widget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.w_delete = QtWidgets.QWidget(self.widget)
        self.w_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.w_delete.setObjectName('w_delete')
        self.verticalLayout.addWidget(self.w_delete)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.w_delete)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.w_delete)
        self.label_5.setMinimumSize(QtCore.QSize(22, 22))
        self.label_5.setMaximumSize(QtCore.QSize(22, 22))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(relative_path(
            'Teachers', ['Misc', 'Resources'], 'trash.png')))
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.w_delete)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)

        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("Form", "Delete"))

    def connect_signals(self):
        self.w_delete.mousePressEvent = self.delete_pressed

        self.w_delete.mouseReleaseEvent = lambda e: self.item_released(
            e, self.w_delete)

        self.w_delete.enterEvent = lambda e: self.entered_item(
            e, self.w_delete)

        self.w_delete.leaveEvent = lambda e: self.left_item(
            e, self.w_delete)

    def delete_pressed(self, event):
        self.w_delete.setStyleSheet("background: #081222;")
        self.delete.emit()
        self.close()

    def item_released(self, event, item):
        item.setStyleSheet("background: transparent;")
        if self.hovering:
            item.setStyleSheet("background: #06293f;")

    def entered_item(self, event, item):
        self.hovering = True
        item.setStyleSheet("background: #06293f;")

    def left_item(self, event, item):
        self.hovering = False
        item.setStyleSheet("background: transparent;")
