from pynput import keyboard
from Teachers.Misc.Functions.relative_path import relative_path
from Teachers.Misc.Widgets.active_overlay import ActiveOverlay
from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.meeting_title_bar import TitleBar
from Teachers.Misc.Widgets.loading_screen import LoadingScreen

class RemoteDesktop(QtWidgets.QMainWindow):
    mouse_move = QtCore.pyqtSignal(tuple)
    mouse_press = QtCore.pyqtSignal(str)
    mouse_release = QtCore.pyqtSignal(str)
    mouse_wheel = QtCore.pyqtSignal(str)

    key_press = QtCore.pyqtSignal(object)
    key_release = QtCore.pyqtSignal(object)

    def __init__(self, View, parent):
        super().__init__()
        self.View = View
        self.parent = parent
        self.target_resolution = None
        self.setupUi(self)
        self.connect_signals()
        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)
        self.LoadingScreen = LoadingScreen(self.widget, relative_path('Teachers', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        
    def run(self):
        self.raise_()
        self.show()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet("QMainWindow{\n"
                                 "  background: #0B1A30;\n"
                                 "}")
        MainWindow.resize(800, 570)
        MainWindow.setMinimumSize(QtCore.QSize(800, 570))
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_bar = TitleBar(self)
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setStyleSheet("background: #081425;")
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
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setStyleSheet("QStatusBar {\n"
                                     "    background: #081222;\n"
                                     "}\n"
                                     "\n"
                                     "QStatusBar QLabel {\n"
                                     "    color: white;\n"
                                     "    padding-left: 3px;\n"
                                     "}")
        self.status_bar.setObjectName("statusbar")
        self.lbl_control_status = QtWidgets.QLabel(self.status_bar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_control_status.sizePolicy().hasHeightForWidth())
        self.lbl_control_status.setSizePolicy(sizePolicy)
        self.lbl_control_status.setMinimumSize(QtCore.QSize(500, 20))
        self.lbl_control_status.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.lbl_control_status.setFont(font)
        MainWindow.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def connect_signals(self):
        self.screen.mouseMoveEvent = self.mouse_moved
        self.screen.mousePressEvent = self.mouse_pressed
        self.screen.mouseReleaseEvent = self.mouse_released
        self.screen.wheelEvent = self.mouse_wheeled
    
    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
            if self.keyboard_listener.running:
                self.keyboard_listener.stop()
            self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.keyboard_listener.start()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()
            self.keyboard_listener.stop()

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
            self.mouse_move.emit(scaled_coordinates)
        super(QtWidgets.QLabel, self.screen).mouseMoveEvent(event)

    def mouse_pressed(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_press.emit('left')
        if event.button() == QtCore.Qt.MiddleButton:
            self.mouse_press.emit('middle')
        if event.button() == QtCore.Qt.RightButton:
            self.mouse_press.emit('right')
        super(QtWidgets.QLabel, self.screen).mousePressEvent(event)

    def mouse_released(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_release.emit('left')
        if event.button() == QtCore.Qt.MiddleButton:
            self.mouse_release.emit('middle')
        if event.button() == QtCore.Qt.RightButton:
            self.mouse_release.emit('right')
        super(QtWidgets.QLabel, self.screen).mouseReleaseEvent(event)

    def mouse_wheeled(self, event):
        degrees = event.angleDelta() / 8
        scroll_direction = f"{'down' if degrees.y() < 0 else 'up'}"
        self.mouse_wheel.emit(scroll_direction)
        super(QtWidgets.QLabel, self.screen).wheelEvent(event)

    def on_press(self, key):
        self.key_press.emit(key)

    def on_release(self, key):
        self.key_release.emit(key)

    def set_control_status(self, status):
        self.lbl_control_status.setText(status)