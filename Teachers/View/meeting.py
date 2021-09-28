from Teachers.Misc.Widgets.alert_item import AlertItem
from Teachers.Misc.Functions.is_blank import is_blank
from Teachers.Misc.Widgets.pop_up import Popup
from Teachers.Misc.Widgets.badge_overlay import BadgeOverlay
from Teachers.Misc.Widgets.active_overlay import ActiveOverlay
from Teachers.Misc.Widgets.overlay import Overlay
from Teachers.Misc.Widgets.replied_to import RepliedMessageSent
from Teachers.Misc.Widgets.custom_button import Button
from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.loading_screen import LoadingScreen
from Teachers.Misc.Functions.relative_path import relative_path
from Teachers.Misc.Widgets.meeting_title_bar import TitleBar
from Teachers.Misc.Widgets.custom_list_view import ListView
from Teachers.Misc.Widgets.flow_layout import FlowLayout
from Teachers.Misc.Widgets.message_sent import MessageSent
from Teachers.Misc.Widgets.chat_input import ChatInput
from Teachers.Misc.Widgets.alert import Alert


class Meeting(QtWidgets.QMainWindow):

    def __init__(self, View):
        super().__init__()
        self.View = View
        self.setupUi(self)

        self.Popup = Popup(self)
        
        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        
        self.ActiveOverlay = ActiveOverlay(self)
        self.Overlay = Overlay(self.page)
        self.BadgeOverlay = BadgeOverlay(self.btn_chat)
        
        self.screens = [self.btn_screenshare, self.btn_inspector]
        self.interactors = [self.btn_student_list,
                            self.btn_chat, self.btn_block]
        self.close_buttons = [self.btn_close_student_list,
                              self.btn_close_chat, self.btn_close_url]

        self.LoadingScreen = LoadingScreen(self.widget, relative_path('Teachers', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        self.LoadingScreenURL = LoadingScreen(self.w_url, relative_path('Teachers', ['Misc', 'Resources'], 'loading_bars.gif'))
        self.LoadingScreenURLList = LoadingScreen(self.w_url_list, relative_path('Teachers', ['Misc', 'Resources'], 'loading_bars.gif'))

        self.url_state = 'Read'
        self.alert = Alert()

    def run(self):
        self.raise_()
        self.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 570)
        MainWindow.setMinimumSize(QtCore.QSize(800, 570))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget {\n"
                                         "    background: #0B1A30;\n"
                                         "    color: white; \n"
                                         "    font-family: Barlow\n"
                                         "}\n"
                                         "\n")
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

        self.lbl_timer = QtWidgets.QLabel('00:00:00', self.widget1)
        font = QtGui.QFont()
        font.setFamily("Barlow Thin")
        font.setPointSize(11)
        self.lbl_timer.setFont(font)
        self.lbl_timer.setIndent(4)
        self.lbl_timer.setStyleSheet("color: gray")
        self.horizontalLayout.addWidget(self.lbl_timer)

        spacerItem = QtWidgets.QSpacerItem(
            772, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_screenshare = Button(self.widget1, 0, True, relative_path('Teachers', ['Misc', 'Resources'], 'monitor_3'), relative_path(
            'Teachers', ['Misc', 'Resources'], 'monitor_2'), relative_path('Teachers', ['Misc', 'Resources'], 'monitor.png'))
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
        self.btn_inspector = Button(self.widget1, 1, False, relative_path('Teachers', ['Misc', 'Resources'], 'inspect_3'), relative_path(
            'Teachers', ['Misc', 'Resources'], 'inspect_2'), relative_path('Teachers', ['Misc', 'Resources'], 'inspect'))
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
        self.btn_student_list = Button(self.widget1, 0, False, relative_path('Teachers', ['Misc', 'Resources'], 'list_3'), relative_path(
            'Teachers', ['Misc', 'Resources'], 'list_2'), relative_path('Teachers', ['Misc', 'Resources'], 'list'))
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
        self.btn_chat = Button(self.widget1, 1, False, relative_path('Teachers', ['Misc', 'Resources'], 'chat_3'), relative_path(
            'Teachers', ['Misc', 'Resources'], 'chat_2'), relative_path('Teachers', ['Misc', 'Resources'], 'chat'))
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
        self.btn_block = Button(self.widget1, 2, False, relative_path('Teachers', ['Misc', 'Resources'], 'block_3'), relative_path(
            'Teachers', ['Misc', 'Resources'], 'block_2'), relative_path('Teachers', ['Misc', 'Resources'], 'block'))
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
        self.page_2.setStyleSheet("QPushButton {\n"
                                "  padding: 5px;\n"
                                "  border-radius: 5px;\n"
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
                                "}\n")
        self.verticalLayout_100 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_100.setContentsMargins(25, 29, 25, 25)
        self.verticalLayout_100.setObjectName("verticalLayout_100")

        self.horizontalLayout_101 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_101.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_101.setSpacing(6)
        self.horizontalLayout_101.setObjectName("horizontalLayout_101")
        self.verticalLayout_100.addLayout(self.horizontalLayout_101)
        self.lbl_inspector = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(15)
        self.lbl_inspector.setFont(font)
        self.lbl_inspector.setIndent(1)
        self.lbl_inspector.setObjectName("lbl_inspector")
        self.horizontalLayout_101.addWidget(self.lbl_inspector)
        spacerItem100 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_101.addItem(spacerItem100)

        self.btn_shutdown = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_shutdown.sizePolicy().hasHeightForWidth())
        self.btn_shutdown.setSizePolicy(sizePolicy)
        self.btn_shutdown.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_shutdown.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_shutdown.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_shutdown.setStyleSheet("QPushButton{\n"
                                           "    background-repeat: none;\n"
                                           f"   background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'shutdown.png')});\n"
                                           "    background-position: center center;\n"
                                           "}\n")
        self.btn_shutdown.setObjectName("btn_shutdown")
        self.horizontalLayout_101.addWidget(self.btn_shutdown)

        self.btn_restart = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_restart.sizePolicy().hasHeightForWidth())
        self.btn_restart.setSizePolicy(sizePolicy)
        self.btn_restart.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_restart.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_restart.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_restart.setStyleSheet("QPushButton{\n"
                                           "    background-repeat: none;\n"
                                           f"   background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'restart.png')});\n"
                                           "    background-position: center center;\n"
                                           "}\n")
        self.btn_restart.setObjectName("btn_restart")
        self.horizontalLayout_101.addWidget(self.btn_restart)

        self.btn_lock = QtWidgets.QPushButton(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_lock.sizePolicy().hasHeightForWidth())
        self.btn_lock.setSizePolicy(sizePolicy)
        self.btn_lock.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_lock.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_lock.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_lock.setStyleSheet("QPushButton{\n"
                                           "    background-repeat: none;\n"
                                           f"   background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'lock.png')});\n"
                                           "    background-position: center center;\n"
                                           "}\n")
        self.btn_lock.setObjectName("btn_lock")
        self.horizontalLayout_101.addWidget(self.btn_lock)

        self.sa_inspector = QtWidgets.QScrollArea(self.page_2)
        self.sa_inspector.setStyleSheet("QScrollArea{\n"
                                         "    border: 1px solid #102542;\n"
                                         "    border-radius: 5px\n"
                                         "}\n"
                                         "QScrollBar:vertical{\n"
                                         "    width: 12px;\n"
                                         "    background: #102542;\n"
                                         "}\n"
                                         "\n"
                                         "QScrollBar::handle:vertical{\n"
                                         "    background-color: #97b9f4;    \n"
                                         "    min-height: 5px;\n"
                                         "    border-radius: 4px;\n"
                                         "    margin: 2px;\n"
                                         "}\n"
                                         "\n"
                                         "QScrollBar::sub-line:vertical{\n"
                                         "     height: 0;\n"
                                         "     width: 0;\n"
                                         "}\n"
                                         "\n"
                                         "QScrollBar::add-line:vertical{\n"
                                         "     height: 0;\n"
                                         "     width: 0;\n"
                                         "}\n"
                                         "\n"
                                         "QScrollBar::add-page:vertical{\n"
                                         "    background: none;\n"
                                         " }\n"
                                         "\n"
                                         "QScrollBar::sub-page:vertical{\n"
                                         "     background: none;\n"
                                         "}")
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

        self.flow_layout = FlowLayout(self.scrollAreaWidgetContents_2)
        self.flow_layout.setObjectName("flow_layout")
        self.verticalLayout_100.addWidget(self.sa_inspector)

        self.sw_left.addWidget(self.page_2)
        self.horizontalLayout_3.addWidget(self.sw_left)
        self.sw_right = QtWidgets.QStackedWidget(self.widget)
        self.sw_right.setMinimumSize(QtCore.QSize(310, 0))
        self.sw_right.setMaximumSize(QtCore.QSize(310, 16777215))
        self.sw_right.setStyleSheet("QLineEdit {\n"
                                    "   padding: 1px 5px;\n"
                                    "   border: 1px solid #0e4884;\n"
                                    "   border-radius: 5px;\n"
                                    "   background-color: transparent;\n"
                                    "}\n"
                                    "\n"
                                    "QLabel {\n"
                                    "  background-color: transparent;\n"
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
                                    "\n")
        self.sw_right.setObjectName("sw_right")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.page_5.setStyleSheet("""
            QWidget#page_5{
                background: #083654;
            }
        """)
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

        self.horizontalLayout_102 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_102.setContentsMargins(0,0,0,0)
        self.horizontalLayout_102.setSpacing(6)
        self.horizontalLayout_102.setObjectName("horizontalLayout_102")
        self.verticalLayout_5.addLayout(self.horizontalLayout_102)

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
        self.horizontalLayout_102.addLayout(self.horizontalLayout_47)

        self.btn_send_many = QtWidgets.QPushButton(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_send_many.sizePolicy().hasHeightForWidth())
        self.btn_send_many.setSizePolicy(sizePolicy)
        self.btn_send_many.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_send_many.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_send_many.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_send_many.setStyleSheet("border-radius: 5px;\n"
                                    f"    background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'send_many.png')});\n"
                                    "background-repeat: no-repeat;\n"
                                    "background-position: center center;")
        self.btn_send_many.setObjectName(
            "btn_send_many")
        self.horizontalLayout_102.addWidget(self.btn_send_many)

        self.lv_student = ListView(self.page_5)
        self.lv_student.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lv_student.setObjectName("lv_student")
        self.verticalLayout_5.addWidget(self.lv_student)
        self.sw_right.addWidget(self.page_5)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.page_3.setStyleSheet("background: #083654;")
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
        self.sa_chat.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_chat.setWidgetResizable(True)
        self.sa_chat.setObjectName("sa_chat")
        self.sa_chat.setStyleSheet("QScrollArea{\n"
                                    "    border: 1px solid #0B1A30;\n"
                                    "}\n"
                                    "QScrollBar:vertical{\n"
                                    "    width: 12px;\n"
                                    "    background: #0B1A30;\n"
                                    "}\n"
                                    "\n"
                                    "QScrollBar::handle:vertical{\n"
                                    "    background-color: #97b9f4;    \n"
                                    "    min-height: 5px;\n"
                                    "    border-radius: 4px;\n"
                                    "    margin: 2px;\n"
                                    "}\n"
                                    "\n"
                                    "QScrollBar::sub-line:vertical{\n"
                                    "     height: 0;\n"
                                    "     width: 0;\n"
                                    "}\n"
                                    "\n"
                                    "QScrollBar::add-line:vertical{\n"
                                    "     height: 0;\n"
                                    "     width: 0;\n"
                                    "}\n"
                                    "\n"
                                    "QScrollBar::add-page:vertical{\n"
                                    "    background: none;\n"
                                    " }\n"
                                    "\n"
                                    "QScrollBar::sub-page:vertical{\n"
                                    "     background: none;\n"
                                    "}")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 270, 394))
        self.scrollAreaWidgetContents.setStyleSheet("background: #0B1A30;")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.sa_chat.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_10 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)
        self.verticalLayout_10.setContentsMargins(8, 15, 8, 15)
        self.verticalLayout_10.setSpacing(15)
        self.verticalLayout_10.setObjectName("verticalLayout_10")

        spacerItem6 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem6)
        self.verticalLayout_4.addWidget(self.sa_chat)

        self.ChatInput = ChatInput(self)
        self.verticalLayout_4.addWidget(self.ChatInput)

        self.sw_right.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.page_4.setStyleSheet("QWidget{\n"
                                    "   background-color:  #083654;\n"
                                    "}\n"
                                    "\n"
                                    "QLineEdit::disabled {\n"
                                    "   border: 1px solid #072f49;\n"
                                    "   border-radius: 5px;\n"
                                    "   background-color: #072f49;\n"
                                    "}\n"
                                    "\n"
                                    )
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
        self.btn_init_add_url = QtWidgets.QPushButton(
            self.widget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_add_url.sizePolicy().hasHeightForWidth())
        self.btn_init_add_url.setSizePolicy(sizePolicy)
        self.btn_init_add_url.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_init_add_url.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_init_add_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_url.setStyleSheet("QPushButton{\n"
                                            "   border-radius: 5px;\n"
                                            "   background: none;\n"
                                            "   background-color: #0e4884;\n"
                                            f"  background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'add.png')});\n"
                                            "   background-repeat: no-repeat;\n"
                                            "   background-position: center center;\n"
                                            "}"
                                            "\n"
                                            "QPushButton::disabled {\n"
                                            "   padding: 5px;\n"
                                            "   background: none;\n"
                                            "   border: 1px solid #102542;\n"
                                            "   background-color: #102542;\n"
                                            f"  background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'add_2.png')});\n"
                                            "   background-repeat: no-repeat;\n"
                                            "   background-position: center center;\n"
                                            "}"
                                            "\n"
                                            "QPushButton:focus,"
                                            "QPushButton:hover {\n"
                                            "   border: 1px solid #256eff;\n"
                                            "}"
                                            )
        self.btn_init_add_url.setObjectName(
            "btn_init_add_url")
        self.horizontalLayout_8.addWidget(self.btn_init_add_url)
        self.btn_init_edit_url = QtWidgets.QPushButton(
            self.widget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_edit_url.sizePolicy().hasHeightForWidth())
        self.btn_init_edit_url.setSizePolicy(sizePolicy)
        self.btn_init_edit_url.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_init_edit_url.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_init_edit_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_edit_url.setStyleSheet("QPushButton{\n"
                                            "   border-radius: 5px;\n"
                                            "   background: none;\n"
                                            "   background-color: #0e4884;\n"
                                            f"  background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'edit.png')});\n"
                                            "   background-repeat: no-repeat;\n"
                                            "   background-position: center center;\n"
                                            "}"
                                            "\n"
                                            "QPushButton::disabled {\n"
                                            "   padding: 5px;\n"
                                            "   border: 1px solid #102542;\n"
                                            "   background: none;\n"
                                            "   background-color: #102542;\n"
                                            f"  background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'edit_2.png')});\n"
                                            "   background-repeat: no-repeat;\n"
                                            "   background-position: center center;\n"
                                            "}"
                                            "\n"
                                            "QPushButton:focus,"
                                            "QPushButton:hover {\n"
                                            "   border: 1px solid #256eff;\n"
                                            "}"
                                            )
        self.btn_init_edit_url.setObjectName(
            "btn_init_edit_url")
        self.horizontalLayout_8.addWidget(self.btn_init_edit_url)
        self.btn_delete_url = QtWidgets.QPushButton(
            self.widget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_delete_url.sizePolicy().hasHeightForWidth())
        self.btn_delete_url.setSizePolicy(sizePolicy)
        self.btn_delete_url.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_delete_url.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_delete_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_url.setStyleSheet("QPushButton{\n"
                                            "   border-radius: 5px;\n"
                                            "   background: none;\n"
                                            "   border: 1px solid #0e4884;\n"
                                            f"  background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'trash.png')});\n"
                                            "   background-repeat: no-repeat;\n"
                                            "   background-position: center center;\n"
                                            "}"
                                            "\n"
                                            "QPushButton::disabled {\n"
                                            "   padding: 5px;\n"
                                            "   background: none;\n"
                                            "   border: 1px solid #102542;\n"
                                            f"  background-image: url({relative_path('Teachers', ['Misc', 'Resources'], 'trash_2.png')});\n"
                                            "   background-repeat: no-repeat;\n"
                                            "   background-position: center center;\n"
                                            "}"
                                            "\n"
                                            "QPushButton:focus,"
                                            "QPushButton:hover {\n"
                                            "   border: 1px solid #256eff;\n"
                                            "}"
                                            )
        self.btn_delete_url.setDisabled(True)
        self.btn_delete_url.setIconSize(QtCore.QSize(20, 20))
        self.btn_delete_url.setObjectName(
            "btn_delete_url")
        self.horizontalLayout_8.addWidget(self.btn_delete_url)
        self.verticalLayout_6.addWidget(self.widget2)
        self.txt_url = QtWidgets.QLineEdit(self.w_url)
        self.txt_url.setDisabled(True)
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
        self.btn_add_edit_url.setStyleSheet("QPushButton{\n"
                                          "    border-radius: 5px;\n"
                                          "    background: #0e4884;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:pressed {\n"
                                          "     background-color: #072f49;\n"
                                          "}")
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
        self.lv_url = ListView(self.w_url_list)
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
        self.lbl_meeting_status = QtWidgets.QLabel(self.status_bar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_meeting_status.sizePolicy().hasHeightForWidth())
        self.lbl_meeting_status.setSizePolicy(sizePolicy)
        self.lbl_meeting_status.setMinimumSize(QtCore.QSize(500, 20))
        self.lbl_meeting_status.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(9)
        self.lbl_meeting_status.setFont(font)
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)
        self.sw_left.setCurrentIndex(0)
        self.sw_right.setCurrentIndex(0)
        self.sw_right.hide()
        self.w_url_btn.hide()
        self.ChatInput.w_reply.hide()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_inspector.setText(_translate("MainWindow", "Inspector"))
        self.label_4.setText(_translate("MainWindow", "Students"))
        self.label_2.setText(_translate("MainWindow", "Chat"))
        self.label_5.setText(_translate("MainWindow", "Blacklisted Sites"))
        self.label_6.setText(_translate("MainWindow", "Domain"))
        self.btn_add_edit_url.setText(_translate("MainWindow", "Add"))
        self.btn_cancel_url.setText(_translate("MainWindow", "Cancel"))

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    def close_right(self):
        for interactor in self.interactors:
            if interactor.is_active:
                interactor.deactivate()
                break
        self.sw_right.hide()

    def display_message_sent(self, text):
        message_sent = MessageSent(self, text)
        self.verticalLayout_10.insertWidget(
            self.verticalLayout_10.count()-1, message_sent)
        self.ChatInput.txt_message.clear()

    def display_replied_message_sent(self, targets, text):
        message_sent = RepliedMessageSent(self, targets, text)
        self.verticalLayout_10.insertWidget(
            self.verticalLayout_10.count()-1, message_sent)
        self.ChatInput.txt_message.clear()

    @QtCore.pyqtSlot(QtGui.QPixmap)
    def set_frame(self, frame):
        frame = frame.scaled(
            self.screen.width(), self.screen.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.screen.setPixmap(frame)

    @QtCore.pyqtSlot(str, QtGui.QPixmap)
    def set_student_frame(self, name, frame):
        student_item = self.scrollAreaWidgetContents_2.findChild(QtWidgets.QWidget, name)
        if student_item:
            target_lbl = student_item.verticalLayout.itemAt(1).widget()
            target_lbl.setPixmap(frame)

    @QtCore.pyqtSlot(str)
    def remove_student_item(self, name):
        student_item = self.scrollAreaWidgetContents_2.findChild(QtWidgets.QWidget, name)
        student_item.deleteLater()

    def disconnect_screen(self):
        self.screen.clear()

    def set_timer(self, time):
        self.lbl_timer.setText(time)

    def run_popup(self, message, icon='information'):
        if icon == 'question':
            self.Popup.lbl_icon.setPixmap(QtGui.QPixmap(relative_path(
            'Teachers', ['Misc', 'Resources'], 'question.png')))
        elif icon == 'warning':
            self.Popup.lbl_icon.setPixmap(QtGui.QPixmap(relative_path(
            'Teachers', ['Misc', 'Resources'], 'warning.png')))
        elif icon == 'critical':
            self.Popup.lbl_icon.setPixmap(QtGui.QPixmap(relative_path(
            'Teachers', ['Misc', 'Resources'], 'critical.png')))
        
        self.Popup.lbl_message.setText(message)
        self.Popup.run()
    
    def clear_url_inputs(self):
        self.txt_url.clear()

    def disable_url_buttons(self):
        self.btn_init_add_url.setDisabled(True)
        self.btn_init_edit_url.setDisabled(True)
        self.btn_delete_url.setDisabled(True)
        self.w_url_btn.show()

    def enable_url_buttons(self):
        self.btn_init_add_url.setDisabled(False)
        self.btn_init_edit_url.setDisabled(False)
        if not is_blank(self.txt_url.text()):
            self.btn_delete_url.setDisabled(False)
        self.w_url_btn.hide()

    def disable_url_inputs(self):
        self.txt_url.setDisabled(True)

    def enable_url_inputs(self):
        self.txt_url.setDisabled(False)

    def set_url(self, value):
        self.url_state = value
        self.btn_add_edit_url.setText(value)

    def set_meeting_status(self, status):
        self.lbl_meeting_status.setText(status)

    def show_alert(self, type, message):
        if type == 'file':
            item = AlertItem(self.alert, 'clip_2.png', message)
        elif type == 'attendance':
            item = AlertItem(self.alert, 'attendance_3.png', message)
        self.alert.add_item(item)
        self.alert.show()