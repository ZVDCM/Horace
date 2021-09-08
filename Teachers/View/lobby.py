from Teachers.Misc.Widgets.loading_screen import LoadingScreen
from Teachers.Misc.Widgets.nav import Nav
from Teachers.Misc.Functions.relative_path import relative_path
from Teachers.Misc.Widgets.lobby_title_bar import TitleBar
from Teachers.Misc.Widgets.custom_table_view import TableView
from Teachers.Misc.Widgets.custom_list_view import ListView
from PyQt5 import QtCore, QtGui, QtWidgets


class Lobby(QtWidgets.QMainWindow):

    def __init__(self, View):
        super().__init__()
        self.View = View
        self.setupUi(self)

        self.side_navs = [self.w_class, self.w_attendance]
        self.ClassLoadingScreen = LoadingScreen(self.classes, relative_path(
            'Teachers', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        self.AttendanceLoadingScreen = LoadingScreen(self.attendances, relative_path(
            'Teachers', ['Misc', 'Resources'], 'loading_bars_huge.gif'))

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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.title_bar = TitleBar(self)
        self.title_bar.setStyleSheet("background: #0B1A30;")
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
        self.verticalLayout_3.setContentsMargins(0, 16, 0, 20)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.w_class = Nav(self, 0, 'Classes', relative_path('Teachers', ['Misc', 'Resources'], 'class_3.png'), relative_path('Teachers', ['Misc', 'Resources'], 'class.png'), relative_path('Teachers', ['Misc', 'Resources'], 'class_2.png'), True)
        self.w_class.setObjectName("w_class")
        self.verticalLayout_3.addWidget(self.w_class)
        self.w_attendance = Nav(self, 1, 'Classes', relative_path('Teachers', ['Misc', 'Resources'], 'attendance_3.png'), relative_path('Teachers', ['Misc', 'Resources'], 'attendance.png'), relative_path('Teachers', ['Misc', 'Resources'], 'attendance_2.png'), False)
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
        self.btn_more_2 = QtWidgets.QPushButton(self.side_bar)
        self.btn_more_2.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_more_2.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_more_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_more_2.setStyleSheet("QPushButton{\n"
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
        self.btn_more_2.setObjectName("btn_more_2")
        self.horizontalLayout_7.addWidget(self.btn_more_2)
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
                                  "    background: #0B1A30;\n"
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
                                  "QScrollBar:vertical{\n"
                                  "    width: 18px;\n"
                                  "    margin: 0px 3px 0px 7px;\n"
                                  "    border-radius: 5px;\n"
                                  "}\n"
                                  "\n"
                                  "QScrollBar::handle:vertical{\n"
                                  "    background-color: #97b9f4;    \n"
                                  "    min-height: 5px;\n"
                                  "     border-radius: 4px;\n"
                                  "}\n"
                                  "\n"
                                  "QScrollBar::sub-line:vertical{\n"
                                  "     height: 0;\n"
                                  "     width: 0;\n"
                                  "}\n"
                                  "\n"
                                  "QScrollBar::add-line:vertical{\n"
                                  "        height: 0;\n"
                                  "     width: 0;\n"
                                  "}\n"
                                  "\n"
                                  "QScrollBar::add-page:vertical{\n"
                                  "    background: #0b1a30;\n"
                                  "    border-bottom-left-radius: 4px;\n"
                                  "    border-bottom-right-radius: 4px;\n"
                                  "    margin-top: -3px;\n"
                                  " }\n"
                                  "\n"
                                  "QScrollBar::sub-page:vertical{\n"
                                  "      background: #0b1a30;\n"
                                  "    border-top-left-radius: 4px;\n"
                                  "    border-top-right-radius: 4px;\n"
                                  "    margin-bottom: -3px;\n"
                                  "}")
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
        self.pushButton = QtWidgets.QPushButton(self.classes)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
                                      "    border-radius: 5px;\n"
                                      "    background: none;\n"
                                      "    padding: 5px 10px;\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:pressed {\n"
                                      "     background-color: #072f49;\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
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
        self.horizontalLayout_3.addWidget(self.label_7)
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_47.setSpacing(0)
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.txt_search_section = QtWidgets.QLineEdit(self.attendances)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_section.sizePolicy().hasHeightForWidth())
        self.txt_search_section.setSizePolicy(sizePolicy)
        self.txt_search_section.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_section.setMaximumSize(QtCore.QSize(250, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_section.setFont(font)
        self.txt_search_section.setStyleSheet("border-radius: none;\n"
                                              "border-top-left-radius: 5px;\n"
                                              "border-bottom-left-radius: 5px;")
        self.txt_search_section.setObjectName("txt_search_section")
        self.horizontalLayout_47.addWidget(self.txt_search_section)
        self.btn_search_sections = QtWidgets.QPushButton(self.attendances)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_sections.sizePolicy().hasHeightForWidth())
        self.btn_search_sections.setSizePolicy(sizePolicy)
        self.btn_search_sections.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_sections.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_sections.setFont(font)
        self.btn_search_sections.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_sections.setStyleSheet("border-top-right-radius: 5px;\n"
                                               "border-bottom-right-radius: 5px;")
        self.btn_search_sections.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'search.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search_sections.setIcon(icon)
        self.btn_search_sections.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_sections.setObjectName("btn_search_sections")
        self.horizontalLayout_47.addWidget(self.btn_search_sections)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_47)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tv_attendance = TableView(self.attendances)
        self.tv_attendance.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tv_attendance.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.tv_attendance.setObjectName("tv_attendance")
        self.horizontalLayout_4.addWidget(self.tv_attendance)
        self.lv_attendance = ListView(self.attendances)
        self.lv_attendance.setMaximumSize(QtCore.QSize(280, 16777215))
        self.lv_attendance.setObjectName("lv_attendance")
        self.horizontalLayout_4.addWidget(self.lv_attendance)
        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.sw_all.addWidget(self.attendances)
        self.horizontalLayout.addWidget(self.sw_all)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setStyleSheet("QStatusBar {\n"
                                      "    background: #081222;\n"
                                      "}\n"
                                      "\n"
                                      "QStatusBar QLabel {\n"
                                      "    color: white;\n"
                                      "    padding-top: 0px;\n"
                                      "    padding-left: 3px;\n"
                                      "}")
        self.status_bar.setSizeGripEnabled(True)
        self.status_bar.setObjectName("status_bar")
        self.lbl_database_status = QtWidgets.QLabel(
            "Database Initialized", self.status_bar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_database_status.sizePolicy().hasHeightForWidth())
        self.lbl_database_status.setSizePolicy(sizePolicy)
        self.lbl_database_status.setMinimumSize(QtCore.QSize(500, 20))
        self.lbl_database_status.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.lbl_database_status.setFont(font)
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        self.sw_all.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("MainWindow", "Classes"))
        self.pushButton.setText(_translate("MainWindow", "Create Class"))
        self.label_7.setText(_translate("MainWindow", "Attendances"))
