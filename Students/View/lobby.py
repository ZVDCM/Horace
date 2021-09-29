from Students.Misc.Widgets.account_context_menu import AccountContextMenu
from Students.Misc.Widgets.active_overlay import ActiveOverlay
from Students.Misc.Widgets.class_item import ClassItem
from Students.Misc.Widgets.flow_layout import FlowLayout
from Students.Misc.Functions.relative_path import relative_path
from Students.Misc.Widgets.loading_screen import LoadingScreen
from Students.Misc.Widgets.meeting_title_bar import TitleBar
from PyQt5 import QtCore, QtGui, QtWidgets


class Lobby(QtWidgets.QMainWindow):

    def __init__(self, View):
        super().__init__()
        self.View = View
        self.setupUi(self)

        self.ClassLoadingScreen = LoadingScreen(self.widget, relative_path(
            'Students', ['Misc', 'Resources'], 'loading_bars_huge.gif'))

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)
        self.ContextMenu = AccountContextMenu(self)


    def run(self):
        self.raise_()
        self.show()
        self.title_bar.btn_maximize_restore.click()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(974, 806))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background: #0B1A30;")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_bar = TitleBar(self)
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_2.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setStyleSheet("QWidget{\n"
                                  "    background: #081425;\n"
                                  "    color: white; \n"
                                  "    font-family: Barlow\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(25, 15, 25, 25)
        self.verticalLayout.setSpacing(25)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_more = QtWidgets.QPushButton(self.widget)
        self.btn_more.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_more.setStyleSheet("QPushButton{\n"
                                      "    border: none;\n"
                                      "    border-radius: none;\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Students', ['Misc', 'Resources'], 'menu_alt.png')});\n"
                                      "    background-position: center center;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover{\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Students', ['Misc', 'Resources'], 'menu_alt_2.png')});\n"
                                      "    background-position: center center;\n"
                                      "}\n"
                                      "")
        self.btn_more.setObjectName("btn_more")
        self.horizontalLayout.addWidget(self.btn_more)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 881, 586))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.flow_layout = FlowLayout(parent=self.scrollAreaWidgetContents, spacing=20)
        self.flow_layout.setObjectName("flow_layout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout_2.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setStyleSheet("QStatusBar {\n"
                                     "    background: #060d18;\n"
                                     "}\n"
                                     "\n"
                                     "QStatusBar QLabel {\n"
                                     "    color: white;\n"
                                     "    padding-left: 3px;\n"
                                     "}")
        self.status_bar.setObjectName("status_bar")
        self.lbl_lobby_status = QtWidgets.QLabel(self.status_bar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_lobby_status.sizePolicy().hasHeightForWidth())
        self.lbl_lobby_status.setSizePolicy(sizePolicy)
        self.lbl_lobby_status.setMinimumSize(QtCore.QSize(500, 20))
        self.lbl_lobby_status.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.lbl_lobby_status.setFont(font)
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Classes"))

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    def add_class_item(self, Class):
        self.ClassItem = ClassItem(self, Class) 
        self.flow_layout.addWidget(self.ClassItem)

    def set_lobby_status(self, status):
        self.lbl_lobby_status.setText(status)