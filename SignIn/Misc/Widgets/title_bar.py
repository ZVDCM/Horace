from PyQt5 import QtCore, QtGui, QtWidgets
from SignIn.Misc.Functions.relative_path import relative_path


class TitleBar(QtWidgets.QWidget):

    def __init__(self, parent, is_fixed=False):
        super().__init__(parent=parent)
        self.parent = parent
        self.is_fixed = is_fixed
        self.start = QtCore.QPoint(0, 0)
        self.pressing = False
        self.is_maximized = False

        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(690, 30)
        Form.setMinimumSize(QtCore.QSize(0, 30))
        Form.setMaximumSize(QtCore.QSize(16777215, 30))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
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
                                            f"    background-image: url({ relative_path('SignIn', ['Misc', 'Resources'], 'minimize.png') });\n"
                                            "    background-position: center center;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "    background: none;\n"
                                            "    background: rgba(0, 0, 0, 40);\n"
                                            "    background-repeat: none;\n"
                                            f"    background-image: url({ relative_path('SignIn', ['Misc', 'Resources'], 'minimize.png') });\n"
                                            "    background-position: center center;\n"
                                            "}")
        self.btn_minimize.setObjectName("btn_minimize")
        self.horizontalLayout.addWidget(self.btn_minimize)

        if not self.is_fixed:
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
                                            f"    background-image: url({ relative_path('SignIn', ['Misc', 'Resources'], 'maximize.png') });\n"
                                            "    background-position: center center;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "    background: none;\n"
                                            "    background: rgba(0, 0, 0, 40);\n"
                                            "    background-repeat: none;\n"
                                            f"    background-image: url({ relative_path('SignIn', ['Misc', 'Resources'], 'maximize.png') });\n"
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
                                        f"    background-image: url({ relative_path('SignIn', ['Misc', 'Resources'], 'close.png') });\n"
                                        "    background-position: center center;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "    background: none;\n"
                                        "    background-color: red;\n"
                                        "    background-repeat: none;\n"
                                        f"    background-image: url({ relative_path('SignIn', ['Misc', 'Resources'], 'close_2.png') });\n"
                                        "    background-position: center center;\n"
                                        "}")
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout.addWidget(self.btn_close)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def resizeEvent(self, event):
        self.setFixedWidth(self.parent.width())
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, event):
        self.pressing = False
        super().mouseReleaseEvent(event)

    def connect_signals(self):
        self.btn_minimize.clicked.connect(self.minimize_clicked)
        if not self.is_fixed:
            self.btn_maximize_restore.clicked.connect(self.maximize_restore_clicked)
        self.btn_close.clicked.connect(self.close_clicked)

    def close_clicked(self):
        self.parent.close()

    def maximize_restore_clicked(self):
        if self.is_maximized:
            self.parent.showNormal()
            self.is_maximized = False
        else:
            self.parent.showMaximized()
            self.is_maximized = True

    def minimize_clicked(self):
        self.parent.showMinimized()

