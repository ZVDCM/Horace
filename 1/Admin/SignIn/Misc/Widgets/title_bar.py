from PyQt5 import QtCore, QtGui, QtWidgets
from SignIn.Misc.Functions.relative_path import relative_path
from SignIn.Misc.Functions.read_db_config import read_db_config
from SignIn.Misc.Widgets.config import Config

class Operation(QtCore.QThread):
    success = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        is_success = self.fn()
        if not is_success:
            self.error.emit()
        else:
            self.success.emit()
        self.quit()

class TitleBar(QtWidgets.QWidget):
    resize = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.controller = None
        self.parent = parent
        self.start = QtCore.QPoint(0, 0)
        self.pressing = False

        self.setupUi(self)
        self.connect_signals()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(10, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.logo = QtWidgets.QLabel(Form)
        self.logo.setFixedSize(QtCore.QSize(18, 18))
        self.logo.setMaximumSize(QtCore.QSize(18, 18))
        qpixmap = QtGui.QPixmap(relative_path('SignIn', ['Misc', 'Resources'], 'Horace.png'))
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

        self.btn_config = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_config.sizePolicy().hasHeightForWidth())
        self.btn_config.setSizePolicy(sizePolicy)
        self.btn_config.setMinimumSize(QtCore.QSize(50, 0))
        self.btn_config.setMaximumSize(QtCore.QSize(55, 16777215))
        self.btn_config.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_config.setStyleSheet("QPushButton{\n"
                                        "    border: none;\n"
                                        "    border-radius: none;\n"
                                        "    background: none;\n"
                                        "    background-repeat: none;\n"
                                        f"    background-image: url({ relative_path('SignIn', ['Misc', 'Resources'], 'settings.png') });\n"
                                        "    background-position: center center;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "    background: none;\n"
                                        "    background: rgba(0, 0, 0, 40);\n"
                                        "    background-repeat: none;\n"
                                        f"    background-image: url({ relative_path('SignIn', ['Misc', 'Resources'], 'settings.png') });\n"
                                        "    background-position: center center;\n"
                                        "}")
        self.btn_config.setObjectName("btn_config")
        self.horizontalLayout.addWidget(self.btn_config)

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

    def connect_signals(self):
        self.resize.connect(self.resize_window)
        self.parent.resizeEvent = self.resizeEvent
        self.btn_config.clicked.connect(self.config)
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
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressing = False
        super().mouseReleaseEvent(event)

    def close_clicked(self):
        self.parent.close()

    def config(self):
        db_config = read_db_config()
        self.Config = Config(self.parent, db_config)
        self.Config.operation.connect(self.configured)
        self.Config.run()

    def configured(self):
        self.Operation = Operation(self.controller.Model.Database.init_db)
        self.Operation.started.connect(self.Config.LoadingScreen.run)
        self.Operation.success.connect(self.Config.close)
        self.Operation.error.connect(lambda: self.parent.run_popup('Database error', 'critical'))
        self.Operation.finished.connect(self.Config.LoadingScreen.hide)
        self.Operation.start()


