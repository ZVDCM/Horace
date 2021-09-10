from Teachers.Misc.Widgets.custom_button import Button
from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.loading_screen import LoadingScreen
from Teachers.Misc.Functions.relative_path import relative_path
from Teachers.Misc.Widgets.meeting_title_bar import TitleBar
from Teachers.Misc.Widgets.custom_list_view import ListView
from Teachers.Misc.Widgets.flow_layout import FlowLayout

class Meeting(QtWidgets.QMainWindow):

    def __init__(self, View):
        super().__init__()
        self.View = View
        self.setupUi(self)

        self.screens = [self.btn_screenshare, self.btn_inspector]
        self.interactors = [self.btn_student_list, self.btn_chat, self.btn_block]
        self.close_buttons = [self.btn_close_student_list, self.btn_close_chat, self.btn_close_url]

    def run(self):
        self.raise_()
        self.show()
        # self.title_bar.btn_maximize_restore.click()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(740, 540))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget {\n"
                                         "    background: #0B1A30;\n"
                                         "    color: white; \n"
                                         "    font-family: Barlow\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton {\n"
                                         "  padding: 5px;\n"
                                         "  border: 1px solid #0e4884;\n"
                                         "  background-color: #0e4884;\n"
                                         "}\n"
                                         "\n"
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
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_bar = TitleBar(self)
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_2.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget1 = QtWidgets.QWidget(self.widget)
        self.widget1.setMinimumSize(QtCore.QSize(0, 70))
        self.widget1.setMaximumSize(QtCore.QSize(16777215, 70))
        self.widget1.setStyleSheet("background: #102542;")
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(15, 15, 15, 15)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            772, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_screenshare = Button(self.widget1, 0, True, relative_path('Teachers', ['Misc', 'Resources'], 'monitor_3'), relative_path('Teachers', ['Misc', 'Resources'], 'monitor_2'), relative_path('Teachers', ['Misc', 'Resources'], 'monitor.png'))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_screenshare.sizePolicy().hasHeightForWidth())
        self.btn_screenshare.setSizePolicy(sizePolicy)
        self.btn_screenshare.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_screenshare.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_screenshare.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_screenshare.setObjectName("btn_screenshare")
        self.horizontalLayout.addWidget(self.btn_screenshare)
        self.btn_inspector = Button(self.widget1, 1, False, relative_path('Teachers', ['Misc', 'Resources'], 'inspect_3'), relative_path('Teachers', ['Misc', 'Resources'], 'inspect_2'), relative_path('Teachers', ['Misc', 'Resources'], 'inspect'))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_inspector.sizePolicy().hasHeightForWidth())
        self.btn_inspector.setSizePolicy(sizePolicy)
        self.btn_inspector.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_inspector.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_inspector.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_inspector.setObjectName("btn_inspector")
        self.horizontalLayout.addWidget(self.btn_inspector)
        self.line = QtWidgets.QFrame(self.widget1)
        self.line.setStyleSheet("color: #083654;")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.btn_student_list = Button(self.widget1, 0, False, relative_path('Teachers', ['Misc', 'Resources'], 'list_3'), relative_path('Teachers', ['Misc', 'Resources'], 'list_2'), relative_path('Teachers', ['Misc', 'Resources'], 'list'))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_student_list.sizePolicy().hasHeightForWidth())
        self.btn_student_list.setSizePolicy(sizePolicy)
        self.btn_student_list.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_student_list.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_student_list.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_student_list.setObjectName("btn_student_list")
        self.horizontalLayout.addWidget(self.btn_student_list)
        self.btn_chat = Button(self.widget1, 1, False, relative_path('Teachers', ['Misc', 'Resources'], 'chat_3'), relative_path('Teachers', ['Misc', 'Resources'], 'chat_2'), relative_path('Teachers', ['Misc', 'Resources'], 'chat'))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_chat.sizePolicy().hasHeightForWidth())
        self.btn_chat.setSizePolicy(sizePolicy)
        self.btn_chat.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_chat.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_chat.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_chat.setObjectName("btn_chat")
        self.horizontalLayout.addWidget(self.btn_chat)
        self.btn_block = Button(self.widget1, 2, False, relative_path('Teachers', ['Misc', 'Resources'], 'block_3'), relative_path('Teachers', ['Misc', 'Resources'], 'block_2'), relative_path('Teachers', ['Misc', 'Resources'], 'block'))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_block.sizePolicy().hasHeightForWidth())
        self.btn_block.setSizePolicy(sizePolicy)
        self.btn_block.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_block.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_block.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_block.setObjectName("btn_block")
        self.horizontalLayout.addWidget(self.btn_block)
        self.line_2 = QtWidgets.QFrame(self.widget1)
        self.line_2.setStyleSheet("color: #083654;")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.btn_leave = QtWidgets.QPushButton(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_leave.sizePolicy().hasHeightForWidth())
        self.btn_leave.setSizePolicy(sizePolicy)
        self.btn_leave.setMinimumSize(QtCore.QSize(80, 30))
        self.btn_leave.setMaximumSize(QtCore.QSize(80, 30))
        self.btn_leave.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_leave.setStyleSheet("QPushButton{\n"
                                     "    border: 1px solid #bd2000;\n"
                                     "    border-radius: 5px;\n"
                                     "    background: none;\n"
                                     "    background-repeat: none;\n"
                                     f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'call_end.png')});\n"
                                     "    background-position: center center;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    background: none;\n"
                                     "    background-color: #bd2000;\n"
                                     "    background-repeat: none;\n"
                                     f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'call_end.png')});\n"
                                     "    background-position: center center;\n"
                                     "}")
        self.btn_leave.setObjectName("btn_leave")
        self.horizontalLayout.addWidget(self.btn_leave)
        self.verticalLayout.addWidget(self.widget1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sw_left = QtWidgets.QStackedWidget(self.widget)
        self.sw_left.setAutoFillBackground(False)
        self.sw_left.setStyleSheet("background: #0B1A30;")
        self.sw_left.setObjectName("sw_left")
        self.page = QtWidgets.QWidget()
        self.page.setMouseTracking(True)
        self.page.setObjectName("page")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.screen = QtWidgets.QLabel(self.page)
        self.screen.setStyleSheet("")
        self.screen.setText("")
        self.screen.setAlignment(QtCore.Qt.AlignCenter)
        self.screen.setObjectName("screen")
        self.verticalLayout_3.addWidget(self.screen)
        self.sw_left.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_9.setContentsMargins(25, 29, 25, 25)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.sa_inspector = QtWidgets.QScrollArea(self.page_2)
        self.sa_inspector.setStyleSheet("border-radius: 5px")
        self.sa_inspector.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_inspector.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.sa_inspector.setWidgetResizable(True)
        self.sa_inspector.setObjectName("sa_inspector")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 858, 543))
        self.scrollAreaWidgetContents_2.setStyleSheet("background: #102542")
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.sa_inspector.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_9.addWidget(self.sa_inspector)
        self.sw_left.addWidget(self.page_2)
        self.horizontalLayout_3.addWidget(self.sw_left)
        self.sw_right = QtWidgets.QStackedWidget(self.widget)
        self.sw_right.setMinimumSize(QtCore.QSize(310, 0))
        self.sw_right.setMaximumSize(QtCore.QSize(310, 16777215))
        self.sw_right.setStyleSheet("QWidget{\n"
                                    "    background: #083654;\n"
                                    "}\n"
                                    "\n"
                                    "QListView{\n"
                                    "    border: 1px solid #0e4884;\n"
                                    "    border-radius: 5px;\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit {\n"
                                    "      padding: 1px 5px;\n"
                                    "      border: 1px solid #0e4884;\n"
                                    "      border-radius: 5px;\n"
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
        self.sw_right.setObjectName("sw_right")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_5.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.page_5)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setIndent(1)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.btn_close_student_list = QtWidgets.QPushButton(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_close_student_list.sizePolicy().hasHeightForWidth())
        self.btn_close_student_list.setSizePolicy(sizePolicy)
        self.btn_close_student_list.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_close_student_list.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_close_student_list.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close_student_list.setStyleSheet("QPushButton{\n"
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
                                                  "    background-repeat: none;\n"
                                                  f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close_2.png')});\n"
                                                  "    background-position: center center;\n"
                                                  "}")
        self.btn_close_student_list.setObjectName("btn_close_student_list")
        self.horizontalLayout_6.addWidget(self.btn_close_student_list)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_47.setSpacing(0)
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.txt_search_student = QtWidgets.QLineEdit(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_student.sizePolicy().hasHeightForWidth())
        self.txt_search_student.setSizePolicy(sizePolicy)
        self.txt_search_student.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_student.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_student.setFont(font)
        self.txt_search_student.setStyleSheet("border-radius: none;\n"
                                              "border-top-left-radius: 5px;\n"
                                              "border-bottom-left-radius: 5px;")
        self.txt_search_student.setObjectName("txt_search_student")
        self.horizontalLayout_47.addWidget(self.txt_search_student)
        self.btn_search_student = QtWidgets.QPushButton(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_student.sizePolicy().hasHeightForWidth())
        self.btn_search_student.setSizePolicy(sizePolicy)
        self.btn_search_student.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_student.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_student.setFont(font)
        self.btn_search_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_student.setStyleSheet("border-top-right-radius: 5px;\n"
                                              "border-bottom-right-radius: 5px;")
        self.btn_search_student.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'search.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search_student.setIcon(icon)
        self.btn_search_student.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_student.setObjectName("btn_search_student")
        self.horizontalLayout_47.addWidget(self.btn_search_student)
        self.verticalLayout_5.addLayout(self.horizontalLayout_47)
        self.lv_student = QtWidgets.QListView(self.page_5)
        self.lv_student.setObjectName("lv_student")
        self.verticalLayout_5.addWidget(self.lv_student)
        self.sw_right.addWidget(self.page_5)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_4.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_4.setSpacing(15)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.page_3)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setIndent(1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.btn_close_chat = QtWidgets.QPushButton(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_close_chat.sizePolicy().hasHeightForWidth())
        self.btn_close_chat.setSizePolicy(sizePolicy)
        self.btn_close_chat.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_close_chat.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_close_chat.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close_chat.setStyleSheet("QPushButton{\n"
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
                                          "    background-repeat: none;\n"
                                          f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close_2.png')});\n"
                                          "    background-position: center center;\n"
                                          "}")
        self.btn_close_chat.setObjectName("btn_close_chat")
        self.horizontalLayout_4.addWidget(self.btn_close_chat)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.sa_chat = QtWidgets.QScrollArea(self.page_3)
        self.sa_chat.setStyleSheet("border-radius: 5px")
        self.sa_chat.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_chat.setWidgetResizable(True)
        self.sa_chat.setObjectName("sa_chat")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 270, 394))
        self.scrollAreaWidgetContents.setStyleSheet("background: #0B1A30")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.sa_chat.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.sa_chat)
        self.lbl_reply = QtWidgets.QLabel(self.page_3)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_reply.setFont(font)
        self.lbl_reply.setStyleSheet("color: gray")
        self.lbl_reply.setIndent(1)
        self.lbl_reply.setObjectName("lbl_reply")
        self.verticalLayout_4.addWidget(self.lbl_reply)
        self.txt_message = QtWidgets.QLineEdit(self.page_3)
        self.txt_message.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_message.setFont(font)
        self.txt_message.setObjectName("txt_message")
        self.verticalLayout_4.addWidget(self.txt_message)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_file = QtWidgets.QPushButton(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_file.sizePolicy().hasHeightForWidth())
        self.btn_file.setSizePolicy(sizePolicy)
        self.btn_file.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_file.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_file.setStyleSheet("QPushButton{\n"
                                    "    border: none;\n"
                                    "    border-radius: none;\n"
                                    "    background: none;\n"
                                    "    background-repeat: none;\n"
                                    f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'clip.png')});\n"
                                    "    background-position: center center;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "    background: none;\n"
                                    "    background-repeat: none;\n"
                                    f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'clip_2.png')});\n"
                                    "    background-position: center center;\n"
                                    "}")
        self.btn_file.setObjectName("btn_file")
        self.horizontalLayout_5.addWidget(self.btn_file)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.btn_send = QtWidgets.QPushButton(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_send.sizePolicy().hasHeightForWidth())
        self.btn_send.setSizePolicy(sizePolicy)
        self.btn_send.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_send.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_send.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_send.setStyleSheet("QPushButton{\n"
                                    "    border: none;\n"
                                    "    border-radius: none;\n"
                                    "    background: none;\n"
                                    "    background-repeat: none;\n"
                                    f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'send.png')});\n"
                                    "    background-position: center center;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "    background: none;\n"
                                    "    background-repeat: none;\n"
                                    f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'send_2.png')});\n"
                                    "    background-position: center center;\n"
                                    "}")
        self.btn_send.setObjectName("btn_send")
        self.horizontalLayout_5.addWidget(self.btn_send)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.sw_right.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.w_url = QtWidgets.QWidget(self.page_4)
        self.w_url.setObjectName("w_url")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.w_url)
        self.verticalLayout_7.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_7.setSpacing(20)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.w_url)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setIndent(1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem4)
        self.btn_close_url = QtWidgets.QPushButton(self.w_url)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_close_url.sizePolicy().hasHeightForWidth())
        self.btn_close_url.setSizePolicy(sizePolicy)
        self.btn_close_url.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_close_url.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_close_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close_url.setStyleSheet("QPushButton{\n"
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
                                         "    background-repeat: none;\n"
                                         f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'close_2.png')});\n"
                                         "    background-position: center center;\n"
                                         "}")
        self.btn_close_url.setObjectName("btn_close_url")
        self.horizontalLayout_7.addWidget(self.btn_close_url)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget2 = QtWidgets.QWidget(self.w_url)
        self.widget2.setObjectName("widget2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_8.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.btn_import_students_sections_12 = QtWidgets.QPushButton(
            self.widget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_import_students_sections_12.sizePolicy().hasHeightForWidth())
        self.btn_import_students_sections_12.setSizePolicy(sizePolicy)
        self.btn_import_students_sections_12.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_import_students_sections_12.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_import_students_sections_12.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_import_students_sections_12.setStyleSheet("border-radius: 5px;\n"
                                                           f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'add.png')});\n"
                                                           "background-repeat: no-repeat;\n"
                                                           "background-position: center center;")
        self.btn_import_students_sections_12.setObjectName(
            "btn_import_students_sections_12")
        self.horizontalLayout_8.addWidget(self.btn_import_students_sections_12)
        self.btn_import_students_sections_14 = QtWidgets.QPushButton(
            self.widget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_import_students_sections_14.sizePolicy().hasHeightForWidth())
        self.btn_import_students_sections_14.setSizePolicy(sizePolicy)
        self.btn_import_students_sections_14.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_import_students_sections_14.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_import_students_sections_14.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_import_students_sections_14.setStyleSheet(
            "border-radius: 5px;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'edit.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_import_students_sections_14.setIcon(icon1)
        self.btn_import_students_sections_14.setIconSize(QtCore.QSize(20, 20))
        self.btn_import_students_sections_14.setObjectName(
            "btn_import_students_sections_14")
        self.horizontalLayout_8.addWidget(self.btn_import_students_sections_14)
        self.btn_import_students_sections_13 = QtWidgets.QPushButton(
            self.widget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_import_students_sections_13.sizePolicy().hasHeightForWidth())
        self.btn_import_students_sections_13.setSizePolicy(sizePolicy)
        self.btn_import_students_sections_13.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_import_students_sections_13.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_import_students_sections_13.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_import_students_sections_13.setStyleSheet("QPushButton{\n"
                                                           "    border-radius: 5px;\n"
                                                           "    background: none;\n"
                                                           "}\n"
                                                           "\n"
                                                           "\n"
                                                           "QPushButton:pressed {\n"
                                                           "     background-color: #072f49;\n"
                                                           "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'trash.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_import_students_sections_13.setIcon(icon2)
        self.btn_import_students_sections_13.setIconSize(QtCore.QSize(20, 20))
        self.btn_import_students_sections_13.setObjectName(
            "btn_import_students_sections_13")
        self.horizontalLayout_8.addWidget(self.btn_import_students_sections_13)
        self.verticalLayout_6.addWidget(self.widget2)
        self.txt_url = QtWidgets.QLineEdit(self.w_url)
        self.txt_url.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_url.setFont(font)
        self.txt_url.setObjectName("txt_url")
        self.verticalLayout_6.addWidget(self.txt_url)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.w_url_btn = QtWidgets.QWidget(self.w_url)
        self.w_url_btn.setObjectName("w_url_btn")
        self.verticalLayout_41 = QtWidgets.QVBoxLayout(self.w_url_btn)
        self.verticalLayout_41.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_41.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_41.setObjectName("verticalLayout_41")
        self.btn_add_edit_url = QtWidgets.QPushButton(self.w_url_btn)
        self.btn_add_edit_url.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_add_edit_url.setFont(font)
        self.btn_add_edit_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_edit_url.setStyleSheet("border-radius: 5px;")
        self.btn_add_edit_url.setObjectName("btn_add_edit_url")
        self.verticalLayout_41.addWidget(self.btn_add_edit_url)
        self.btn_cancel_url = QtWidgets.QPushButton(self.w_url_btn)
        self.btn_cancel_url.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_cancel_url.setFont(font)
        self.btn_cancel_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel_url.setStyleSheet("QPushButton{\n"
                                          "    border-radius: 5px;\n"
                                          "    background: none;\n"
                                          "}\n"
                                          "\n"
                                          "\n"
                                          "QPushButton:pressed {\n"
                                          "     background-color: #072f49;\n"
                                          "}")
        self.btn_cancel_url.setObjectName("btn_cancel_url")
        self.verticalLayout_41.addWidget(self.btn_cancel_url)
        self.verticalLayout_7.addWidget(self.w_url_btn)
        self.verticalLayout_9.addWidget(self.w_url)
        self.line_3 = QtWidgets.QFrame(self.page_4)
        self.line_3.setStyleSheet("color: #0e4177;")
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_9.addWidget(self.line_3)
        self.w_url_list = QtWidgets.QWidget(self.page_4)
        self.w_url_list.setObjectName("w_url_list")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.w_url_list)
        self.verticalLayout_8.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.lv_url = QtWidgets.QListView(self.w_url_list)
        self.lv_url.setObjectName("lv_url")
        self.verticalLayout_8.addWidget(self.lv_url)
        self.verticalLayout_9.addWidget(self.w_url_list)
        self.sw_right.addWidget(self.page_4)
        self.horizontalLayout_3.addWidget(self.sw_right)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.widget)
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

        self.retranslateUi(MainWindow)
        self.sw_left.setCurrentIndex(0)
        self.sw_right.setCurrentIndex(0)
        self.sw_right.hide()
        self.w_url_btn.hide()
        self.lbl_reply.hide()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_4.setText(_translate("MainWindow", "Students"))
        self.label_2.setText(_translate("MainWindow", "Chat"))
        self.lbl_reply.setText(_translate("MainWindow", "Replying to"))
        self.txt_message.setPlaceholderText(
            _translate("MainWindow", "Type Something..."))
        self.label_5.setText(_translate("MainWindow", "Blacklisted Sites"))
        self.label_6.setText(_translate("MainWindow", "URL"))
        self.btn_add_edit_url.setText(_translate("MainWindow", "Add"))
        self.btn_cancel_url.setText(_translate("MainWindow", "Cancel"))

    def close_right(self):
        for interactor in self.interactors:
            if interactor.is_active:
                interactor.deactivate()
                break
        self.sw_right.hide()