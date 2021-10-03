from Teachers.Misc.Widgets.account_context_menu import AccountContextMenu
from Teachers.Misc.Widgets.alert import Alert
from Teachers.Misc.Widgets.alert_item import AlertItem
from Teachers.Misc.Widgets.active_overlay import ActiveOverlay
from Teachers.Misc.Widgets.loading_screen import LoadingScreen
from Teachers.Misc.Widgets.nav import Nav
from Teachers.Misc.Functions.relative_path import relative_path
from Teachers.Misc.Widgets.lobby_title_bar import TitleBar
from Teachers.Misc.Widgets.custom_table_view import TableView
from Teachers.Misc.Widgets.custom_list_view import ListView
from Teachers.Misc.Widgets.flow_layout import FlowLayout
from Teachers.Misc.Widgets.class_item import ClassItem
from PyQt5 import QtCore, QtGui, QtWidgets


class Lobby(QtWidgets.QMainWindow):

    def __init__(self, View):
        super().__init__()
        self.View = View
        self.setupUi(self)

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)

        self.side_navs = [self.w_class, self.w_attendance]
        self.ClassLoadingScreen = LoadingScreen(self.classes, relative_path(
            'Teachers', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        self.AttendanceTableLoadingScreen = LoadingScreen(self.tv_attendance, relative_path(
            'Teachers', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        self.AttendanceListLoadingScreen = LoadingScreen(self.lv_attendance, relative_path(
            'Teachers', ['Misc', 'Resources'], 'loading_bars.gif'))

        self.alert = Alert()
        self.ContextMenu = AccountContextMenu(self)

    def run(self):
        self.raise_()
        self.show()
        self.title_bar.btn_maximize_restore.click()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet("QMainWindow{\n"
                                 "    background: #0B1A30;"
                                 "}\n")
        MainWindow.setMinimumSize(QtCore.QSize(974, 806))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.title_bar = TitleBar(self)
        self.title_bar.setStyleSheet("background: #081425;")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_5.addWidget(self.title_bar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.side_bar = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.side_bar.sizePolicy().hasHeightForWidth())
        self.side_bar.setSizePolicy(sizePolicy)
        self.side_bar.setMinimumSize(QtCore.QSize(92, 0))
        self.side_bar.setStyleSheet("background: #0D3C6E;")
        self.side_bar.setObjectName("side_bar")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.side_bar)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 20)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.w_class = Nav(self, 0, 'Classes', relative_path('Teachers', ['Misc', 'Resources'], 'class_3.png'), relative_path('Teachers', ['Misc', 'Resources'], 'class.png'), relative_path('Teachers', ['Misc', 'Resources'], 'class_2.png'), True)
        self.w_class.setObjectName("w_class")
        self.verticalLayout_3.addWidget(self.w_class)
        self.w_attendance = Nav(self, 1, 'Attendances', relative_path('Teachers', ['Misc', 'Resources'], 'attendance_3.png'), relative_path('Teachers', ['Misc', 'Resources'], 'attendance.png'), relative_path('Teachers', ['Misc', 'Resources'], 'attendance_2.png'), False)
        self.w_attendance.setObjectName("w_attendance")
        self.verticalLayout_3.addWidget(self.w_attendance)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem2 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.btn_more = QtWidgets.QPushButton(self.side_bar)
        self.btn_more.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_more.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_more.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_more.setStyleSheet("QPushButton{\n"
                                      "    border: none;\n"
                                      "    border-radius: none;\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'menu.png')});\n"
                                      "    background-position: center center;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover{\n"
                                      "    background: none;\n"
                                      "    background-repeat: none;\n"
                                      f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'menu_2.png')});\n"
                                      "    background-position: center center;\n"
                                      "}")
        self.btn_more.setObjectName("btn_more")
        self.horizontalLayout_7.addWidget(self.btn_more)
        spacerItem3 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.widget_4 = QtWidgets.QWidget(self.side_bar)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3.addWidget(self.widget_4)
        self.horizontalLayout.addWidget(self.side_bar)
        self.sw_all = QtWidgets.QStackedWidget(self.centralwidget)
        self.sw_all.setStyleSheet("QWidget {\n"
                                  "    background: #081425;\n"
                                  "    color: white; \n"
                                  "    font-family: Barlow\n"
                                  "}\n"
                                  "\n"
                                  "QLineEdit {\n"
                                  "    padding: 1px 5px;\n"
                                  "    border: 1px solid #0e4884;\n"
                                  "    border-radius: 5px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton {\n"
                                  "  padding: 5px;\n"
                                  "  border: 1px solid #0e4884;\n"
                                  "  background-color: #0e4884;\n"
                                  "}\n"
                                  "\n"
                                  "QLineEdit:focus,\n"
                                  "QLineEdit:hover,\n"
                                  "QPushButton:focus,\n"
                                  "QPushButton:hover {\n"
                                  "  border: 1px solid #256eff;\n"
                                  "  outline: none;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:pressed {\n"
                                  "  background-color: #072f49;\n"
                                  "}\n"
                                  "\n"
                                  "QGroupBox {\n"
                                  "    border: 1px solid #083654;\n"
                                  "    border-radius: 5px;\n"
                                  "    margin-top: 15px;\n"
                                  "}\n"
                                  "QGroupBox::title{\n"
                                  "    subcontrol-origin: margin;\n"
                                  "    subcontrol-position: top left;\n"
                                  "    margin-top: 2px;\n"
                                  "    margin-left: 20px;\n"
                                  "    background-color: transparent;\n"
                                  "}\n"
                                  )
        self.sw_all.setObjectName("sw_all")
        self.classes = QtWidgets.QWidget()
        self.classes.setStyleSheet("")
        self.classes.setObjectName("classes")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.classes)
        self.verticalLayout_7.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_7.setSpacing(20)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.classes)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("padding-bottom: 3px;")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setIndent(1)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.sa_class = QtWidgets.QScrollArea(self.classes)
        self.sa_class.setStyleSheet("")
        self.sa_class.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_class.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.sa_class.setWidgetResizable(True)
        self.sa_class.setObjectName("sa_class")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 840, 658))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.flow_layout = FlowLayout(parent=self.scrollAreaWidgetContents, spacing=20)
        self.flow_layout.setObjectName("flow_layout")

        self.sa_class.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_7.addWidget(self.sa_class)
        self.verticalLayout_7.setStretch(1, 1)
        self.sw_all.addWidget(self.classes)
        self.attendances = QtWidgets.QWidget()
        self.attendances.setObjectName("attendances")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.attendances)
        self.verticalLayout_8.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_8.setSpacing(20)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(15)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.horizontalLayout_69 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_69.setContentsMargins(0,0,5,0)
        self.horizontalLayout_69.setSpacing(0)

        self.label_7 = QtWidgets.QLabel(self.attendances)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("")
        self.label_7.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_7.setIndent(1)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_69.addWidget(self.label_7)

        self.btn_download = QtWidgets.QPushButton(self.attendances)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_download.sizePolicy().hasHeightForWidth())
        self.btn_download.setSizePolicy(sizePolicy)
        self.btn_download.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_download.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_download.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_download.setStyleSheet("border-radius: 5px;\n"
                                    f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'download.png')});\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center center;")
        self.btn_download.setObjectName(
            "btn_download")
        self.horizontalLayout_69.addWidget(self.btn_download)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_69)
        
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_47.setSpacing(0)
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.txt_search_attendance = QtWidgets.QLineEdit(self.attendances)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_attendance.sizePolicy().hasHeightForWidth())
        self.txt_search_attendance.setSizePolicy(sizePolicy)
        self.txt_search_attendance.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_attendance.setMaximumSize(QtCore.QSize(250, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_attendance.setFont(font)
        self.txt_search_attendance.setStyleSheet("border-radius: none;\n"
                                              "border-top-left-radius: 5px;\n"
                                              "border-bottom-left-radius: 5px;")
        self.txt_search_attendance.setObjectName("txt_search_attendance")
        self.horizontalLayout_47.addWidget(self.txt_search_attendance)
        self.btn_search_attendance = QtWidgets.QPushButton(self.attendances)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_attendance.sizePolicy().hasHeightForWidth())
        self.btn_search_attendance.setSizePolicy(sizePolicy)
        self.btn_search_attendance.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_attendance.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_attendance.setFont(font)
        self.btn_search_attendance.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_attendance.setStyleSheet("border-top-right-radius: 5px;\n"
                                               "border-bottom-right-radius: 5px;")
        self.btn_search_attendance.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'search.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search_attendance.setIcon(icon)
        self.btn_search_attendance.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_attendance.setObjectName("btn_search_attendance")
        self.horizontalLayout_47.addWidget(self.btn_search_attendance)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_47)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.groupBox = QtWidgets.QGroupBox('Content', self.attendances)
        self.groupBox.setObjectName("groupBox")
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setContentsMargins(20,20,20,20)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        self.tv_attendance = TableView(self.groupBox)
        self.tv_attendance.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.tv_attendance.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.tv_attendance.setObjectName("tv_attendance")
        
        self.verticalLayout_6.addWidget(self.tv_attendance)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox('File', self.attendances)
        self.groupBox_2.setMaximumSize(QtCore.QSize(280, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_9.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_9.setObjectName("verticalLayout_9")

        self.lv_attendance = ListView(self.groupBox_2)
        self.lv_attendance.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.lv_attendance.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.lv_attendance.setObjectName("lv_attendance")

        self.verticalLayout_9.addWidget(self.lv_attendance)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.sw_all.addWidget(self.attendances)
        self.horizontalLayout.addWidget(self.sw_all)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setStyleSheet("QStatusBar {\n"
                                      "    background: #060d18;\n"
                                      "}\n"
                                      "\n"
                                      "QStatusBar QLabel {\n"
                                      "    color: white;\n"
                                      "    padding-top: 0px;\n"
                                      "    padding-left: 3px;\n"
                                      "}")
        self.status_bar.setSizeGripEnabled(True)
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
        self.sw_all.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("MainWindow", "Classes"))
        self.label_7.setText(_translate("MainWindow", "Attendances"))

    def add_class_item(self, Class):
        self.ClassItem = ClassItem(self, Class) 
        self.flow_layout.addWidget(self.ClassItem)

    def show_alert(self, type, message):
        if type == 'file':
            item = AlertItem(self.alert, 'clip_2.png', message)
        self.alert.add_item(item)
        self.alert.show()

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    def set_lobby_status(self, status):
        try:
            self.lbl_lobby_status.setText(status)
        except RuntimeError:
            return