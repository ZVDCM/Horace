from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Functions.relative_path import relative_path


class ContextMenu(QtWidgets.QWidget):
    shutdown = QtCore.pyqtSignal()
    restart = QtCore.pyqtSignal()
    lock = QtCore.pyqtSignal()
    control = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.hovering = False
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(230, 190)
        Form.setMinimumSize(QtCore.QSize(230, 190))
        Form.setMaximumSize(QtCore.QSize(230, 190))
        Form.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 9)
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

        shadow_effect = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=4, xOffset=0, yOffset=2, color=QtGui.QColor("#222222"))
        self.widget.setGraphicsEffect(shadow_effect)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.w_shutdown = QtWidgets.QWidget(self.widget)
        self.w_shutdown.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.w_shutdown.setObjectName('w_shutdown')
        self.verticalLayout.addWidget(self.w_shutdown)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.w_shutdown)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.w_shutdown)
        self.label_5.setMinimumSize(QtCore.QSize(22, 22))
        self.label_5.setMaximumSize(QtCore.QSize(22, 22))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(relative_path(
            'Teachers', ['Misc', 'Resources'], 'shutdown.png')))
        self.label_5.setScaledContents(False)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.w_shutdown)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)

        self.w_restart = QtWidgets.QWidget(self.widget)
        self.w_restart.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.w_restart.setObjectName('w_restart')
        self.verticalLayout.addWidget(self.w_restart)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.w_restart)
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.w_restart)
        self.label_9.setMinimumSize(QtCore.QSize(22, 22))
        self.label_9.setMaximumSize(QtCore.QSize(22, 22))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(relative_path(
            'Teachers', ['Misc', 'Resources'], 'restart.png')))
        self.label_9.setScaledContents(False)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.w_restart)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)

        self.w_lock = QtWidgets.QWidget(self.widget)
        self.w_lock.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.w_lock.setObjectName('w_lock')
        self.verticalLayout.addWidget(self.w_lock)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.w_lock)
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.w_lock)
        self.label_7.setMinimumSize(QtCore.QSize(22, 22))
        self.label_7.setMaximumSize(QtCore.QSize(22, 22))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(relative_path(
            'Teachers', ['Misc', 'Resources'], 'lock.png')))
        self.label_7.setScaledContents(False)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.w_lock)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("color: #083654")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.w_control = QtWidgets.QWidget(self.widget)
        self.w_control.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.w_control.setObjectName('w_control')
        self.verticalLayout.addWidget(self.w_control)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.w_control)
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_11 = QtWidgets.QLabel(self.w_control)
        self.label_11.setMinimumSize(QtCore.QSize(22, 22))
        self.label_11.setMaximumSize(QtCore.QSize(22, 22))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(relative_path(
            'Teachers', ['Misc', 'Resources'], 'remote_desktop.png')))
        self.label_11.setScaledContents(False)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.w_control)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)

        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("Form", "Shutdown"))
        self.label_10.setText(_translate("Form", "Restart"))
        self.label_8.setText(_translate("Form", "Lock"))
        self.label_12.setText(_translate("Form", "Control"))

    def connect_signals(self):
        self.w_shutdown.mousePressEvent = self.shutdown_pressed
        self.w_restart.mousePressEvent = self.restart_pressed
        self.w_lock.mousePressEvent = self.lock_pressed
        self.w_control.mousePressEvent = self.control_pressed

        self.w_shutdown.mouseReleaseEvent = lambda e: self.item_released(
            e, self.w_shutdown)
        self.w_restart.mouseReleaseEvent = lambda e: self.item_released(
            e, self.w_restart)
        self.w_lock.mouseReleaseEvent = lambda e: self.item_released(
            e, self.w_lock)
        self.w_control.mouseReleaseEvent = lambda e: self.item_released(
            e, self.w_control)

        self.w_shutdown.enterEvent = lambda e: self.entered_item(
            e, self.w_shutdown)
        self.w_restart.enterEvent = lambda e: self.entered_item(
            e, self.w_restart)
        self.w_lock.enterEvent = lambda e: self.entered_item(
            e, self.w_lock)
        self.w_control.enterEvent = lambda e: self.entered_item(
            e, self.w_control)

        self.w_shutdown.leaveEvent = lambda e: self.left_item(
            e, self.w_shutdown)
        self.w_restart.leaveEvent = lambda e: self.left_item(
            e, self.w_restart)
        self.w_lock.leaveEvent = lambda e: self.left_item(
            e, self.w_lock)
        self.w_control.leaveEvent = lambda e: self.left_item(
            e, self.w_control)

    def shutdown_pressed(self, event):
        self.w_shutdown.setStyleSheet("background: #081222;")
        self.shutdown.emit()
        self.close()

    def restart_pressed(self, event):
        self.w_restart.setStyleSheet("background: #081222;")
        self.restart.emit()
        self.close()

    def lock_pressed(self, event):
        self.w_lock.setStyleSheet("background: #081222;")
        self.lock.emit()
        self.close()

    def control_pressed(self, event):
        self.w_control.setStyleSheet("background: #081222;")
        self.control.emit()
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

    def focusOutEvent(self, event):
        self.close()
        super().focusOutEvent(event)
