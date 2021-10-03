from PyQt5 import QtCore, QtGui, QtWidgets
from Students.Misc.Functions.relative_path import relative_path


class TitleBar(QtWidgets.QWidget):

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
        Form.resize(690, 30)
        Form.setMinimumSize(QtCore.QSize(0, 30))
        Form.setMaximumSize(QtCore.QSize(16777215, 30))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(10, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.logo = QtWidgets.QLabel(Form)
        self.logo.setFixedSize(QtCore.QSize(18, 18))
        self.logo.setMaximumSize(QtCore.QSize(18, 18))
        qpixmap = QtGui.QPixmap(relative_path('Students', ['Misc', 'Resources'], 'horace.png'))
        self.logo.setScaledContents(True)
        self.logo.setPixmap(qpixmap)
        self.logo.setStyleSheet("margin-top: 2px")
        self.horizontalLayout.addWidget(self.logo, alignment=QtCore.Qt.AlignCenter)

        self.title = QtWidgets.QLabel('PDC 60', Form)
        self.title.setStyleSheet("margin-top: 2px; margin-left: 5px; color: gray")
        font = QtGui.QFont()
        font.setFamily("Barlow")
        self.title.setFont(font)
        self.horizontalLayout.addWidget(self.title, alignment=QtCore.Qt.AlignCenter)

        spacerItem = QtWidgets.QSpacerItem(
            537, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
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
        self.btn_minimize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_minimize.setStyleSheet("QPushButton{\n"
                                      "    border: none;\n"
                                      "    border-radius: none;\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'minimize.png')});\n"
                                      "    background-position: center center;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover{\n"
                                      "    background: none;\n"
                                      "    background: rgba(0, 0, 0, 40);\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'minimize.png')});\n"
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
                                        f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'maximize.png')});\n"
                                        "    background-position: center center;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "    background: none;\n"
                                        "    background: rgba(0, 0, 0, 40);\n"
                                        "    background-repeat: none;\n"
                                        f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'maximize.png')});\n"
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
                                        f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close.png')});\n"
                                        "    background-position: center center;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "    background: none;\n"
                                        "    background-color: red;\n"
                                        "    background-repeat: none;\n"
                                        f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close_2.png')});\n"
                                        "    background-position: center center;\n"
                                        "}")
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout.addWidget(self.btn_close)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def connect_signals(self):
        self.btn_minimize.clicked.connect(self.minimize_clicked)
        self.btn_maximize_restore.clicked.connect(
            self.maximize_restore_clicked)
        self.btn_close.clicked.connect(self.close_clicked)

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
                return

            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.move(self.mapToGlobal(self.movement).x(),
                             self.mapToGlobal(self.movement).y())
            self.start = self.end
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressing = False
        self.parent.setMinimumSize(QtCore.QSize(800, 570))
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
        self.parent.ActiveOverlay.show()
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
        self.parent.ActiveOverlay.hide()
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
