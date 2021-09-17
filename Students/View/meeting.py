from PIL.Image import Image
from PIL.ImageQt import ImageQt
from Students.Misc.Widgets.teacher_message_received import MessageReceived
from Students.Misc.Widgets.custom_button import Button
from PyQt5 import QtCore, QtGui, QtWidgets
from Students.Misc.Widgets.loading_screen import LoadingScreen
from Students.Misc.Functions.relative_path import relative_path
from Students.Misc.Widgets.meeting_title_bar import TitleBar
from Students.Misc.Widgets.custom_list_view import ListView
from Students.Misc.Widgets.flow_layout import FlowLayout
from Students.Misc.Widgets.message_sent import MessageSent


class Meeting(QtWidgets.QMainWindow):

    def __init__(self, View):
        super().__init__()
        self.View = View
        self.setupUi(self)

        self.LoadingScreen = LoadingScreen(self.widget, relative_path('Students', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        self.interactors = [self.btn_student_list, self.btn_chat]
        self.close_buttons = [self.btn_close_student_list, self.btn_close_chat]

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
        self.centralwidget.setStyleSheet("background: #0B1A30;")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_bar = TitleBar(self)
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setStyleSheet("QWidget{\n"
                                  "    color: white; \n"
                                  "    font-family: Barlow\n"
                                  "}")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 70))
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 70))
        self.widget_2.setStyleSheet("background: #102542;")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_11.setContentsMargins(15, 15, 15, 15)
        self.horizontalLayout_11.setSpacing(15)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem = QtWidgets.QSpacerItem(
            772, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.btn_student_list = Button(self.widget_2, 0, False, relative_path('Students', ['Misc', 'Resources'], 'list_3'), relative_path(
            'Students', ['Misc', 'Resources'], 'list_2'), relative_path('Students', ['Misc', 'Resources'], 'list'))
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
        self.horizontalLayout_11.addWidget(self.btn_student_list)
        self.btn_chat = Button(self.widget_2, 1, False, relative_path('Students', ['Misc', 'Resources'], 'chat_3'), relative_path(
            'Students', ['Misc', 'Resources'], 'chat_2'), relative_path('Students', ['Misc', 'Resources'], 'chat'))
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
        self.horizontalLayout_11.addWidget(self.btn_chat)
        self.line_5 = QtWidgets.QFrame(self.widget_2)
        self.line_5.setStyleSheet("color: #083654;")
        self.line_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_5.setLineWidth(2)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_11.addWidget(self.line_5)
        self.btn_leave = QtWidgets.QPushButton(self.widget_2)
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
                                     f"    background-image: url({relative_path('Students', ['Misc', 'Resources'], 'call_end.png')});\n"
                                     "    background-position: center center;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "    background: none;\n"
                                     "    background-color: #bd2000;\n"
                                     "    background-repeat: none;\n"
                                     f"    background-image: url({relative_path('Students', ['Misc', 'Resources'], 'call_end.png')});\n"
                                     "    background-position: center center;\n"
                                     "}")
        self.btn_leave.setObjectName("btn_leave")
        self.horizontalLayout_11.addWidget(self.btn_leave)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.w_left = QtWidgets.QWidget(self.widget)
        self.w_left.setObjectName("w_left")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.w_left)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.screen = QtWidgets.QLabel(self.w_left)
        self.screen.setStyleSheet("")
        self.screen.setText("")
        self.screen.setAlignment(QtCore.Qt.AlignCenter)
        self.screen.setObjectName("screen")
        self.horizontalLayout.addWidget(self.screen)
        self.horizontalLayout_12.addWidget(self.w_left)
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
                                    "QScrollArea{\n"
                                    "    border: 1px solid #0b1a30;\n"
                                    "    border-radius: 5px\n"
                                    "}\n"
                                    "QScrollBar:vertical{\n"
                                    "    width: 12px;\n"
                                    "}\n"
                                    "\n"
                                    "QScrollBar::handle:vertical{\n"
                                    "    background-color: #97b9f4;    \n"
                                    "    min-height: 5px;\n"
                                    "    border-radius: 4px;\n"
                                    "    margin: 2px;\n\n"
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
                                    " }\n"
                                    "\n"
                                    "QScrollBar::sub-page:vertical{\n"
                                    "      background: #0b1a30;\n"
                                    "}")
        self.sw_right.setObjectName("sw_right")
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.page_8)
        self.verticalLayout_10.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_10.setSpacing(15)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_7 = QtWidgets.QLabel(self.page_8)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setIndent(1)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_14.addWidget(self.label_7)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem1)
        self.btn_close_student_list = QtWidgets.QPushButton(self.page_8)
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
                                                  f"    background-image: url({relative_path('Students', ['Misc', 'Resources'], 'close.png')});\n"
                                                  "    background-position: center center;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover{\n"
                                                  "    background: none;\n"
                                                  "    background-repeat: none;\n"
                                                  f"    background-image: url({relative_path('Students', ['Misc', 'Resources'], 'close_2.png')});\n"
                                                  "    background-position: center center;\n"
                                                  "}")
        self.btn_close_student_list.setObjectName("btn_close_student_list")
        self.horizontalLayout_14.addWidget(self.btn_close_student_list)
        self.verticalLayout_10.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_48.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_48.setSpacing(0)
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")
        self.txt_search_student = QtWidgets.QLineEdit(self.page_8)
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
        self.horizontalLayout_48.addWidget(self.txt_search_student)
        self.btn_search_student = QtWidgets.QPushButton(self.page_8)
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
        icon.addPixmap(QtGui.QPixmap(relative_path('Students', ['Misc', 'Resources'], 'search.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search_student.setIcon(icon)
        self.btn_search_student.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_student.setObjectName("btn_search_student")
        self.horizontalLayout_48.addWidget(self.btn_search_student)
        self.verticalLayout_10.addLayout(self.horizontalLayout_48)
        self.lv_student = QtWidgets.QListView(self.page_8)
        self.lv_student.setObjectName("lv_student")
        self.verticalLayout_10.addWidget(self.lv_student)
        self.sw_right.addWidget(self.page_8)
        self.page_9 = QtWidgets.QWidget()
        self.page_9.setObjectName("page_9")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.page_9)
        self.verticalLayout_11.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_11.setSpacing(15)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_3 = QtWidgets.QLabel(self.page_9)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setIndent(1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_15.addWidget(self.label_3)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem2)
        self.btn_close_chat = QtWidgets.QPushButton(self.page_9)
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
                                          f"    background-image: url({relative_path('Students', ['Misc', 'Resources'], 'close.png')});\n"
                                          "    background-position: center center;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:hover{\n"
                                          "    background: none;\n"
                                          "    background-repeat: none;\n"
                                          f"    background-image: url({relative_path('Students', ['Misc', 'Resources'], 'close_2.png')});\n"
                                          "    background-position: center center;\n"
                                          "}")
        self.btn_close_chat.setObjectName("btn_close_chat")
        self.horizontalLayout_15.addWidget(self.btn_close_chat)
        self.verticalLayout_11.addLayout(self.horizontalLayout_15)
        self.sa_chat = QtWidgets.QScrollArea(self.page_9)
        self.sa_chat.setStyleSheet("background: #0B1A30")
        self.sa_chat.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_chat.setWidgetResizable(True)
        self.sa_chat.setObjectName("sa_chat")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(
            QtCore.QRect(0, 0, 270, 307))
        self.scrollAreaWidgetContents_4.setObjectName(
            "scrollAreaWidgetContents_4")
        self.sa_chat.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_6.setContentsMargins(8, 15, 8, 15)
        self.verticalLayout_6.setSpacing(15)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        spacerItem6 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem6)

        self.verticalLayout_11.addWidget(self.sa_chat)

        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setSpacing(6)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.txt_message = QtWidgets.QLineEdit(self.page_9)
        self.txt_message.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_message.setFont(font)
        self.txt_message.setObjectName("txt_message")
        self.verticalLayout_12.addWidget(self.txt_message)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.btn_file = QtWidgets.QPushButton(self.page_9)
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
        self.horizontalLayout_18.addWidget(self.btn_file)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem1)
        self.btn_send = QtWidgets.QPushButton(self.page_9)
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
        self.horizontalLayout_18.addWidget(self.btn_send)
        self.verticalLayout_12.addLayout(self.horizontalLayout_18)
        self.verticalLayout_11.addLayout(self.verticalLayout_12)
        self.sw_right.addWidget(self.page_9)
        self.horizontalLayout_12.addWidget(self.sw_right)
        self.horizontalLayout_12.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
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

        self.retranslateUi(MainWindow)
        self.sw_right.setCurrentIndex(0)
        self.sw_right.hide()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_7.setText(_translate("MainWindow", "Students"))
        self.label_3.setText(_translate("MainWindow", "Chat"))
        self.txt_message.setPlaceholderText(
            _translate("MainWindow", "Type Something..."))

    def close_right(self):
        for interactor in self.interactors:
            if interactor.is_active:
                interactor.deactivate()
                break
        self.sw_right.hide()

    def display_message_sent(self, text):
        message_sent = MessageSent(self, text)
        self.verticalLayout_6.insertWidget(self.verticalLayout_6.count()-1, message_sent)
        self.txt_message.clear()

    @QtCore.pyqtSlot(str, str)
    def display_message_received(self, text, sender):
        message_received = MessageReceived(self, text, sender)
        self.verticalLayout_6.insertWidget(self.verticalLayout_6.count()-1, message_received)

    @QtCore.pyqtSlot(QtGui.QPixmap)
    def set_frame(self, frame):
        frame = frame.scaled(
                self.screen.width(), self.screen.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.screen.setPixmap(frame)

    def disconnect_screen(self):
        self.screen.clear()