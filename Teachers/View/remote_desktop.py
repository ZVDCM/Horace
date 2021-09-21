from Teachers.Misc.Functions.relative_path import relative_path
from Teachers.Misc.Widgets.active_overlay import ActiveOverlay
from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.meeting_title_bar import TitleBar
from Teachers.Misc.Widgets.loading_screen import LoadingScreen

class RemoteDesktop(QtWidgets.QMainWindow):
    operation = QtCore.pyqtSignal(tuple)

    def __init__(self, View, parent):
        super().__init__()
        self.View = View
        self.parent = parent
        self.target_resolution = None
        self.setupUi(self)
        self.screen.mouseMoveEvent = self.mouse_moved
        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)
        self.LoadingScreen = LoadingScreen(self.widget, relative_path('Teachers', ['Misc', 'Resources'], 'loading_bars_huge.gif'))

    def run(self):
        self.raise_()
        self.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet("QMainWindow{\n"
                                 "  background: #0B1A30;\n"
                                 "}")
        MainWindow.resize(800, 570)
        MainWindow.setMinimumSize(QtCore.QSize(800, 570))
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_bar = TitleBar(self)
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setStyleSheet("background: #0B1A30;")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("gridLayout")
        self.screen = QtWidgets.QLabel(self.widget)
        self.screen.setMouseTracking(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.screen.sizePolicy().hasHeightForWidth())
        self.screen.setSizePolicy(sizePolicy)
        self.screen.setText("")
        self.screen.setObjectName("screen")
        self.horizontalLayout.addWidget(self.screen, alignment=QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("QStatusBar {\n"
                                     "    background: #081222;\n"
                                     "}\n"
                                     "\n"
                                     "QStatusBar QLabel {\n"
                                     "    color: white;\n"
                                     "    padding-left: 3px;\n"
                                     "}")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    @QtCore.pyqtSlot(QtGui.QPixmap)
    def set_frame(self, frame):
        frame = frame.scaled(
            self.widget.width(), self.widget.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.screen.setPixmap(frame)

    def mouse_moved(self, event):
        if self.target_resolution:
            size_ratio = (self.screen.width()/self.target_resolution[0], self.screen.height()/self.target_resolution[1])
            pos = self.screen.mapToParent(event.pos())
            scaled_coordinates = (pos.x()//size_ratio[0], pos.y()//size_ratio[1])
            self.operation.emit(scaled_coordinates)
        super(QtWidgets.QLabel, self.screen).mouseMoveEvent(event)
