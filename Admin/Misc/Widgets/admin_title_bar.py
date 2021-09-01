from PyQt5 import QtCore, QtGui, QtWidgets
from Admin.Misc.Functions.relative_path import relative_path


class TitleBar(QtWidgets.QWidget):
    resize = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.start = QtCore.QPoint(0, 0)
        self.pressing = False
        self.prev_size= self.parent.size()

        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 30))
        Form.setMaximumSize(QtCore.QSize(16777215, 30))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(230, 0))
        self.widget.setMaximumSize(QtCore.QSize(230, 16777215))
        self.widget.setStyleSheet("background: #0D3C6E;")
        self.widget.setObjectName("widget")
        self.horizontalLayout_2.addWidget(self.widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            378, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_minimize = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_minimize.sizePolicy().hasHeightForWidth())
        self.btn_minimize.setSizePolicy(sizePolicy)
        self.btn_minimize.setMinimumSize(QtCore.QSize(50, 0))
        self.btn_minimize.setMaximumSize(QtCore.QSize(55, 16777215))
        self.btn_minimize.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_minimize.setStyleSheet("QPushButton{\n"
                                        "    border: none;\n"
                                        "    border-radius: none;\n"
                                        "    background: none;\n"
                                        "    background-repeat: none;\n"
                                        f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'minimize.png')});\n"
                                        "    background-position: center center;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "    background: none;\n"
                                        "    background: rgba(0, 0, 0, 40);\n"
                                        "    background-repeat: none;\n"
                                        f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'minimize.png')});\n"
                                        "    background-position: center center;\n"
                                        "}")
        self.btn_minimize.setObjectName("btn_minimize")
        self.horizontalLayout.addWidget(self.btn_minimize)
        self.btn_maximize_restore = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_maximize_restore.sizePolicy().hasHeightForWidth())
        self.btn_maximize_restore.setSizePolicy(sizePolicy)
        self.btn_maximize_restore.setMinimumSize(QtCore.QSize(50, 0))
        self.btn_maximize_restore.setMaximumSize(QtCore.QSize(55, 16777215))
        self.btn_maximize_restore.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_maximize_restore.setStyleSheet("QPushButton{\n"
                                                "    border: none;\n"
                                                "    border-radius: none;\n"
                                                "    background: none;\n"
                                                "    background-repeat: none;\n"
                                                f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'maximize.png')});\n"
                                                "    background-position: center center;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "    background: none;\n"
                                                "    background: rgba(0, 0, 0, 40);\n"
                                                "    background-repeat: none;\n"
                                                f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'maximize.png')});\n"
                                                "    background-position: center center;\n"
                                                "}")
        self.btn_maximize_restore.setObjectName("btn_maximize_restore")
        self.horizontalLayout.addWidget(self.btn_maximize_restore)
        self.btn_close = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)
        self.btn_close.setMinimumSize(QtCore.QSize(50, 0))
        self.btn_close.setMaximumSize(QtCore.QSize(55, 16777215))
        self.btn_close.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close.setAutoFillBackground(False)
        self.btn_close.setStyleSheet("QPushButton{\n"
                                     "    border: none;\n"
                                     "    border-radius: none;\n"
                                     "    background: none;\n"
                                     "    background-repeat: none;\n"
                                     f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'close.png')});\n"
                                     "    background-position: center center;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    background: none;\n"
                                     "    background-color: red;\n"
                                     "    background-repeat: none;\n"
                                     f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'close_2.png')});\n"
                                     "    background-position: center center;\n"
                                     "}")
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout.addWidget(self.btn_close)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def connect_signals(self):
        self.resize.connect(self.resize_window)
        self.parent.resizeEvent = self.resizeEvent
        self.btn_minimize.clicked.connect(self.minimize_clicked)
        self.btn_maximize_restore.clicked.connect(
            self.maximize_restore_clicked)
        self.btn_close.clicked.connect(self.close_clicked)

    def resizeEvent(self, event):
        self.resize.emit()
        super(self.parent.__class__, self.parent).resizeEvent(event)

    def resize_window(self):
        self.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.start = self.mapToGlobal(event.pos())
            self.pressing = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.pressing:
            if self.parent.isMaximized():
                self.btn_maximize_restore.click()
                self.parent.move(self.start.x() - (self.prev_size.width() // 2), 0)
                self.parent.setFixedSize(self.prev_size)

            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.move(self.mapToGlobal(self.movement).x(),
                             self.mapToGlobal(self.movement).y())
            self.start = self.end
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressing = False
        self.parent.setMinimumSize(QtCore.QSize(1188, 884))
        self.parent.setMaximumSize(QtCore.QSize(16777215, 16777215))
        super().mouseReleaseEvent(event)

    def close_clicked(self):
        self.parent.close()

    def maximize_restore_clicked(self):
        if self.parent.isMaximized():
            self.set_minimum()
        else:
            self.set_maximum()

    def set_minimum(self):
        self.parent.showNormal()
        self.btn_maximize_restore.setStyleSheet("QPushButton{\n"
                                                "    border: none;\n"
                                                "    border-radius: none;\n"
                                                "    background: none;\n"
                                                "    background-repeat: none;\n"
                                                f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'maximize.png')});\n"
                                                "    background-position: center center;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "    background: none;\n"
                                                "    background: rgba(0, 0, 0, 40);\n"
                                                "    background-repeat: none;\n"
                                                f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'maximize.png')});\n"
                                                "    background-position: center center;\n"
                                                "}")

    def set_maximum(self):
        self.prev_size = self.parent.size()
        self.parent.showMaximized()
        self.btn_maximize_restore.setStyleSheet("QPushButton{\n"
                                                "    border: none;\n"
                                                "    border-radius: none;\n"
                                                "    background: none;\n"
                                                "    background-repeat: none;\n"
                                                f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'restore.png')});\n"
                                                "    background-position: center center;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "    background: none;\n"
                                                "    background: rgba(0, 0, 0, 40);\n"
                                                "    background-repeat: none;\n"
                                                f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'restore.png')});\n"
                                                "    background-position: center center;\n"
                                                "}")

    def minimize_clicked(self):
        self.parent.showMinimized()
