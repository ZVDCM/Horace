from Admin.Misc.Widgets.account_context_menu import AccountContextMenu
from Admin.Misc.Widgets.class_item import ClassItem
from Admin.Misc.Widgets.section_item import SectionItem
from Admin.Misc.Widgets.context_menu import ContextMenu
from Admin.Misc.Widgets.confirm import Confirm
from Admin.Misc.Widgets.custom_label import SideNav
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from Admin.Misc.Widgets.admin_title_bar import TitleBar
from Admin.Misc.Widgets.loading_screen import LoadingScreen
from Admin.Misc.Widgets.custom_table_view import TableView
from Admin.Misc.Widgets.custom_list_view import ListView
from Admin.Misc.Widgets.custom_lineedit import PasswordGenerator
from Admin.Misc.Widgets.pop_up import Popup
from Admin.Misc.Functions.relative_path import relative_path
from Admin.Misc.Widgets.student_item import StudentItem
from Admin.Misc.Widgets.teacher_item import TeacherItem
from Admin.Misc.Widgets.active_overlay import ActiveOverlay


class Admin(QtWidgets.QMainWindow):

    def __init__(self, View):
        super().__init__()
        self.View = View
        self.setupUi(self)
        self.side_navs = [self.lbl_students_and_sections, self.lbl_teachers_and_attendances,
                          self.lbl_classes_and_members, self.lbl_blacklisted_url]

        self.Popup = Popup(self)

        # Table
        self.TableSectionStudentLoadingScreen = LoadingScreen(self.w_table_section_student, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        self.TableTeacherLoadingScreen = LoadingScreen(self.w_table_teacher, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        self.TableClassLoadingScreen = LoadingScreen(self.w_table_class, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        
        # Section Student
        self.SectionLoadingScreen = LoadingScreen(self.w_section_input, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))
        self.StudentLoadingScreen = LoadingScreen(self.w_student_input, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))
        self.SectionStudentLoadingScreen = LoadingScreen(self.w_section_student, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))

        # Teacher Attendance
        self.TeacherLoadingScreen = LoadingScreen(self.w_teacher_input, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))
        self.AttendanceLoadingScreen = LoadingScreen(self.w_attendance, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))

        # Class Member
        self.ClassLoadingScreen = LoadingScreen(self.w_class_input, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))
        self.ClassTeacherLoadingScreen = LoadingScreen(self.w_class_teacher, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))
        self.ClassSectionLoadingScreen = LoadingScreen(self.w_class_section, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))

        # URL
        self.URLViewerLoadingScreen = LoadingScreen(self.w_website_viewer, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_bars_huge.gif'))
        self.URLLoadingScreen = LoadingScreen(self.w_url_input, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))
        self.URLSLoadingScreen = LoadingScreen(self.w_url, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))

        self.hide_buttons()
        self.disable_edit_delete()
        self.disable_student_inputs()
        self.disable_section_inputs()
        self.disable_teacher_inputs()
        self.disable_class_inputs()
        self.disable_url_inputs()

        self.student_state = "Read"
        self.section_state = "Read"
        self.teacher_state = "Read"
        self.class_state = "Read"
        self.url_state = "Read"

        self.AccountContextMenu = AccountContextMenu(self.btn_more)
        self.ActiveOverlay = ActiveOverlay(self)
        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)


    def run(self):
        self.raise_()
        self.show()
        self.title_bar.btn_maximize_restore.click()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        MainWindow.setMinimumSize(QtCore.QSize(1188, 884))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QWidget{\n"
                                         "    background: #0B1A30;\n"
                                         "    color: white; \n"
                                         "    font-family: Barlow\n"
                                         "}\n"
                                         "\n"
                                         "QGroupBox {\n"
                                         "    border: 1px solid #083654;\n"
                                         "    border-radius: 5px;\n"
                                         "    margin-top: 15px;\n"
                                         "}\n"
                                         "\n"
                                         "QGroupBox::title{\n"
                                         "    subcontrol-origin: margin;\n"
                                         "    subcontrol-position: top left;\n"
                                         "    margin-top: 7px;\n"
                                         "    margin-left: 15px;\n"
                                         "    background-color: transparent;\n"
                                         "}\n"
                                         "\n"
                                         "\n"
                                         )
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_bar = TitleBar(self)
        self.title_bar.setMinimumSize(QtCore.QSize(0, 30))
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title_bar.setStyleSheet("background: #0B1A30;")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout.addWidget(self.title_bar)
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
        self.side_bar.setMinimumSize(QtCore.QSize(230, 0))
        self.side_bar.setStyleSheet("background: #0D3C6E;")
        self.side_bar.setObjectName("side_bar")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.side_bar)
        self.verticalLayout_5.setContentsMargins(15, 15, 0, 15)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.icon = QtWidgets.QLabel(self.side_bar)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setStyleSheet("margin-top: 10px; \n"
                                "margin-bottom: 10px;\n"
                                "padding-right: 15px")
        self.icon.setText("")
        self.icon.setPixmap(QtGui.QPixmap(relative_path(
            'Admin', ['Misc', 'Resources'], 'crown.png')))
        self.icon.setScaledContents(False)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName("icon")
        self.verticalLayout_5.addWidget(self.icon)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl_students_and_sections = SideNav(self, True, 0)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.lbl_students_and_sections.setFont(font)
        self.lbl_students_and_sections.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lbl_students_and_sections.setStyleSheet("padding: 10px;\n"
                                                     "border-left: 5px solid #71A0F8;\n"
                                                     "background: #256EFF;")
        self.lbl_students_and_sections.setObjectName(
            "lbl_students_and_sections")
        self.verticalLayout_3.addWidget(self.lbl_students_and_sections)
        self.lbl_teachers_and_attendances = SideNav(self, False, 1)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.lbl_teachers_and_attendances.setFont(font)
        self.lbl_teachers_and_attendances.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lbl_teachers_and_attendances.setStyleSheet("padding: 10px")
        self.lbl_teachers_and_attendances.setObjectName(
            "lbl_teachers_and_attendances")
        self.verticalLayout_3.addWidget(self.lbl_teachers_and_attendances)
        self.lbl_classes_and_members = SideNav(self, False, 2)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.lbl_classes_and_members.setFont(font)
        self.lbl_classes_and_members.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lbl_classes_and_members.setStyleSheet("padding: 10px")
        self.lbl_classes_and_members.setObjectName("lbl_classes_and_members")
        self.verticalLayout_3.addWidget(self.lbl_classes_and_members)
        self.lbl_blacklisted_url = SideNav(self, False, 3)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.lbl_blacklisted_url.setFont(font)
        self.lbl_blacklisted_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lbl_blacklisted_url.setStyleSheet("padding: 10px")
        self.lbl_blacklisted_url.setObjectName("lbl_blacklisted_url")
        self.verticalLayout_3.addWidget(self.lbl_blacklisted_url)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 283, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.btn_more = QtWidgets.QPushButton(self.side_bar)
        self.btn_more.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_more.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_more.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_more.setStyleSheet("QPushButton{\n"
                                    "    border: none;\n"
                                    "    border-radius: none;\n"
                                    "    background: none;\n"
                                    "    background-repeat: none;\n"
                                    f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'menu.png')});\n"
                                    "    background-position: center center;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "    background: none;\n"
                                    "    background-repeat: none;\n"
                                    f"   background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'menu_2.png')});\n"
                                    "    background-position: center center;\n"
                                    "}")
        self.btn_more.setObjectName("btn_more")
        self.horizontalLayout_7.addWidget(self.btn_more)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout.addWidget(self.side_bar)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setStyleSheet("background: #081425")
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sw_all = QtWidgets.QStackedWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sw_all.sizePolicy().hasHeightForWidth())
        self.sw_all.setSizePolicy(sizePolicy)
        self.sw_all.setObjectName("sw_all")
        self.section_student = QtWidgets.QWidget()
        self.section_student.setObjectName("section_student")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.section_student)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(15)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.w_table_section_student = QtWidgets.QWidget(self.section_student)
        self.w_table_section_student.setMinimumSize(QtCore.QSize(377, 0))
        self.w_table_section_student.setStyleSheet("QWidget{\n"
                                    "    background: #102542;\n"
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
        self.w_table_section_student.setObjectName("w_table_section_student")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.w_table_section_student)
        self.verticalLayout_6.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.lbl_sections_table_status = QtWidgets.QLabel(self.w_table_section_student)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_sections_table_status.setFont(font)
        self.lbl_sections_table_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sections_table_status.setIndent(1)
        self.lbl_sections_table_status.setObjectName(
            "lbl_sections_table_status")
        self.horizontalLayout_8.addWidget(self.lbl_sections_table_status)
        self.line_8 = QtWidgets.QFrame(self.w_table_section_student)
        self.line_8.setStyleSheet("color: #083654;")
        self.line_8.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_8.setLineWidth(2)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setObjectName("line_8")
        self.horizontalLayout_8.addWidget(self.line_8)
        self.lbl_students_table_status = QtWidgets.QLabel(self.w_table_section_student)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_students_table_status.setFont(font)
        self.lbl_students_table_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_students_table_status.setIndent(1)
        self.lbl_students_table_status.setObjectName(
            "lbl_students_table_status")
        self.horizontalLayout_8.addWidget(self.lbl_students_table_status)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.btn_import_students_sections = QtWidgets.QPushButton(
            self.w_table_section_student)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_import_students_sections.sizePolicy().hasHeightForWidth())
        self.btn_import_students_sections.setSizePolicy(sizePolicy)
        self.btn_import_students_sections.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_import_students_sections.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_import_students_sections.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_import_students_sections.setStyleSheet("border-radius: 5px")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            relative_path('Admin', ['Misc', 'Resources'], 'import.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_import_students_sections.setIcon(icon)
        self.btn_import_students_sections.setIconSize(QtCore.QSize(20, 20))
        self.btn_import_students_sections.setObjectName(
            "btn_import_students_sections")
        self.horizontalLayout_8.addWidget(self.btn_import_students_sections)
        self.btn_export_students_sections = QtWidgets.QPushButton(
            self.w_table_section_student)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_export_students_sections.sizePolicy().hasHeightForWidth())
        self.btn_export_students_sections.setSizePolicy(sizePolicy)
        self.btn_export_students_sections.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_export_students_sections.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_export_students_sections.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_export_students_sections.setStyleSheet("border-radius: 5px")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'export.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_export_students_sections.setIcon(icon1)
        self.btn_export_students_sections.setIconSize(QtCore.QSize(20, 20))
        self.btn_export_students_sections.setObjectName(
            "btn_export_students_sections")
        self.horizontalLayout_8.addWidget(self.btn_export_students_sections)
        self.btn_clear_students_sections_table = QtWidgets.QPushButton(
            self.w_table_section_student)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_clear_students_sections_table.sizePolicy().hasHeightForWidth())
        self.btn_clear_students_sections_table.setSizePolicy(sizePolicy)
        self.btn_clear_students_sections_table.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_clear_students_sections_table.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_clear_students_sections_table.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_students_sections_table.setStyleSheet("QPushButton{\n"
                                                             "    border-radius: 5px;\n"
                                                             "    background: none;\n"
                                                             "}\n"
                                                             "\n"
                                                             "\n"
                                                             "QPushButton:pressed {\n"
                                                             "     background-color: #072f49;\n"
                                                             "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'delete_table.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'delete_table_2.png')),
                        QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.btn_clear_students_sections_table.setIcon(icon2)
        self.btn_clear_students_sections_table.setIconSize(
            QtCore.QSize(20, 20))
        self.btn_clear_students_sections_table.setObjectName(
            "btn_clear_students_sections_table")
        self.horizontalLayout_8.addWidget(
            self.btn_clear_students_sections_table)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.line = QtWidgets.QFrame(self.w_table_section_student)
        self.line.setStyleSheet("color: #083654;")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.sw_student_section = QtWidgets.QStackedWidget(self.w_table_section_student)
        self.sw_student_section.setObjectName("sw_student_section")
        self.student_section_table = QtWidgets.QWidget()
        self.student_section_table.setObjectName("student_section_table")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(
            self.student_section_table)
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23.setSpacing(15)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_11.setSpacing(15)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.groupBox_2 = QtWidgets.QGroupBox(self.student_section_table)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_8.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_8.setSpacing(15)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_46 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_46.setSpacing(0)
        self.horizontalLayout_46.setObjectName("horizontalLayout_46")
        self.btn_init_section_bulk = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_section_bulk.sizePolicy().hasHeightForWidth())
        self.btn_init_section_bulk.setSizePolicy(sizePolicy)
        self.btn_init_section_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_section_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_section_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_section_bulk.setStyleSheet("border-radius: 5px")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'add_batch.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_init_section_bulk.setIcon(icon3)
        self.btn_init_section_bulk.setIconSize(QtCore.QSize(18, 18))
        self.btn_init_section_bulk.setObjectName("btn_init_section_bulk")
        self.horizontalLayout_46.addWidget(self.btn_init_section_bulk)
        spacerItem4 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_46.addItem(spacerItem4)
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_47.setSpacing(0)
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.txt_search_section = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_section.sizePolicy().hasHeightForWidth())
        self.txt_search_section.setSizePolicy(sizePolicy)
        self.txt_search_section.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_section.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_section.setFont(font)
        self.txt_search_section.setStyleSheet("border-radius: none;\n"
                                              "border-top-left-radius: 5px;\n"
                                              "border-bottom-left-radius: 5px;")
        self.txt_search_section.setObjectName("txt_search_section")
        self.horizontalLayout_47.addWidget(self.txt_search_section)
        self.btn_search_sections = QtWidgets.QPushButton(self.groupBox_2)
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'search.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search_sections.setIcon(icon4)
        self.btn_search_sections.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_sections.setObjectName("btn_search_sections")
        self.horizontalLayout_47.addWidget(self.btn_search_sections)
        self.horizontalLayout_46.addLayout(self.horizontalLayout_47)
        self.verticalLayout_8.addLayout(self.horizontalLayout_46)
        self.tv_sections = TableView(self.groupBox_2)
        self.tv_sections.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tv_sections.setObjectName("tv_sections")
        self.verticalLayout_8.addWidget(self.tv_sections)
        self.horizontalLayout_11.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.student_section_table)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_7.setSpacing(15)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_44.setSpacing(0)
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        self.btn_init_student_bulk = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_student_bulk.sizePolicy().hasHeightForWidth())
        self.btn_init_student_bulk.setSizePolicy(sizePolicy)
        self.btn_init_student_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_student_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_student_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_student_bulk.setStyleSheet("border-radius: 5px")
        self.btn_init_student_bulk.setIcon(icon3)
        self.btn_init_student_bulk.setIconSize(QtCore.QSize(18, 18))
        self.btn_init_student_bulk.setObjectName("btn_init_student_bulk")
        self.horizontalLayout_44.addWidget(self.btn_init_student_bulk)
        spacerItem5 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_44.addItem(spacerItem5)
        self.horizontalLayout_45 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_45.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_45.setSpacing(0)
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")
        self.txt_search_student = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_student.sizePolicy().hasHeightForWidth())
        self.txt_search_student.setSizePolicy(sizePolicy)
        self.txt_search_student.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_student.setMaximumSize(QtCore.QSize(280, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_student.setFont(font)
        self.txt_search_student.setStyleSheet("border-radius: none;\n"
                                              "border-top-left-radius: 5px;\n"
                                              "border-bottom-left-radius: 5px;")
        self.txt_search_student.setObjectName("txt_search_student")
        self.horizontalLayout_45.addWidget(self.txt_search_student)
        self.btn_search_students = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_students.sizePolicy().hasHeightForWidth())
        self.btn_search_students.setSizePolicy(sizePolicy)
        self.btn_search_students.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_students.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_students.setFont(font)
        self.btn_search_students.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_students.setStyleSheet("border-top-right-radius: 5px;\n"
                                               "border-bottom-right-radius: 5px;")
        self.btn_search_students.setText("")
        self.btn_search_students.setIcon(icon4)
        self.btn_search_students.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_students.setObjectName("btn_search_students")
        self.horizontalLayout_45.addWidget(self.btn_search_students)
        self.horizontalLayout_44.addLayout(self.horizontalLayout_45)
        self.verticalLayout_7.addLayout(self.horizontalLayout_44)
        self.tv_students = TableView(self.groupBox)
        self.tv_students.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tv_students.setObjectName("tv_students")
        self.verticalLayout_7.addWidget(self.tv_students)
        self.horizontalLayout_11.addWidget(self.groupBox)
        self.verticalLayout_23.addLayout(self.horizontalLayout_11)
        self.sw_student_section.addWidget(self.student_section_table)
        self.student_section_student_bulk = QtWidgets.QWidget()
        self.student_section_student_bulk.setObjectName(
            "student_section_student_bulk")

        self.verticalLayout_100 = QtWidgets.QVBoxLayout(self.student_section_student_bulk)
        self.verticalLayout_100.setContentsMargins(0,15,0,0)
        self.verticalLayout_100.setSpacing(15)

        self.horizontalLayout_100 = QtWidgets.QHBoxLayout()
        self.verticalLayout_100.addLayout(self.horizontalLayout_100)
        self.horizontalLayout_100.setContentsMargins(0,0,0,0)
        self.horizontalLayout_100.setSpacing(6)

        self.section_combobox = QtWidgets.QComboBox(self.student_section_student_bulk)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.section_combobox.setFont(font)
        self.section_combobox.setStyleSheet("QComboBox {\n"
                                            "     padding: 3px 7px;\n"
                                            "     border: 1px solid #0e4884;\n"
                                            "     border-radius: 5px;\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox:focus,\n"
                                            "QComboBox:hover {\n"
                                            "      border: 1px solid #256eff;\n"
                                            "      outline: none;\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox::drop-down {\n"
                                            "    subcontrol-origin: padding;\n"
                                            "    subcontrol-position: top right;\n"
                                            "    border: none;\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox::down-arrow {\n"
                                            f"   image: url({relative_path('SignIn', ['Misc', 'Resources'], 'down.png')});\n"
                                            "    padding-right: 10px;\n"
                                            "}\n"
                                            "\n"
                                            "QComboBox QAbstractItemView {\n"
                                            "    outline: none;\n"
                                            "}")
        self.horizontalLayout_100.addWidget(self.section_combobox)

        spacerItem10 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_100.addItem(spacerItem10)

        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.verticalLayout_100.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_27.setSpacing(6)
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.sa_student_bulk = QtWidgets.QScrollArea(
            self.student_section_student_bulk)
        self.sa_student_bulk.setStyleSheet("")
        self.sa_student_bulk.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_student_bulk.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.sa_student_bulk.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.sa_student_bulk.setWidgetResizable(True)
        self.sa_student_bulk.setObjectName("sa_student_bulk")
        self.widget_11 = QtWidgets.QWidget()
        self.widget_11.setGeometry(QtCore.QRect(0, 0, 521, 735))
        self.widget_11.setObjectName("widget_11")
        self.verticalLayout_38 = QtWidgets.QVBoxLayout(self.widget_11)
        self.verticalLayout_38.setContentsMargins(0, 0, 10, 0)
        self.verticalLayout_38.setSpacing(20)
        self.verticalLayout_38.setObjectName("verticalLayout_38")

        student_item = StudentItem(self)
        student_item.setObjectName(f"studentItem_1")
        self.verticalLayout_38.addWidget(student_item)

        student_item = StudentItem(self)
        student_item.setObjectName(f"studentItem_2")
        self.verticalLayout_38.addWidget(student_item)

        spacerItem6 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_38.addItem(spacerItem6)
        
        self.sa_student_bulk.setWidget(self.widget_11)
        self.horizontalLayout_27.addWidget(self.sa_student_bulk)
        self.verticalLayout_33 = QtWidgets.QVBoxLayout()
        self.verticalLayout_33.setSpacing(6)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.btn_add_student_bulk = QtWidgets.QPushButton(
            self.student_section_student_bulk)
        self.btn_add_student_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_add_student_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_add_student_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_student_bulk.setStyleSheet("QPushButton{\n"
                                                "  border-radius: 5px;"
                                                "}\n"
                                                "QPushButton::disabled {\n"
                                                "  border: 1px solid #0b1a30;\n"
                                                "  background-color: #0b1a30;\n"
                                                "}\n")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'check.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'check_2.png')),
                        QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.btn_add_student_bulk.setIcon(icon5)
        self.btn_add_student_bulk.setIconSize(QtCore.QSize(19, 19))
        self.btn_add_student_bulk.setObjectName("btn_add_student_bulk")
        self.verticalLayout_33.addWidget(self.btn_add_student_bulk)
        self.btn_add_student_item = QtWidgets.QPushButton(
            self.student_section_student_bulk)
        self.btn_add_student_item.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_add_student_item.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_add_student_item.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_student_item.setStyleSheet("border-radius: 5px;\n"
                                                f"background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                "background-repeat: no-repeat;\n"
                                                "background-position: center center;")
        self.btn_add_student_item.setIconSize(QtCore.QSize(17, 17))
        self.btn_add_student_item.setObjectName("btn_add_student_item")
        self.verticalLayout_33.addWidget(self.btn_add_student_item)
        self.btn_clear_student_items = QtWidgets.QPushButton(
            self.student_section_student_bulk)
        self.btn_clear_student_items.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_student_items.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_student_items.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_student_items.setStyleSheet("QPushButton{\n"
                                                   "    border-radius: 5px;\n"
                                                   "    background: none;\n"
                                                   "}\n"
                                                   "\n"
                                                   "\n"
                                                   "QPushButton:pressed {\n"
                                                   "     background-color: #072f49;\n"
                                                   "}")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'clear.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_clear_student_items.setIcon(icon6)
        self.btn_clear_student_items.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_student_items.setObjectName("btn_clear_student_items")
        self.verticalLayout_33.addWidget(self.btn_clear_student_items)
        self.btn_back_student_bulk = QtWidgets.QPushButton(
            self.student_section_student_bulk)
        self.btn_back_student_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_back_student_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_back_student_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_back_student_bulk.setStyleSheet("QPushButton{\n"
                                                 "    border: none;\n"
                                                 "    border-radius: none;\n"
                                                 "    background: none;\n"
                                                 "    background-repeat: none;\n"
                                                 f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'left.png')});\n"
                                                 "    background-position: center center;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover{\n"
                                                 "    background: none;\n"
                                                 "    background-repeat: none;\n"
                                                 f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'left_2.png')});\n"
                                                 "    background-position: center center;\n"
                                                 "}")
        self.btn_back_student_bulk.setObjectName("btn_back_student_bulk")
        self.verticalLayout_33.addWidget(self.btn_back_student_bulk)
        spacerItem7 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_33.addItem(spacerItem7)
        self.horizontalLayout_27.addLayout(self.verticalLayout_33)
        self.sw_student_section.addWidget(self.student_section_student_bulk)
        self.student_section_section_bulk = QtWidgets.QWidget()
        self.student_section_section_bulk.setObjectName(
            "student_section_section_bulk")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(
            self.student_section_section_bulk)
        self.horizontalLayout_9.setContentsMargins(0, 15, 0, 0)
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.sa_section_bulk = QtWidgets.QScrollArea(
            self.student_section_section_bulk)
        self.sa_section_bulk.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_section_bulk.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.sa_section_bulk.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.sa_section_bulk.setWidgetResizable(True)
        self.sa_section_bulk.setObjectName("sa_section_bulk")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(
            QtCore.QRect(0, 0, 521, 735))
        self.scrollAreaWidgetContents_5.setObjectName(
            "scrollAreaWidgetContents_5")
        self.verticalLayout_53 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_5)
        self.verticalLayout_53.setContentsMargins(0, 0, 10, 0)
        self.verticalLayout_53.setSpacing(20)
        self.verticalLayout_53.setObjectName("verticalLayout_53")

        sectionItem = SectionItem(self)
        sectionItem.setObjectName(f"sectionItem_1")
        self.verticalLayout_53.addWidget(sectionItem)

        sectionItem = SectionItem(self)
        sectionItem.setObjectName(f"sectionItem_2")
        self.verticalLayout_53.addWidget(sectionItem)

        spacerItem8 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_53.addItem(spacerItem8)

        self.sa_section_bulk.setWidget(self.scrollAreaWidgetContents_5)
        self.horizontalLayout_9.addWidget(self.sa_section_bulk)
        self.verticalLayout_52 = QtWidgets.QVBoxLayout()
        self.verticalLayout_52.setSpacing(6)
        self.verticalLayout_52.setObjectName("verticalLayout_52")
        self.btn_add_section_bulk = QtWidgets.QPushButton(
            self.student_section_section_bulk)
        self.btn_add_section_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_add_section_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_add_section_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_section_bulk.setStyleSheet("QPushButton{\n"
                                                "  border-radius: 5px;"
                                                "}\n"
                                                "QPushButton::disabled {\n"
                                                "  border: 1px solid #0b1a30;\n"
                                                "  background-color: #0b1a30;\n"
                                                "}\n")
        self.btn_add_section_bulk.setIcon(icon5)
        self.btn_add_section_bulk.setIconSize(QtCore.QSize(19, 19))
        self.btn_add_section_bulk.setObjectName("btn_add_section_bulk")
        self.verticalLayout_52.addWidget(self.btn_add_section_bulk)
        self.btn_add_section_item = QtWidgets.QPushButton(
            self.student_section_section_bulk)
        self.btn_add_section_item.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_add_section_item.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_add_section_item.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_section_item.setStyleSheet("border-radius: 5px;\n"
                                                f"background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                "background-repeat: no-repeat;\n"
                                                "background-position: center center;")
        self.btn_add_section_item.setIconSize(QtCore.QSize(17, 17))
        self.btn_add_section_item.setObjectName("btn_add_section_item")
        self.verticalLayout_52.addWidget(self.btn_add_section_item)
        self.btn_clear_section_items = QtWidgets.QPushButton(
            self.student_section_section_bulk)
        self.btn_clear_section_items.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_section_items.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_section_items.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_section_items.setStyleSheet("QPushButton{\n"
                                                   "    border-radius: 5px;\n"
                                                   "    background: none;\n"
                                                   "}\n"
                                                   "\n"
                                                   "\n"
                                                   "QPushButton:pressed {\n"
                                                   "     background-color: #072f49;\n"
                                                   "}")
        self.btn_clear_section_items.setIcon(icon6)
        self.btn_clear_section_items.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_section_items.setObjectName("btn_clear_section_items")
        self.verticalLayout_52.addWidget(self.btn_clear_section_items)
        self.btn_back_section_bulk = QtWidgets.QPushButton(
            self.student_section_section_bulk)
        self.btn_back_section_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_back_section_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_back_section_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_back_section_bulk.setStyleSheet("QPushButton{\n"
                                                 "    border: none;\n"
                                                 "    border-radius: none;\n"
                                                 "    background: none;\n"
                                                 "    background-repeat: none;\n"
                                                 f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'left.png')});\n"
                                                 "    background-position: center center;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover{\n"
                                                 "    background: none;\n"
                                                 "    background-repeat: none;\n"
                                                 f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'left_2.png')});\n"
                                                 "    background-position: center center;\n"
                                                 "}")
        self.btn_back_section_bulk.setObjectName("btn_back_section_bulk")
        self.verticalLayout_52.addWidget(self.btn_back_section_bulk)
        spacerItem9 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_52.addItem(spacerItem9)
        self.horizontalLayout_9.addLayout(self.verticalLayout_52)
        self.sw_student_section.addWidget(self.student_section_section_bulk)
        self.verticalLayout_6.addWidget(self.sw_student_section)
        self.horizontalLayout_3.addWidget(self.w_table_section_student)
        self.widget_5 = QtWidgets.QWidget(self.section_student)
        self.widget_5.setMinimumSize(QtCore.QSize(234, 0))
        self.widget_5.setMaximumSize(QtCore.QSize(380, 16777215))
        self.widget_5.setStyleSheet("QWidget{\n"
                                    "    background: #083654;\n"
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
                                    "QLineEdit::disabled {\n"
                                    "   border: 1px solid #072f49;\n"
                                    "   border-radius: 5px;\n"
                                    "   background-color: #072f49;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::disabled {\n"
                                    "  padding: 5px;\n"
                                    "  border: 1px solid #102542;\n"
                                    "  background-color: #102542;\n"
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
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_39 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_39.setSpacing(0)
        self.verticalLayout_39.setObjectName("verticalLayout_39")
        self.w_section_input = QtWidgets.QWidget(self.widget_5)
        self.w_section_input.setObjectName("w_section_input")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.w_section_input)
        self.verticalLayout_12.setContentsMargins(15, 15, 15, 20)
        self.verticalLayout_12.setSpacing(15)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setSpacing(6)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_11 = QtWidgets.QLabel(self.w_section_input)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("letter-spacing: 0.5px")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setIndent(1)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_13.addWidget(self.label_11)
        spacerItem10 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem10)
        self.btn_init_add_section = QtWidgets.QPushButton(self.w_section_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_add_section.sizePolicy().hasHeightForWidth())
        self.btn_init_add_section.setSizePolicy(sizePolicy)
        self.btn_init_add_section.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_add_section.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_add_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_section.setStyleSheet("QPushButton{\n"
                                                "    border-radius: 5px;\n"
                                                f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                "    background-repeat: no-repeat;\n"
                                                "    background-position: center center;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton::disabled{\n"
                                                "    border-radius: 5px;\n"
                                                f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add_2.png')});\n"
                                                "    background-repeat: no-repeat;\n"
                                                "    background-position: center center;\n"
                                                "}")
        self.btn_init_add_section.setIconSize(QtCore.QSize(17, 17))
        self.btn_init_add_section.setObjectName("btn_init_add_section")
        self.horizontalLayout_13.addWidget(self.btn_init_add_section)
        self.btn_init_edit_section = QtWidgets.QPushButton(
            self.w_section_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_edit_section.sizePolicy().hasHeightForWidth())
        self.btn_init_edit_section.setSizePolicy(sizePolicy)
        self.btn_init_edit_section.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_section.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_edit_section.setStyleSheet("border-radius: 5px")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'edit.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon7.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'edit_2.png')),
                        QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.btn_init_edit_section.setIcon(icon7)
        self.btn_init_edit_section.setIconSize(QtCore.QSize(20, 20))
        self.btn_init_edit_section.setObjectName("btn_init_edit_section")
        self.horizontalLayout_13.addWidget(self.btn_init_edit_section)
        self.btn_delete_section = QtWidgets.QPushButton(self.w_section_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_delete_section.sizePolicy().hasHeightForWidth())
        self.btn_delete_section.setSizePolicy(sizePolicy)
        self.btn_delete_section.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_section.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_section.setStyleSheet("QPushButton{\n"
                                              "    border-radius: 5px;\n"
                                              "    background: none;\n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "     background-color: #072f49;\n"
                                              "}")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'trash.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon8.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'trash_2.png')),
                        QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.btn_delete_section.setIcon(icon8)
        self.btn_delete_section.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_section.setObjectName("btn_delete_section")
        self.horizontalLayout_13.addWidget(self.btn_delete_section)
        self.verticalLayout_12.addLayout(self.horizontalLayout_13)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_13.setSpacing(6)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_12 = QtWidgets.QLabel(self.w_section_input)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setIndent(1)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_13.addWidget(self.label_12)
        self.txt_section_name = QtWidgets.QLineEdit(self.w_section_input)
        self.txt_section_name.setEnabled(False)
        self.txt_section_name.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_section_name.setFont(font)
        self.txt_section_name.setObjectName("txt_section_name")
        self.verticalLayout_13.addWidget(self.txt_section_name)
        self.verticalLayout_12.addLayout(self.verticalLayout_13)
        self.w_section_btn = QtWidgets.QWidget(self.w_section_input)
        self.w_section_btn.setObjectName("w_section_btn")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.w_section_btn)
        self.verticalLayout_14.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_14.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.btn_add_edit_section = QtWidgets.QPushButton(self.w_section_btn)
        self.btn_add_edit_section.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_add_edit_section.setFont(font)
        self.btn_add_edit_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_edit_section.setStyleSheet("border-radius: 5px;")
        self.btn_add_edit_section.setObjectName("btn_add_edit_section")
        self.verticalLayout_14.addWidget(self.btn_add_edit_section)
        self.btn_cancel_section = QtWidgets.QPushButton(self.w_section_btn)
        self.btn_cancel_section.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_cancel_section.setFont(font)
        self.btn_cancel_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel_section.setStyleSheet("QPushButton{\n"
                                              "    border-radius: 5px;\n"
                                              "    background: none;\n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "     background-color: #072f49;\n"
                                              "}")
        self.btn_cancel_section.setObjectName("btn_cancel_section")
        self.verticalLayout_14.addWidget(self.btn_cancel_section)
        self.verticalLayout_12.addWidget(self.w_section_btn)
        self.verticalLayout_39.addWidget(self.w_section_input)
        self.line_3 = QtWidgets.QFrame(self.widget_5)
        self.line_3.setStyleSheet("color: #0e4177;")
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_39.addWidget(self.line_3)

        self.w_section_student = QtWidgets.QWidget(self.widget_5)
        self.w_section_student.setObjectName("w_section_student")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.w_section_student)
        self.verticalLayout_15.setContentsMargins(15, 20, 15, 15)
        self.verticalLayout_15.setSpacing(15)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setSpacing(6)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.lbl_section_students_status = QtWidgets.QLabel(
            self.w_section_student)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_section_students_status.setFont(font)
        self.lbl_section_students_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_section_students_status.setIndent(1)
        self.lbl_section_students_status.setObjectName(
            "lbl_section_students_status")
        self.horizontalLayout_20.addWidget(self.lbl_section_students_status)
        spacerItem12 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem12)
        self.btn_init_add_section_student = QtWidgets.QPushButton(
            self.w_section_student)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_add_section_student.sizePolicy().hasHeightForWidth())
        self.btn_init_add_section_student.setSizePolicy(sizePolicy)
        self.btn_init_add_section_student.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_add_section_student.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_add_section_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_section_student.setStyleSheet("QPushButton{\n"
                                                        "    border-radius: 5px;\n"
                                                        f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                        "    background-repeat: no-repeat;\n"
                                                        "    background-position: center center;\n"
                                                        "}\n"
                                                        "\n"
                                                        "QPushButton::disabled{\n"
                                                        "    border-radius: 5px;\n"
                                                        f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add_2.png')});\n"
                                                        "    background-repeat: no-repeat;\n"
                                                        "    background-position: center center;\n"
                                                        "}")
        self.btn_init_add_section_student.setIconSize(QtCore.QSize(17, 17))
        self.btn_init_add_section_student.setObjectName(
            "btn_init_add_section_student")
        self.horizontalLayout_20.addWidget(self.btn_init_add_section_student)
        self.btn_delete_section_student = QtWidgets.QPushButton(
            self.w_section_student)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_delete_section_student.sizePolicy().hasHeightForWidth())
        self.btn_delete_section_student.setSizePolicy(sizePolicy)
        self.btn_delete_section_student.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_section_student.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_section_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_section_student.setStyleSheet("QPushButton{\n"
                                                      "    border-radius: 5px;\n"
                                                      "    background: none;\n"
                                                      "}\n"
                                                      "\n"
                                                      "\n"
                                                      "QPushButton:pressed {\n"
                                                      "     background-color: #072f49;\n"
                                                      "}")
        self.btn_delete_section_student.setIcon(icon8)
        self.btn_delete_section_student.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_section_student.setObjectName(
            "btn_delete_section_student")
        self.horizontalLayout_20.addWidget(self.btn_delete_section_student)
        self.btn_clear_section_student_table = QtWidgets.QPushButton(
            self.w_section_student)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_clear_section_student_table.sizePolicy().hasHeightForWidth())
        self.btn_clear_section_student_table.setSizePolicy(sizePolicy)
        self.btn_clear_section_student_table.setMinimumSize(
            QtCore.QSize(30, 30))
        self.btn_clear_section_student_table.setMaximumSize(
            QtCore.QSize(30, 30))
        self.btn_clear_section_student_table.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_section_student_table.setStyleSheet("QPushButton{\n"
                                                           "    border-radius: 5px;\n"
                                                           "    background: none;\n"
                                                           "}\n"
                                                           "\n"
                                                           "\n"
                                                           "QPushButton:pressed {\n"
                                                           "     background-color: #072f49;\n"
                                                           "}")
        self.btn_clear_section_student_table.setIcon(icon2)
        self.btn_clear_section_student_table.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_section_student_table.setObjectName(
            "btn_clear_section_student_table")
        self.horizontalLayout_20.addWidget(
            self.btn_clear_section_student_table)
        self.verticalLayout_15.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_55 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_55.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_55.setSpacing(0)
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")
        self.txt_search_section_student = QtWidgets.QLineEdit(
            self.w_section_student)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_section_student.sizePolicy().hasHeightForWidth())
        self.txt_search_section_student.setSizePolicy(sizePolicy)
        self.txt_search_section_student.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_section_student.setMaximumSize(
            QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_section_student.setFont(font)
        self.txt_search_section_student.setStyleSheet("border-radius: none;\n"
                                                      "border-top-left-radius: 5px;\n"
                                                      "border-bottom-left-radius: 5px;")
        self.txt_search_section_student.setObjectName(
            "txt_search_section_student")
        self.horizontalLayout_55.addWidget(self.txt_search_section_student)
        self.btn_search_section_student = QtWidgets.QPushButton(
            self.w_section_student)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_section_student.sizePolicy().hasHeightForWidth())
        self.btn_search_section_student.setSizePolicy(sizePolicy)
        self.btn_search_section_student.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_section_student.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_section_student.setFont(font)
        self.btn_search_section_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_section_student.setStyleSheet("border-top-right-radius: 5px;\n"
                                                      "border-bottom-right-radius: 5px;")
        self.btn_search_section_student.setText("")
        self.btn_search_section_student.setIcon(icon4)
        self.btn_search_section_student.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_section_student.setObjectName(
            "btn_search_section_student")
        self.horizontalLayout_55.addWidget(self.btn_search_section_student)
        self.verticalLayout_15.addLayout(self.horizontalLayout_55)
        self.lv_section_student = ListView(self.w_section_student)
        self.lv_section_student.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lv_section_student.setObjectName("lv_section_student")
        self.verticalLayout_15.addWidget(self.lv_section_student)
        self.verticalLayout_39.addWidget(self.w_section_student)

        self.line_4 = QtWidgets.QFrame(self.widget_5)
        self.line_4.setStyleSheet("color: #0e4177;")
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setLineWidth(2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_39.addWidget(self.line_4)

        self.w_student_input = QtWidgets.QWidget(self.widget_5)
        self.w_student_input.setObjectName("w_student_input")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.w_student_input)
        self.verticalLayout_11.setContentsMargins(15, 20, 15, 20)
        self.verticalLayout_11.setSpacing(15)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_7 = QtWidgets.QLabel(self.w_student_input)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("letter-spacing: 0.5px")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setIndent(1)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_12.addWidget(self.label_7)
        spacerItem11 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem11)
        self.btn_init_add_student = QtWidgets.QPushButton(self.w_student_input)
        self.btn_init_add_student.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_add_student.sizePolicy().hasHeightForWidth())
        self.btn_init_add_student.setSizePolicy(sizePolicy)
        self.btn_init_add_student.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_add_student.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_add_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_student.setStyleSheet("QPushButton{\n"
                                                "    border-radius: 5px;\n"
                                                f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                "    background-repeat: no-repeat;\n"
                                                "    background-position: center center;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton::disabled{\n"
                                                "    border-radius: 5px;\n"
                                                f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add_2.png')});\n"
                                                "    background-repeat: no-repeat;\n"
                                                "    background-position: center center;\n"
                                                "}")
        self.btn_init_add_student.setIconSize(QtCore.QSize(17, 17))
        self.btn_init_add_student.setObjectName("btn_init_add_student")
        self.horizontalLayout_12.addWidget(self.btn_init_add_student)
        self.btn_init_edit_student = QtWidgets.QPushButton(
            self.w_student_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_edit_student.sizePolicy().hasHeightForWidth())
        self.btn_init_edit_student.setSizePolicy(sizePolicy)
        self.btn_init_edit_student.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_student.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_edit_student.setStyleSheet("border-radius: 5px")
        self.btn_init_edit_student.setIcon(icon7)
        self.btn_init_edit_student.setIconSize(QtCore.QSize(20, 20))
        self.btn_init_edit_student.setObjectName("btn_init_edit_student")
        self.horizontalLayout_12.addWidget(self.btn_init_edit_student)
        self.btn_delete_student = QtWidgets.QPushButton(self.w_student_input)
        self.btn_delete_student.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_delete_student.sizePolicy().hasHeightForWidth())
        self.btn_delete_student.setSizePolicy(sizePolicy)
        self.btn_delete_student.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_student.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_student.setStyleSheet("QPushButton{\n"
                                              "    border-radius: 5px;\n"
                                              "    background: none;\n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "     background-color: #072f49;\n"
                                              "}")
        self.btn_delete_student.setIcon(icon8)
        self.btn_delete_student.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_student.setObjectName("btn_delete_student")
        self.horizontalLayout_12.addWidget(self.btn_delete_student)
        self.verticalLayout_11.addLayout(self.horizontalLayout_12)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.w_student_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setIndent(1)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_9.addWidget(self.label_8)
        self.txt_student_username = QtWidgets.QLineEdit(self.w_student_input)
        self.txt_student_username.setEnabled(False)
        self.txt_student_username.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_student_username.setFont(font)
        self.txt_student_username.setObjectName("txt_student_username")
        self.verticalLayout_9.addWidget(self.txt_student_username)
        self.label_10 = QtWidgets.QLabel(self.w_student_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setIndent(1)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_9.addWidget(self.label_10)
        self.txt_student_password = PasswordGenerator(self.w_student_input)
        self.txt_student_password.setEnabled(False)
        self.txt_student_password.setReadOnly(True)
        self.txt_student_password.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_student_password.setFont(font)
        self.txt_student_password.setObjectName("txt_student_password")
        self.verticalLayout_9.addWidget(self.txt_student_password)
        self.verticalLayout_11.addLayout(self.verticalLayout_9)
        self.w_student_btn = QtWidgets.QWidget(self.w_student_input)
        self.w_student_btn.setObjectName("w_student_btn")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.w_student_btn)
        self.verticalLayout_10.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_10.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.btn_add_edit_student = QtWidgets.QPushButton(self.w_student_btn)
        self.btn_add_edit_student.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_add_edit_student.setFont(font)
        self.btn_add_edit_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_edit_student.setStyleSheet("border-radius: 5px;")
        self.btn_add_edit_student.setObjectName("btn_add_edit_student")
        self.verticalLayout_10.addWidget(self.btn_add_edit_student)
        self.btn_cancel_student = QtWidgets.QPushButton(self.w_student_btn)
        self.btn_cancel_student.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_cancel_student.setFont(font)
        self.btn_cancel_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel_student.setStyleSheet("QPushButton{\n"
                                              "    border-radius: 5px;\n"
                                              "    background: none;\n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "     background-color: #072f49;\n"
                                              "}")
        self.btn_cancel_student.setObjectName("btn_cancel_student")
        self.verticalLayout_10.addWidget(self.btn_cancel_student)
        self.verticalLayout_11.addWidget(self.w_student_btn)
        self.verticalLayout_39.addWidget(self.w_student_input)

        self.horizontalLayout_3.addWidget(self.widget_5)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)
        self.sw_all.addWidget(self.section_student)
        self.teacher = QtWidgets.QWidget()
        self.teacher.setObjectName("teacher")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.teacher)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(15)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.w_table_teacher = QtWidgets.QWidget(self.teacher)
        self.w_table_teacher.setMinimumSize(QtCore.QSize(377, 0))
        self.w_table_teacher.setStyleSheet("QWidget{\n"
                                    "    background: #102542;\n"
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
        self.w_table_teacher.setObjectName("w_table_teacher")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.w_table_teacher)
        self.verticalLayout_16.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_16.setSpacing(5)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_14.setSpacing(6)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.lbl_teachers_table_status = QtWidgets.QLabel(self.w_table_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_teachers_table_status.sizePolicy().hasHeightForWidth())
        self.lbl_teachers_table_status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_teachers_table_status.setFont(font)
        self.lbl_teachers_table_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_teachers_table_status.setIndent(1)
        self.lbl_teachers_table_status.setObjectName(
            "lbl_teachers_table_status")
        self.horizontalLayout_14.addWidget(self.lbl_teachers_table_status)
        spacerItem13 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem13)
        self.btn_import_teachers = QtWidgets.QPushButton(self.w_table_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_import_teachers.sizePolicy().hasHeightForWidth())
        self.btn_import_teachers.setSizePolicy(sizePolicy)
        self.btn_import_teachers.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_import_teachers.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_import_teachers.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_import_teachers.setStyleSheet("border-radius: 5px")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'import.png')),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_import_teachers.setIcon(icon11)
        self.btn_import_teachers.setIconSize(QtCore.QSize(20, 20))
        self.btn_import_teachers.setObjectName("btn_import_teachers")
        self.horizontalLayout_14.addWidget(self.btn_import_teachers)
        self.btn_export_teachers = QtWidgets.QPushButton(self.w_table_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_export_teachers.sizePolicy().hasHeightForWidth())
        self.btn_export_teachers.setSizePolicy(sizePolicy)
        self.btn_export_teachers.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_export_teachers.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_export_teachers.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_export_teachers.setStyleSheet("border-radius: 5px")
        self.btn_export_teachers.setIcon(icon1)
        self.btn_export_teachers.setIconSize(QtCore.QSize(20, 20))
        self.btn_export_teachers.setObjectName("btn_export_teachers")
        self.horizontalLayout_14.addWidget(self.btn_export_teachers)
        self.btn_clear_teachers_table = QtWidgets.QPushButton(self.w_table_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_clear_teachers_table.sizePolicy().hasHeightForWidth())
        self.btn_clear_teachers_table.setSizePolicy(sizePolicy)
        self.btn_clear_teachers_table.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_teachers_table.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_teachers_table.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_teachers_table.setStyleSheet("QPushButton{\n"
                                                    "    border-radius: 5px;\n"
                                                    "    background: none;\n"
                                                    "}\n"
                                                    "\n"
                                                    "\n"
                                                    "QPushButton:pressed {\n"
                                                    "     background-color: #072f49;\n"
                                                    "}")
        self.btn_clear_teachers_table.setIcon(icon2)
        self.btn_clear_teachers_table.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_teachers_table.setObjectName("btn_clear_teachers_table")
        self.horizontalLayout_14.addWidget(self.btn_clear_teachers_table)
        self.verticalLayout_16.addLayout(self.horizontalLayout_14)
        self.line_2 = QtWidgets.QFrame(self.w_table_teacher)
        self.line_2.setStyleSheet("color: #083654;")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_16.addWidget(self.line_2)
        self.sw_teacher_attendance = QtWidgets.QStackedWidget(self.w_table_teacher)
        self.sw_teacher_attendance.setObjectName("sw_teacher_attendance")
        self.teacher_table = QtWidgets.QWidget()
        self.teacher_table.setObjectName("teacher_table")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.teacher_table)
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_24.setSpacing(15)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setSpacing(15)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.groupBox_3 = QtWidgets.QGroupBox(self.teacher_table)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_17.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_17.setSpacing(15)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_48.setSpacing(0)
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")
        self.btn_init_teachers_bulk = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_teachers_bulk.sizePolicy().hasHeightForWidth())
        self.btn_init_teachers_bulk.setSizePolicy(sizePolicy)
        self.btn_init_teachers_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_teachers_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_teachers_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_teachers_bulk.setStyleSheet("border-radius: 5px")
        self.btn_init_teachers_bulk.setIcon(icon3)
        self.btn_init_teachers_bulk.setIconSize(QtCore.QSize(18, 18))
        self.btn_init_teachers_bulk.setObjectName("btn_init_teachers_bulk")
        self.horizontalLayout_48.addWidget(self.btn_init_teachers_bulk)
        spacerItem14 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_48.addItem(spacerItem14)
        self.horizontalLayout_49 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_49.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_49.setSpacing(0)
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        self.txt_search_teacher = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_teacher.sizePolicy().hasHeightForWidth())
        self.txt_search_teacher.setSizePolicy(sizePolicy)
        self.txt_search_teacher.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_teacher.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_teacher.setFont(font)
        self.txt_search_teacher.setStyleSheet("border-radius: none;\n"
                                              "border-top-left-radius: 5px;\n"
                                              "border-bottom-left-radius: 5px;")
        self.txt_search_teacher.setObjectName("txt_search_teacher")
        self.horizontalLayout_49.addWidget(self.txt_search_teacher)
        self.btn_search_teacher = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_teacher.sizePolicy().hasHeightForWidth())
        self.btn_search_teacher.setSizePolicy(sizePolicy)
        self.btn_search_teacher.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_teacher.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_teacher.setFont(font)
        self.btn_search_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_teacher.setStyleSheet("border-top-right-radius: 5px;\n"
                                                  "border-bottom-right-radius: 5px;")
        self.btn_search_teacher.setText("")
        self.btn_search_teacher.setIcon(icon4)
        self.btn_search_teacher.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_teacher.setObjectName("btn_search_teacher")
        self.horizontalLayout_49.addWidget(self.btn_search_teacher)
        self.horizontalLayout_48.addLayout(self.horizontalLayout_49)
        self.verticalLayout_17.addLayout(self.horizontalLayout_48)
        self.tv_teachers = TableView(self.groupBox_3)
        self.tv_teachers.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tv_teachers.setObjectName("tv_teachers")
        self.verticalLayout_17.addWidget(self.tv_teachers)
        self.horizontalLayout_17.addWidget(self.groupBox_3)
        self.verticalLayout_24.addLayout(self.horizontalLayout_17)
        self.sw_teacher_attendance.addWidget(self.teacher_table)
        self.teacher_teacher_bulk = QtWidgets.QWidget()
        self.teacher_teacher_bulk.setObjectName("teacher_teacher_bulk")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout(
            self.teacher_teacher_bulk)
        self.horizontalLayout_29.setContentsMargins(0, 15, 0, 0)
        self.horizontalLayout_29.setSpacing(6)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.sa_teacher_bulk = QtWidgets.QScrollArea(self.teacher_teacher_bulk)
        self.sa_teacher_bulk.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sa_teacher_bulk.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.sa_teacher_bulk.setWidgetResizable(True)
        self.sa_teacher_bulk.setObjectName("sa_teacher_bulk")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 44, 16))
        self.scrollAreaWidgetContents_3.setObjectName(
            "scrollAreaWidgetContents_3")
        self.verticalLayout_47 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_3)
        self.verticalLayout_47.setContentsMargins(0, 0, 10, 0)
        self.verticalLayout_47.setSpacing(20)
        self.verticalLayout_47.setObjectName("verticalLayout_47")

        teacher_item = TeacherItem(self)
        teacher_item.setObjectName("teacherItem_1")
        self.verticalLayout_47.addWidget(teacher_item)

        teacher_item = TeacherItem(self)
        teacher_item.setObjectName("teacherItem_2")
        self.verticalLayout_47.addWidget(teacher_item)

        spacerItem15 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_47.addItem(spacerItem15)

        self.sa_teacher_bulk.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_29.addWidget(self.sa_teacher_bulk)
        self.verticalLayout_34 = QtWidgets.QVBoxLayout()
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.btn_add_teacher_bulk = QtWidgets.QPushButton(
            self.teacher_teacher_bulk)
        self.btn_add_teacher_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_add_teacher_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_add_teacher_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_teacher_bulk.setStyleSheet("QPushButton{\n"
                                                "  border-radius: 5px;"
                                                "}\n"
                                                "QPushButton::disabled {\n"
                                                "  border: 1px solid #0b1a30;\n"
                                                "  background-color: #0b1a30;\n"
                                                "}\n")
        self.btn_add_teacher_bulk.setIcon(icon5)
        self.btn_add_teacher_bulk.setIconSize(QtCore.QSize(19, 19))
        self.btn_add_teacher_bulk.setObjectName("btn_add_teacher_bulk")
        self.verticalLayout_34.addWidget(self.btn_add_teacher_bulk)
        self.btn_add_teacher_item = QtWidgets.QPushButton(
            self.teacher_teacher_bulk)
        self.btn_add_teacher_item.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_add_teacher_item.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_add_teacher_item.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_teacher_item.setStyleSheet("border-radius: 5px;\n"
                                                f"background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                "background-repeat: no-repeat;\n"
                                                "background-position: center center;")
        self.btn_add_teacher_item.setIconSize(QtCore.QSize(17, 17))
        self.btn_add_teacher_item.setObjectName("btn_add_teacher_item")
        self.verticalLayout_34.addWidget(self.btn_add_teacher_item)
        self.btn_clear_teacher_item = QtWidgets.QPushButton(
            self.teacher_teacher_bulk)
        self.btn_clear_teacher_item.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_teacher_item.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_teacher_item.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_teacher_item.setStyleSheet("QPushButton{\n"
                                                  "    border-radius: 5px;\n"
                                                  "    background: none;\n"
                                                  "}\n"
                                                  "\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "     background-color: #072f49;\n"
                                                  "}")
        self.btn_clear_teacher_item.setIcon(icon6)
        self.btn_clear_teacher_item.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_teacher_item.setObjectName("btn_clear_teacher_item")
        self.verticalLayout_34.addWidget(self.btn_clear_teacher_item)
        self.btn_back_teacher_bulk = QtWidgets.QPushButton(
            self.teacher_teacher_bulk)
        self.btn_back_teacher_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_back_teacher_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_back_teacher_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_back_teacher_bulk.setStyleSheet("QPushButton{\n"
                                                 "    border: none;\n"
                                                 "    border-radius: none;\n"
                                                 "    background: none;\n"
                                                 "    background-repeat: none;\n"
                                                 f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'left.png')});\n"
                                                 "    background-position: center center;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover{\n"
                                                 "    background: none;\n"
                                                 "    background-repeat: none;\n"
                                                 f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'left_2.png')});\n"
                                                 "    background-position: center center;\n"
                                                 "}")
        self.btn_back_teacher_bulk.setObjectName("btn_back_teacher_bulk")
        self.verticalLayout_34.addWidget(self.btn_back_teacher_bulk)
        spacerItem16 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_34.addItem(spacerItem16)
        self.horizontalLayout_29.addLayout(self.verticalLayout_34)
        self.sw_teacher_attendance.addWidget(self.teacher_teacher_bulk)
        self.verticalLayout_16.addWidget(self.sw_teacher_attendance)
        self.horizontalLayout_4.addWidget(self.w_table_teacher)
        self.widget_7 = QtWidgets.QWidget(self.teacher)
        self.widget_7.setMinimumSize(QtCore.QSize(234, 0))
        self.widget_7.setMaximumSize(QtCore.QSize(380, 16777215))
        self.widget_7.setStyleSheet("QWidget{\n"
                                    "    background: #083654;\n"
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
                                    "QLineEdit::disabled {\n"
                                    "   border: 1px solid #072f49;\n"
                                    "   border-radius: 5px;\n"
                                    "   background-color: #072f49;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::disabled {\n"
                                    "  padding: 5px;\n"
                                    "  border: 1px solid #102542;\n"
                                    "  background-color: #102542;\n"
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
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_40 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_40.setSpacing(0)
        self.verticalLayout_40.setObjectName("verticalLayout_40")
        self.w_teacher_input = QtWidgets.QWidget(self.widget_7)
        self.w_teacher_input.setObjectName("w_teacher_input")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.w_teacher_input)
        self.verticalLayout_19.setContentsMargins(15, 15, 15, 20)
        self.verticalLayout_19.setSpacing(15)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setSpacing(6)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_15 = QtWidgets.QLabel(self.w_teacher_input)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("letter-spacing: 0.5px")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setIndent(1)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_18.addWidget(self.label_15)
        spacerItem17 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem17)
        self.btn_init_add_teacher = QtWidgets.QPushButton(self.w_teacher_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_add_teacher.sizePolicy().hasHeightForWidth())
        self.btn_init_add_teacher.setSizePolicy(sizePolicy)
        self.btn_init_add_teacher.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_add_teacher.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_add_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_teacher.setStyleSheet("QPushButton{\n"
                                                "    border-radius: 5px;\n"
                                                f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                "    background-repeat: no-repeat;\n"
                                                "    background-position: center center;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton::disabled{\n"
                                                "    border-radius: 5px;\n"
                                                f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add_2.png')});\n"
                                                "    background-repeat: no-repeat;\n"
                                                "    background-position: center center;\n"
                                                "}")
        self.btn_init_add_teacher.setIconSize(QtCore.QSize(17, 17))
        self.btn_init_add_teacher.setObjectName("btn_init_add_teacher")
        self.horizontalLayout_18.addWidget(self.btn_init_add_teacher)
        self.btn_init_edit_teacher = QtWidgets.QPushButton(
            self.w_teacher_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_edit_teacher.sizePolicy().hasHeightForWidth())
        self.btn_init_edit_teacher.setSizePolicy(sizePolicy)
        self.btn_init_edit_teacher.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_teacher.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_edit_teacher.setStyleSheet("border-radius: 5px")
        self.btn_init_edit_teacher.setIcon(icon7)
        self.btn_init_edit_teacher.setIconSize(QtCore.QSize(20, 20))
        self.btn_init_edit_teacher.setObjectName("btn_init_edit_teacher")
        self.horizontalLayout_18.addWidget(self.btn_init_edit_teacher)
        self.btn_delete_teacher = QtWidgets.QPushButton(self.w_teacher_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_delete_teacher.sizePolicy().hasHeightForWidth())
        self.btn_delete_teacher.setSizePolicy(sizePolicy)
        self.btn_delete_teacher.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_teacher.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_teacher.setStyleSheet("QPushButton{\n"
                                              "    border-radius: 5px;\n"
                                              "    background: none;\n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "     background-color: #072f49;\n"
                                              "}")
        self.btn_delete_teacher.setIcon(icon8)
        self.btn_delete_teacher.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_teacher.setObjectName("btn_delete_teacher")
        self.horizontalLayout_18.addWidget(self.btn_delete_teacher)
        self.verticalLayout_19.addLayout(self.horizontalLayout_18)
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_21.setSpacing(6)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label_16 = QtWidgets.QLabel(self.w_teacher_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setIndent(1)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_21.addWidget(self.label_16)
        self.txt_teacher_username = QtWidgets.QLineEdit(self.w_teacher_input)
        self.txt_teacher_username.setEnabled(False)
        self.txt_teacher_username.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_teacher_username.setFont(font)
        self.txt_teacher_username.setObjectName("txt_teacher_username")
        self.verticalLayout_21.addWidget(self.txt_teacher_username)
        self.label_18 = QtWidgets.QLabel(self.w_teacher_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setIndent(1)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_21.addWidget(self.label_18)
        self.txt_teacher_password = PasswordGenerator(self.w_teacher_input)
        self.txt_teacher_password.setEnabled(False)
        self.txt_teacher_password.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_teacher_password.setFont(font)
        self.txt_teacher_password.setObjectName("txt_teacher_password")
        self.verticalLayout_21.addWidget(self.txt_teacher_password)
        self.verticalLayout_19.addLayout(self.verticalLayout_21)
        self.w_teacher_btn = QtWidgets.QWidget(self.w_teacher_input)
        self.w_teacher_btn.setObjectName("w_teacher_btn")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.w_teacher_btn)
        self.verticalLayout_22.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_22.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.btn_add_edit_teacher = QtWidgets.QPushButton(self.w_teacher_btn)
        self.btn_add_edit_teacher.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_add_edit_teacher.setFont(font)
        self.btn_add_edit_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_edit_teacher.setStyleSheet("border-radius: 5px;")
        self.btn_add_edit_teacher.setObjectName("btn_add_edit_teacher")
        self.verticalLayout_22.addWidget(self.btn_add_edit_teacher)
        self.btn_cancel_teacher = QtWidgets.QPushButton(self.w_teacher_btn)
        self.btn_cancel_teacher.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_cancel_teacher.setFont(font)
        self.btn_cancel_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel_teacher.setStyleSheet("QPushButton{\n"
                                              "    border-radius: 5px;\n"
                                              "    background: none;\n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QPushButton:pressed {\n"
                                              "     background-color: #072f49;\n"
                                              "}")
        self.btn_cancel_teacher.setObjectName("btn_cancel_teacher")
        self.verticalLayout_22.addWidget(self.btn_cancel_teacher)
        self.verticalLayout_19.addWidget(self.w_teacher_btn)
        self.verticalLayout_40.addWidget(self.w_teacher_input)
        self.line_12 = QtWidgets.QFrame(self.widget_7)
        self.line_12.setStyleSheet("color: #0e4177;")
        self.line_12.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_12.setLineWidth(2)
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setObjectName("line_12")
        self.verticalLayout_40.addWidget(self.line_12)
        self.w_attendance = QtWidgets.QWidget(self.widget_7)
        self.w_attendance.setObjectName("w_attendance")
        self.verticalLayout_43 = QtWidgets.QVBoxLayout(self.w_attendance)
        self.verticalLayout_43.setContentsMargins(15, 20, 15, 20)
        self.verticalLayout_43.setSpacing(15)
        self.verticalLayout_43.setObjectName("verticalLayout_43")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setSpacing(6)
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.lbl_attendance_status = QtWidgets.QLabel(self.w_attendance)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_attendance_status.setFont(font)
        self.lbl_attendance_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_attendance_status.setIndent(1)
        self.lbl_attendance_status.setObjectName("lbl_attendance_status")
        self.horizontalLayout_31.addWidget(self.lbl_attendance_status)
        spacerItem18 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_31.addItem(spacerItem18)
        self.btn_delete_attendance = QtWidgets.QPushButton(self.w_attendance)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_delete_attendance.sizePolicy().hasHeightForWidth())
        self.btn_delete_attendance.setSizePolicy(sizePolicy)
        self.btn_delete_attendance.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_attendance.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_attendance.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_attendance.setStyleSheet("QPushButton{\n"
                                                 "    border-radius: 5px;\n"
                                                 "    background: none;\n"
                                                 "}\n"
                                                 "\n"
                                                 "\n"
                                                 "QPushButton:pressed {\n"
                                                 "     background-color: #072f49;\n"
                                                 "}")
        self.btn_delete_attendance.setIcon(icon8)
        self.btn_delete_attendance.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_attendance.setObjectName("btn_delete_attendance")
        self.horizontalLayout_31.addWidget(self.btn_delete_attendance)
        self.btn_clear_attendance_table = QtWidgets.QPushButton(
            self.w_attendance)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_clear_attendance_table.sizePolicy().hasHeightForWidth())
        self.btn_clear_attendance_table.setSizePolicy(sizePolicy)
        self.btn_clear_attendance_table.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_attendance_table.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_attendance_table.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_attendance_table.setStyleSheet("QPushButton{\n"
                                                      "    border-radius: 5px;\n"
                                                      "    background: none;\n"
                                                      "}\n"
                                                      "\n"
                                                      "\n"
                                                      "QPushButton:pressed {\n"
                                                      "     background-color: #072f49;\n"
                                                      "}")
        self.btn_clear_attendance_table.setIcon(icon2)
        self.btn_clear_attendance_table.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_attendance_table.setObjectName(
            "btn_clear_attendance_table")
        self.horizontalLayout_31.addWidget(self.btn_clear_attendance_table)
        self.verticalLayout_43.addLayout(self.horizontalLayout_31)
        self.horizontalLayout_59 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_59.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_59.setSpacing(0)
        self.horizontalLayout_59.setObjectName("horizontalLayout_59")
        self.txt_search_attendance = QtWidgets.QLineEdit(self.w_attendance)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_attendance.sizePolicy().hasHeightForWidth())
        self.txt_search_attendance.setSizePolicy(sizePolicy)
        self.txt_search_attendance.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_attendance.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_attendance.setFont(font)
        self.txt_search_attendance.setStyleSheet("border-radius: none;\n"
                                                 "border-top-left-radius: 5px;\n"
                                                 "border-bottom-left-radius: 5px;")
        self.txt_search_attendance.setObjectName("txt_search_attendance")
        self.horizontalLayout_59.addWidget(self.txt_search_attendance)
        self.btn_search_attendance = QtWidgets.QPushButton(self.w_attendance)
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
        self.btn_search_attendance.setIcon(icon4)
        self.btn_search_attendance.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_attendance.setObjectName("btn_search_attendance")
        self.horizontalLayout_59.addWidget(self.btn_search_attendance)
        self.verticalLayout_43.addLayout(self.horizontalLayout_59)
        self.lv_attendance = ListView(self.w_attendance)
        self.lv_attendance.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lv_attendance.setObjectName("lv_attendance")
        self.verticalLayout_43.addWidget(self.lv_attendance)
        self.verticalLayout_40.addWidget(self.w_attendance)
        
        self.verticalLayout_40.setStretch(4, 1)
        self.horizontalLayout_4.addWidget(self.widget_7)
        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)
        self.sw_all.addWidget(self.teacher)
        self.class_member = QtWidgets.QWidget()
        self.class_member.setObjectName("class_member")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.class_member)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(15)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.w_table_class = QtWidgets.QWidget(self.class_member)
        self.w_table_class.setMinimumSize(QtCore.QSize(377, 0))
        self.w_table_class.setStyleSheet("QWidget{\n"
                                    "    background: #102542;\n"
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
        self.w_table_class.setObjectName("w_table_class")
        self.verticalLayout_29 = QtWidgets.QVBoxLayout(self.w_table_class)
        self.verticalLayout_29.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_29.setSpacing(5)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_23.setSpacing(6)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.lbl_class_table_status = QtWidgets.QLabel(self.w_table_class)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_class_table_status.sizePolicy().hasHeightForWidth())
        self.lbl_class_table_status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_class_table_status.setFont(font)
        self.lbl_class_table_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_class_table_status.setIndent(1)
        self.lbl_class_table_status.setObjectName("lbl_class_table_status")
        self.horizontalLayout_23.addWidget(self.lbl_class_table_status)
        spacerItem20 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_23.addItem(spacerItem20)
        self.btn_import_class = QtWidgets.QPushButton(self.w_table_class)
        self.btn_import_class.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_import_class.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_import_class.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_import_class.setStyleSheet("border-radius: 5px")
        self.btn_import_class.setIcon(icon11)
        self.btn_import_class.setIconSize(QtCore.QSize(20, 20))
        self.btn_import_class.setObjectName("btn_import_class")
        self.horizontalLayout_23.addWidget(self.btn_import_class)
        self.btn_export_class = QtWidgets.QPushButton(self.w_table_class)
        self.btn_export_class.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_export_class.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_export_class.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_export_class.setStyleSheet("border-radius: 5px")
        self.btn_export_class.setIcon(icon1)
        self.btn_export_class.setIconSize(QtCore.QSize(20, 20))
        self.btn_export_class.setObjectName("btn_export_class")
        self.horizontalLayout_23.addWidget(self.btn_export_class)
        self.btn_clear_class_table = QtWidgets.QPushButton(self.w_table_class)
        self.btn_clear_class_table.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_class_table.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_class_table.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_class_table.setStyleSheet("QPushButton{\n"
                                                 "    border-radius: 5px;\n"
                                                 "    background: none;\n"
                                                 "}\n"
                                                 "\n"
                                                 "\n"
                                                 "QPushButton:pressed {\n"
                                                 "     background-color: #072f49;\n"
                                                 "}")
        self.btn_clear_class_table.setIcon(icon2)
        self.btn_clear_class_table.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_class_table.setObjectName("btn_clear_class_table")
        self.horizontalLayout_23.addWidget(self.btn_clear_class_table)
        self.verticalLayout_29.addLayout(self.horizontalLayout_23)
        self.line_7 = QtWidgets.QFrame(self.w_table_class)
        self.line_7.setStyleSheet("color: #083654;")
        self.line_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_7.setLineWidth(2)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_29.addWidget(self.line_7)
        self.sw_class = QtWidgets.QStackedWidget(self.w_table_class)
        self.sw_class.setObjectName("sw_class")
        self.class_table = QtWidgets.QWidget()
        self.class_table.setObjectName("class_table")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout(self.class_table)
        self.verticalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_30.setSpacing(15)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.groupBox_5 = QtWidgets.QGroupBox(self.class_table)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_31 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_31.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_31.setSpacing(15)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.horizontalLayout_52 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_52.setSpacing(0)
        self.horizontalLayout_52.setObjectName("horizontalLayout_52")
        self.btn_init_class_bulk = QtWidgets.QPushButton(self.groupBox_5)
        self.btn_init_class_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_class_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_class_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_class_bulk.setStyleSheet("border-radius: 5px")
        self.btn_init_class_bulk.setIcon(icon3)
        self.btn_init_class_bulk.setIconSize(QtCore.QSize(18, 18))
        self.btn_init_class_bulk.setObjectName("btn_init_class_bulk")
        self.horizontalLayout_52.addWidget(self.btn_init_class_bulk)
        spacerItem21 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_52.addItem(spacerItem21)
        self.horizontalLayout_53 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_53.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_53.setSpacing(0)
        self.horizontalLayout_53.setObjectName("horizontalLayout_53")
        self.txt_search_class = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_class.sizePolicy().hasHeightForWidth())
        self.txt_search_class.setSizePolicy(sizePolicy)
        self.txt_search_class.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_class.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_class.setFont(font)
        self.txt_search_class.setStyleSheet("border-radius: none;\n"
                                            "border-top-left-radius: 5px;\n"
                                            "border-bottom-left-radius: 5px;")
        self.txt_search_class.setObjectName("txt_search_class")
        self.horizontalLayout_53.addWidget(self.txt_search_class)
        self.btn_search_class = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_class.sizePolicy().hasHeightForWidth())
        self.btn_search_class.setSizePolicy(sizePolicy)
        self.btn_search_class.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_class.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_class.setFont(font)
        self.btn_search_class.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_class.setStyleSheet("border-top-right-radius: 5px;\n"
                                            "border-bottom-right-radius: 5px;")
        self.btn_search_class.setText("")
        self.btn_search_class.setIcon(icon4)
        self.btn_search_class.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_class.setObjectName("btn_search_class")
        self.horizontalLayout_53.addWidget(self.btn_search_class)
        self.horizontalLayout_52.addLayout(self.horizontalLayout_53)
        self.verticalLayout_31.addLayout(self.horizontalLayout_52)
        self.tv_class = TableView(self.groupBox_5)
        self.tv_class.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tv_class.setObjectName("tv_class")
        self.verticalLayout_31.addWidget(self.tv_class)
        self.horizontalLayout_26.addWidget(self.groupBox_5)
        self.verticalLayout_30.addLayout(self.horizontalLayout_26)
        self.sw_class.addWidget(self.class_table)
        self.class_class_bulk = QtWidgets.QWidget()
        self.class_class_bulk.setObjectName("class_class_bulk")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.class_class_bulk)
        self.horizontalLayout_30.setContentsMargins(0, 15, 0, 0)
        self.horizontalLayout_30.setSpacing(6)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.class_class_bulk)
        self.scrollArea_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_4.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(
            QtCore.QRect(0, 0, 521, 703))
        self.scrollAreaWidgetContents_4.setObjectName(
            "scrollAreaWidgetContents_4")
        self.verticalLayout_50 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_4)
        self.verticalLayout_50.setContentsMargins(0, 0, 10, 0)
        self.verticalLayout_50.setSpacing(20)
        self.verticalLayout_50.setObjectName("verticalLayout_50")

        class_item = ClassItem(self)
        class_item.setObjectName("classItem_1")
        self.verticalLayout_50.addWidget(class_item)

        class_item = ClassItem(self)
        class_item.setObjectName("classItem_2")
        self.verticalLayout_50.addWidget(class_item)

        spacerItem22 = QtWidgets.QSpacerItem(
            20, 460, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_50.addItem(spacerItem22)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.horizontalLayout_30.addWidget(self.scrollArea_4)
        self.verticalLayout_35 = QtWidgets.QVBoxLayout()
        self.verticalLayout_35.setSpacing(6)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.btn_add_class_bulk = QtWidgets.QPushButton(self.class_class_bulk)
        self.btn_add_class_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_add_class_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_add_class_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_class_bulk.setStyleSheet("border-radius: 5px")
        self.btn_add_class_bulk.setIcon(icon5)
        self.btn_add_class_bulk.setIconSize(QtCore.QSize(19, 19))
        self.btn_add_class_bulk.setObjectName("btn_add_class_bulk")
        self.verticalLayout_35.addWidget(self.btn_add_class_bulk)
        self.btn_add_class_item = QtWidgets.QPushButton(self.class_class_bulk)
        self.btn_add_class_item.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_add_class_item.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_add_class_item.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_class_item.setStyleSheet("border-radius: 5px;\n"
                                              f"background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                              "background-repeat: no-repeat;\n"
                                              "background-position: center center;")
        self.btn_add_class_item.setIconSize(QtCore.QSize(17, 17))
        self.btn_add_class_item.setObjectName("btn_add_class_item")
        self.verticalLayout_35.addWidget(self.btn_add_class_item)
        self.btn_clear_class_item = QtWidgets.QPushButton(
            self.class_class_bulk)
        self.btn_clear_class_item.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_class_item.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_class_item.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_class_item.setStyleSheet("QPushButton{\n"
                                                "    border-radius: 5px;\n"
                                                "    background: none;\n"
                                                "}\n"
                                                "\n"
                                                "\n"
                                                "QPushButton:pressed {\n"
                                                "     background-color: #072f49;\n"
                                                "}")
        self.btn_clear_class_item.setIcon(icon6)
        self.btn_clear_class_item.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_class_item.setObjectName("btn_clear_class_item")
        self.verticalLayout_35.addWidget(self.btn_clear_class_item)
        self.btn_back_class_bulk = QtWidgets.QPushButton(self.class_class_bulk)
        self.btn_back_class_bulk.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_back_class_bulk.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_back_class_bulk.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_back_class_bulk.setStyleSheet("QPushButton{\n"
                                               "    border: none;\n"
                                               "    border-radius: none;\n"
                                               "    background: none;\n"
                                               "    background-repeat: none;\n"
                                               f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'left.png')});\n"
                                               "    background-position: center center;\n"
                                               "}\n"
                                               "\n"
                                               "QPushButton:hover{\n"
                                               "    background: none;\n"
                                               "    background-repeat: none;\n"
                                               f"    background-image: url({relative_path('Admin', ['Misc', 'Resources'], 'left_2.png')});\n"
                                               "    background-position: center center;\n"
                                               "}")
        self.btn_back_class_bulk.setObjectName("btn_back_class_bulk")
        self.verticalLayout_35.addWidget(self.btn_back_class_bulk)
        spacerItem23 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_35.addItem(spacerItem23)
        self.horizontalLayout_30.addLayout(self.verticalLayout_35)
        self.sw_class.addWidget(self.class_class_bulk)
        self.verticalLayout_29.addWidget(self.sw_class)
        self.horizontalLayout_5.addWidget(self.w_table_class)
        self.widget_8 = QtWidgets.QWidget(self.class_member)
        self.widget_8.setMinimumSize(QtCore.QSize(234, 0))
        self.widget_8.setMaximumSize(QtCore.QSize(380, 16777215))
        self.widget_8.setStyleSheet("QWidget{\n"
                                    "    background: #083654;\n"
                                    "}\n"
                                    "\n"
                                    "QTimeEdit,\n"
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
                                    "QTimeEdit::disabled,\n"
                                    "QLineEdit::disabled {\n"
                                    "   border: 1px solid #072f49;\n"
                                    "   border-radius: 5px;\n"
                                    "   background-color: #072f49;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::disabled {\n"
                                    "  padding: 5px;\n"
                                    "  border: 1px solid #102542;\n"
                                    "  background-color: #102542;\n"
                                    "}\n"
                                    "\n"
                                    "QTimeEdit:focus,\n"
                                    "QTimeEdit:hover,\n"
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
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_45 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_45.setSpacing(0)
        self.verticalLayout_45.setObjectName("verticalLayout_45")
        self.w_class_input = QtWidgets.QWidget(self.widget_8)
        self.w_class_input.setObjectName("w_class_input")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.w_class_input)
        self.verticalLayout_26.setContentsMargins(15, 15, 15, 20)
        self.verticalLayout_26.setSpacing(15)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setSpacing(6)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_20 = QtWidgets.QLabel(self.w_class_input)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("letter-spacing: 0.5px")
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setIndent(1)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_21.addWidget(self.label_20)
        spacerItem24 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem24)
        self.btn_init_add_class = QtWidgets.QPushButton(self.w_class_input)
        self.btn_init_add_class.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_add_class.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_add_class.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_class.setStyleSheet("QPushButton{\n"
                                              "    border-radius: 5px;\n"
                                              f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                              "    background-repeat: no-repeat;\n"
                                              "    background-position: center center;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton::disabled{\n"
                                              "    border-radius: 5px;\n"
                                              f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add_2.png')});\n"
                                              "    background-repeat: no-repeat;\n"
                                              "    background-position: center center;\n"
                                              "}")
        self.btn_init_add_class.setIconSize(QtCore.QSize(17, 17))
        self.btn_init_add_class.setObjectName("btn_init_add_class")
        self.horizontalLayout_21.addWidget(self.btn_init_add_class)
        self.btn_init_edit_class = QtWidgets.QPushButton(self.w_class_input)
        self.btn_init_edit_class.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_class.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_class.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_edit_class.setStyleSheet("border-radius: 5px")
        self.btn_init_edit_class.setIcon(icon7)
        self.btn_init_edit_class.setIconSize(QtCore.QSize(20, 20))
        self.btn_init_edit_class.setObjectName("btn_init_edit_class")
        self.horizontalLayout_21.addWidget(self.btn_init_edit_class)
        self.btn_delete_class = QtWidgets.QPushButton(self.w_class_input)
        self.btn_delete_class.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_class.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_class.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_class.setStyleSheet("QPushButton{\n"
                                            "    border-radius: 5px;\n"
                                            "    background: none;\n"
                                            "}\n"
                                            "\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "     background-color: #072f49;\n"
                                            "}")
        self.btn_delete_class.setIcon(icon8)
        self.btn_delete_class.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_class.setObjectName("btn_delete_class")
        self.horizontalLayout_21.addWidget(self.btn_delete_class)
        self.verticalLayout_26.addLayout(self.horizontalLayout_21)
        self.verticalLayout_27 = QtWidgets.QVBoxLayout()
        self.verticalLayout_27.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_27.setSpacing(6)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.label_21 = QtWidgets.QLabel(self.w_class_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_21.setFont(font)
        self.label_21.setIndent(1)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_27.addWidget(self.label_21)
        self.txt_class_code = QtWidgets.QLineEdit(self.w_class_input)
        self.txt_class_code.setEnabled(False)
        self.txt_class_code.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_class_code.setFont(font)
        self.txt_class_code.setMaxLength(8)
        self.txt_class_code.setObjectName("txt_class_code")
        self.verticalLayout_27.addWidget(self.txt_class_code)
        self.label_25 = QtWidgets.QLabel(self.w_class_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_25.setFont(font)
        self.label_25.setIndent(1)
        self.label_25.setObjectName("label_25")
        self.verticalLayout_27.addWidget(self.label_25)
        self.txt_class_name = QtWidgets.QLineEdit(self.w_class_input)
        self.txt_class_name.setEnabled(False)
        self.txt_class_name.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_class_name.setFont(font)
        self.txt_class_name.setObjectName("txt_class_name")
        self.verticalLayout_27.addWidget(self.txt_class_name)
        self.label_23 = QtWidgets.QLabel(self.w_class_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_23.setFont(font)
        self.label_23.setIndent(1)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_27.addWidget(self.label_23)
        self.txt_class_start = QtWidgets.QTimeEdit(self.w_class_input)
        self.txt_class_start.setEnabled(False)
        self.txt_class_start.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_class_start.setFont(font)
        self.txt_class_start.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        self.txt_class_start.setTime(QtCore.QTime(7, 0, 0))
        self.txt_class_start.setObjectName("txt_class_start")
        self.verticalLayout_27.addWidget(self.txt_class_start)
        self.label_24 = QtWidgets.QLabel(self.w_class_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_24.setFont(font)
        self.label_24.setIndent(1)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_27.addWidget(self.label_24)
        self.txt_class_end = QtWidgets.QTimeEdit(self.w_class_input)
        self.txt_class_end.setEnabled(False)
        self.txt_class_end.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_class_end.setFont(font)
        self.txt_class_end.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        self.txt_class_end.setTime(QtCore.QTime(7, 0, 0))
        self.txt_class_end.setObjectName("txt_class_end")
        self.verticalLayout_27.addWidget(self.txt_class_end)
        self.verticalLayout_26.addLayout(self.verticalLayout_27)
        self.w_class_btn = QtWidgets.QWidget(self.w_class_input)
        self.w_class_btn.setObjectName("w_class_btn")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.w_class_btn)
        self.verticalLayout_28.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_28.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.btn_add_edit_class = QtWidgets.QPushButton(self.w_class_btn)
        self.btn_add_edit_class.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btn_add_edit_class.setFont(font)
        self.btn_add_edit_class.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_edit_class.setStyleSheet("border-radius: 5px;")
        self.btn_add_edit_class.setObjectName("btn_add_edit_class")
        self.verticalLayout_28.addWidget(self.btn_add_edit_class)
        self.btn_cancel_class = QtWidgets.QPushButton(self.w_class_btn)
        self.btn_cancel_class.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_cancel_class.setFont(font)
        self.btn_cancel_class.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel_class.setStyleSheet("QPushButton{\n"
                                            "    border-radius: 5px;\n"
                                            "    background: none;\n"
                                            "}\n"
                                            "\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "     background-color: #072f49;\n"
                                            "}")
        self.btn_cancel_class.setObjectName("btn_cancel_class")
        self.verticalLayout_28.addWidget(self.btn_cancel_class)
        self.verticalLayout_26.addWidget(self.w_class_btn)
        self.verticalLayout_45.addWidget(self.w_class_input)
        self.line_13 = QtWidgets.QFrame(self.widget_8)
        self.line_13.setStyleSheet("color: #0e4177;")
        self.line_13.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_13.setLineWidth(2)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setObjectName("line_13")
        self.verticalLayout_45.addWidget(self.line_13)
        self.w_class_teacher = QtWidgets.QWidget(self.widget_8)
        self.w_class_teacher.setObjectName("w_class_teacher")
        self.verticalLayout_44 = QtWidgets.QVBoxLayout(self.w_class_teacher)
        self.verticalLayout_44.setContentsMargins(15, 20, 15, 20)
        self.verticalLayout_44.setSpacing(15)
        self.verticalLayout_44.setObjectName("verticalLayout_44")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setSpacing(6)
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.lbl_class_teacher_status = QtWidgets.QLabel(self.w_class_teacher)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_class_teacher_status.setFont(font)
        self.lbl_class_teacher_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_class_teacher_status.setIndent(1)
        self.lbl_class_teacher_status.setObjectName(
            "lbl_class_teacher_status")
        self.horizontalLayout_32.addWidget(self.lbl_class_teacher_status)
        spacerItem25 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_32.addItem(spacerItem25)
        self.btn_init_add_class_teacher = QtWidgets.QPushButton(self.w_class_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_add_class_teacher.sizePolicy().hasHeightForWidth())
        self.btn_init_add_class_teacher.setSizePolicy(sizePolicy)
        self.btn_init_add_class_teacher.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_add_class_teacher.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_add_class_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_class_teacher.setStyleSheet("QPushButton{\n"
                                                      "    border-radius: 5px;\n"
                                                      f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                      "    background-repeat: no-repeat;\n"
                                                      "    background-position: center center;\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton::disabled{\n"
                                                      "    border-radius: 5px;\n"
                                                      f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add_2.png')});\n"
                                                      "    background-repeat: no-repeat;\n"
                                                      "    background-position: center center;\n"
                                                      "}")
        self.btn_init_add_class_teacher.setIconSize(QtCore.QSize(17, 17))
        self.btn_init_add_class_teacher.setObjectName(
            "btn_init_add_class_teacher")
        self.horizontalLayout_32.addWidget(self.btn_init_add_class_teacher)
        self.btn_delete_class_teacher = QtWidgets.QPushButton(self.w_class_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_delete_class_teacher.sizePolicy().hasHeightForWidth())
        self.btn_delete_class_teacher.setSizePolicy(sizePolicy)
        self.btn_delete_class_teacher.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_class_teacher.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_class_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_class_teacher.setStyleSheet("QPushButton{\n"
                                                    "    border-radius: 5px;\n"
                                                    "    background: none;\n"
                                                    "}\n"
                                                    "\n"
                                                    "\n"
                                                    "QPushButton:pressed {\n"
                                                    "     background-color: #072f49;\n"
                                                    "}")
        self.btn_delete_class_teacher.setIcon(icon8)
        self.btn_delete_class_teacher.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_class_teacher.setObjectName("btn_delete_class_teacher")
        self.horizontalLayout_32.addWidget(self.btn_delete_class_teacher)
        self.btn_clear_class_teacher = QtWidgets.QPushButton(self.w_class_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_clear_class_teacher.sizePolicy().hasHeightForWidth())
        self.btn_clear_class_teacher.setSizePolicy(sizePolicy)
        self.btn_clear_class_teacher.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_class_teacher.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_class_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_class_teacher.setStyleSheet("QPushButton{\n"
                                                   "    border-radius: 5px;\n"
                                                   "    background: none;\n"
                                                   "}\n"
                                                   "\n"
                                                   "\n"
                                                   "QPushButton:pressed {\n"
                                                   "     background-color: #072f49;\n"
                                                   "}")
        self.btn_clear_class_teacher.setIcon(icon2)
        self.btn_clear_class_teacher.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_class_teacher.setObjectName("btn_clear_class_teacher")
        self.horizontalLayout_32.addWidget(self.btn_clear_class_teacher)
        self.verticalLayout_44.addLayout(self.horizontalLayout_32)
        self.horizontalLayout_60 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_60.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_60.setSpacing(0)
        self.horizontalLayout_60.setObjectName("horizontalLayout_60")
        self.txt_search_class_teacher = QtWidgets.QLineEdit(self.w_class_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_class_teacher.sizePolicy().hasHeightForWidth())
        self.txt_search_class_teacher.setSizePolicy(sizePolicy)
        self.txt_search_class_teacher.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_class_teacher.setMaximumSize(
            QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_class_teacher.setFont(font)
        self.txt_search_class_teacher.setStyleSheet("border-radius: none;\n"
                                                    "border-top-left-radius: 5px;\n"
                                                    "border-bottom-left-radius: 5px;")
        self.txt_search_class_teacher.setObjectName("txt_search_class_teacher")
        self.horizontalLayout_60.addWidget(self.txt_search_class_teacher)
        self.btn_search_class_teacher = QtWidgets.QPushButton(self.w_class_teacher)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_class_teacher.sizePolicy().hasHeightForWidth())
        self.btn_search_class_teacher.setSizePolicy(sizePolicy)
        self.btn_search_class_teacher.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_class_teacher.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_class_teacher.setFont(font)
        self.btn_search_class_teacher.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_class_teacher.setStyleSheet("border-top-right-radius: 5px;\n"
                                                    "border-bottom-right-radius: 5px;")
        self.btn_search_class_teacher.setText("")
        self.btn_search_class_teacher.setIcon(icon4)
        self.btn_search_class_teacher.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_class_teacher.setObjectName("btn_search_class_teacher")
        self.horizontalLayout_60.addWidget(self.btn_search_class_teacher)
        self.verticalLayout_44.addLayout(self.horizontalLayout_60)
        self.lv_class_teacher = ListView(self.w_class_teacher)
        self.lv_class_teacher.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lv_class_teacher.setObjectName("lv_class_teacher")
        self.verticalLayout_44.addWidget(self.lv_class_teacher)
        self.verticalLayout_45.addWidget(self.w_class_teacher)
        self.line_6 = QtWidgets.QFrame(self.widget_8)
        self.line_6.setStyleSheet("color: #0e4177;")
        self.line_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_6.setLineWidth(2)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_45.addWidget(self.line_6)
        self.w_class_section = QtWidgets.QWidget(self.widget_8)
        self.w_class_section.setObjectName("w_class_section")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.w_class_section)
        self.verticalLayout_25.setContentsMargins(15, 20, 15, 15)
        self.verticalLayout_25.setSpacing(15)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setSpacing(6)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.lbl_class_section_status = QtWidgets.QLabel(self.w_class_section)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_class_section_status.sizePolicy().hasHeightForWidth())
        self.lbl_class_section_status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_class_section_status.setFont(font)
        self.lbl_class_section_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_class_section_status.setIndent(1)
        self.lbl_class_section_status.setObjectName("lbl_class_section_status")
        self.horizontalLayout_22.addWidget(self.lbl_class_section_status)
        spacerItem26 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem26)
        self.btn_init_add_class_section = QtWidgets.QPushButton(
            self.w_class_section)
        self.btn_init_add_class_section.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_add_class_section.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_add_class_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_class_section.setStyleSheet("QPushButton{\n"
                                                      "    border-radius: 5px;\n"
                                                      f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                                      "    background-repeat: no-repeat;\n"
                                                      "    background-position: center center;\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton::disabled{\n"
                                                      "    border-radius: 5px;\n"
                                                      f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add_2.png')});\n"
                                                      "    background-repeat: no-repeat;\n"
                                                      "    background-position: center center;\n"
                                                      "}")
        self.btn_init_add_class_section.setIconSize(QtCore.QSize(17, 17))
        self.btn_init_add_class_section.setObjectName(
            "btn_init_add_class_section")
        self.horizontalLayout_22.addWidget(self.btn_init_add_class_section)
        self.btn_delete_class_section = QtWidgets.QPushButton(
            self.w_class_section)
        self.btn_delete_class_section.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_class_section.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_class_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_class_section.setStyleSheet("QPushButton{\n"
                                                    "    border-radius: 5px;\n"
                                                    "    background: none;\n"
                                                    "}\n"
                                                    "\n"
                                                    "\n"
                                                    "QPushButton:pressed {\n"
                                                    "     background-color: #072f49;\n"
                                                    "}")
        self.btn_delete_class_section.setIcon(icon8)
        self.btn_delete_class_section.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_class_section.setObjectName("btn_delete_class_section")
        self.horizontalLayout_22.addWidget(self.btn_delete_class_section)
        self.btn_clear_class_student = QtWidgets.QPushButton(
            self.w_class_section)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_clear_class_student.sizePolicy().hasHeightForWidth())
        self.btn_clear_class_student.setSizePolicy(sizePolicy)
        self.btn_clear_class_student.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_class_student.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_class_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_class_student.setStyleSheet("QPushButton{\n"
                                                   "    border-radius: 5px;\n"
                                                   "    background: none;\n"
                                                   "}\n"
                                                   "\n"
                                                   "\n"
                                                   "QPushButton:pressed {\n"
                                                   "     background-color: #072f49;\n"
                                                   "}")
        self.btn_clear_class_student.setIcon(icon2)
        self.btn_clear_class_student.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_class_student.setObjectName("btn_clear_class_student")
        self.horizontalLayout_22.addWidget(self.btn_clear_class_student)
        self.verticalLayout_25.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_56 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_56.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_56.setSpacing(0)
        self.horizontalLayout_56.setObjectName("horizontalLayout_56")
        self.txt_search_class_section = QtWidgets.QLineEdit(
            self.w_class_section)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_class_section.sizePolicy().hasHeightForWidth())
        self.txt_search_class_section.setSizePolicy(sizePolicy)
        self.txt_search_class_section.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_class_section.setMaximumSize(
            QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_class_section.setFont(font)
        self.txt_search_class_section.setStyleSheet("border-radius: none;\n"
                                                    "border-top-left-radius: 5px;\n"
                                                    "border-bottom-left-radius: 5px;")
        self.txt_search_class_section.setObjectName("txt_search_class_section")
        self.horizontalLayout_56.addWidget(self.txt_search_class_section)
        self.btn_search_class_section = QtWidgets.QPushButton(
            self.w_class_section)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_class_section.sizePolicy().hasHeightForWidth())
        self.btn_search_class_section.setSizePolicy(sizePolicy)
        self.btn_search_class_section.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_class_section.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_class_section.setFont(font)
        self.btn_search_class_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_class_section.setStyleSheet("border-top-right-radius: 5px;\n"
                                                    "border-bottom-right-radius: 5px;")
        self.btn_search_class_section.setText("")
        self.btn_search_class_section.setIcon(icon4)
        self.btn_search_class_section.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_class_section.setObjectName("btn_search_class_section")
        self.horizontalLayout_56.addWidget(self.btn_search_class_section)
        self.verticalLayout_25.addLayout(self.horizontalLayout_56)
        self.lv_class_section = ListView(self.w_class_section)
        self.lv_class_section.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lv_class_section.setObjectName("lv_class_section")
        self.verticalLayout_25.addWidget(self.lv_class_section)
        self.verticalLayout_45.addWidget(self.w_class_section)
        self.verticalLayout_45.setStretch(4, 1)
        self.horizontalLayout_5.addWidget(self.widget_8)
        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 1)
        self.sw_all.addWidget(self.class_member)
        self.blacklisted_url = QtWidgets.QWidget()
        self.blacklisted_url.setObjectName("blacklisted_url")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.blacklisted_url)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(15)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.w_website_viewer = QtWidgets.QWidget(self.blacklisted_url)
        self.w_website_viewer.setMinimumSize(QtCore.QSize(377, 0))
        self.w_website_viewer.setStyleSheet("QWidget{\n"
                                            "    background: #102542;\n"
                                            "}\n")
        self.w_website_viewer.setObjectName("w_website_viewer")

        self.verticalLayout_69 = QtWidgets.QVBoxLayout(self.w_website_viewer)
        self.verticalLayout_69.setObjectName("w_website_viewer")

        self.web_viewer = QtWebEngineWidgets.QWebEngineView()
        self.verticalLayout_69.addWidget(self.web_viewer)

        self.horizontalLayout_10.addWidget(self.w_website_viewer)
        self.widget_12 = QtWidgets.QWidget(self.blacklisted_url)
        self.widget_12.setMinimumSize(QtCore.QSize(234, 0))
        self.widget_12.setMaximumSize(QtCore.QSize(380, 16777215))
        self.widget_12.setStyleSheet("QWidget{\n"
                                     "    background: #083654;\n"
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
                                     "QLineEdit::disabled {\n"
                                     "   border: 1px solid #072f49;\n"
                                     "   border-radius: 5px;\n"
                                     "   background-color: #072f49;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton::disabled {\n"
                                     "  padding: 5px;\n"
                                     "  border: 1px solid #102542;\n"
                                     "  background-color: #102542;\n"
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
                                     )
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_42 = QtWidgets.QVBoxLayout(self.widget_12)
        self.verticalLayout_42.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_42.setSpacing(0)
        self.verticalLayout_42.setObjectName("verticalLayout_42")
        self.w_url_input = QtWidgets.QWidget(self.widget_12)
        self.w_url_input.setObjectName("w_url_input")
        self.verticalLayout_36 = QtWidgets.QVBoxLayout(self.w_url_input)
        self.verticalLayout_36.setContentsMargins(15, 15, 15, 20)
        self.verticalLayout_36.setSpacing(15)
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setSpacing(6)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_17 = QtWidgets.QLabel(self.w_url_input)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("letter-spacing: 0.5px")
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setIndent(1)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_25.addWidget(self.label_17)
        spacerItem27 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem27)
        self.btn_init_add_url = QtWidgets.QPushButton(self.w_url_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_add_url.sizePolicy().hasHeightForWidth())
        self.btn_init_add_url.setSizePolicy(sizePolicy)
        self.btn_init_add_url.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_add_url.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_add_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_add_url.setStyleSheet("QPushButton{\n"
                                            "    border-radius: 5px;\n"
                                            f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add.png')});\n"
                                            "    background-repeat: no-repeat;\n"
                                            "    background-position: center center;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton::disabled{\n"
                                            "    border-radius: 5px;\n"
                                            f"    background-image:  url({relative_path('Admin', ['Misc', 'Resources'], 'add_2.png')});\n"
                                            "    background-repeat: no-repeat;\n"
                                            "    background-position: center center;\n"
                                            "}")
        self.btn_init_add_url.setIconSize(QtCore.QSize(17, 17))
        self.btn_init_add_url.setObjectName("btn_init_add_url")
        self.horizontalLayout_25.addWidget(self.btn_init_add_url)
        self.btn_init_edit_url = QtWidgets.QPushButton(self.w_url_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_init_edit_url.sizePolicy().hasHeightForWidth())
        self.btn_init_edit_url.setSizePolicy(sizePolicy)
        self.btn_init_edit_url.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_url.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_init_edit_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_init_edit_url.setStyleSheet("border-radius: 5px")
        self.btn_init_edit_url.setIcon(icon7)
        self.btn_init_edit_url.setIconSize(QtCore.QSize(20, 20))
        self.btn_init_edit_url.setObjectName("btn_init_edit_url")
        self.horizontalLayout_25.addWidget(self.btn_init_edit_url)
        self.btn_delete_url = QtWidgets.QPushButton(self.w_url_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_delete_url.sizePolicy().hasHeightForWidth())
        self.btn_delete_url.setSizePolicy(sizePolicy)
        self.btn_delete_url.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_delete_url.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_delete_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_url.setStyleSheet("QPushButton{\n"
                                          "    border-radius: 5px;\n"
                                          "    background: none;\n"
                                          "}\n"
                                          "\n"
                                          "\n"
                                          "QPushButton:pressed {\n"
                                          "     background-color: #072f49;\n"
                                          "}")
        self.btn_delete_url.setIcon(icon8)
        self.btn_delete_url.setIconSize(QtCore.QSize(21, 21))
        self.btn_delete_url.setObjectName("btn_delete_url")
        self.horizontalLayout_25.addWidget(self.btn_delete_url)
        self.verticalLayout_36.addLayout(self.horizontalLayout_25)
        self.verticalLayout_37 = QtWidgets.QVBoxLayout()
        self.verticalLayout_37.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_37.setSpacing(6)
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.label_19 = QtWidgets.QLabel(self.w_url_input)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.label_19.setFont(font)
        self.label_19.setIndent(1)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_37.addWidget(self.label_19)
        self.txt_url = QtWidgets.QLineEdit(self.w_url_input)
        self.txt_url.setEnabled(False)
        self.txt_url.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_url.setFont(font)
        self.txt_url.setObjectName("txt_url")
        self.verticalLayout_37.addWidget(self.txt_url)
        self.verticalLayout_36.addLayout(self.verticalLayout_37)
        self.w_url_btn = QtWidgets.QWidget(self.w_url_input)
        self.w_url_btn.setObjectName("w_url_btn")
        self.verticalLayout_41 = QtWidgets.QVBoxLayout(self.w_url_btn)
        self.verticalLayout_41.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_41.setContentsMargins(0, 10, 0, 0)
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
        self.verticalLayout_36.addWidget(self.w_url_btn)
        self.verticalLayout_42.addWidget(self.w_url_input)
        self.line_11 = QtWidgets.QFrame(self.widget_12)
        self.line_11.setStyleSheet("color: #0e4177;")
        self.line_11.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_11.setLineWidth(2)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setObjectName("line_11")
        self.verticalLayout_42.addWidget(self.line_11)
        self.w_url = QtWidgets.QWidget(self.widget_12)
        self.w_url.setObjectName("w_url")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.w_url)
        self.verticalLayout_4.setContentsMargins(15, 20, 15, 15)
        self.verticalLayout_4.setSpacing(15)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_24.setSpacing(6)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.lbl_url_status = QtWidgets.QLabel(self.w_url)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_url_status.sizePolicy().hasHeightForWidth())
        self.lbl_url_status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_url_status.setFont(font)
        self.lbl_url_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_url_status.setIndent(1)
        self.lbl_url_status.setObjectName("lbl_url_status")
        self.horizontalLayout_24.addWidget(self.lbl_url_status)
        spacerItem28 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_24.addItem(spacerItem28)
        self.btn_clear_url_table = QtWidgets.QPushButton(self.w_url)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_clear_url_table.sizePolicy().hasHeightForWidth())
        self.btn_clear_url_table.setSizePolicy(sizePolicy)
        self.btn_clear_url_table.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_clear_url_table.setMaximumSize(QtCore.QSize(30, 30))
        self.btn_clear_url_table.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_url_table.setStyleSheet("QPushButton{\n"
                                               "    border-radius: 5px;\n"
                                               "    background: none;\n"
                                               "}\n"
                                               "\n"
                                               "\n"
                                               "QPushButton:pressed {\n"
                                               "     background-color: #072f49;\n"
                                               "}")
        self.btn_clear_url_table.setIcon(icon2)
        self.btn_clear_url_table.setIconSize(QtCore.QSize(20, 20))
        self.btn_clear_url_table.setObjectName("btn_clear_url_table")
        self.horizontalLayout_24.addWidget(self.btn_clear_url_table)
        self.verticalLayout_4.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_57 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_57.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_57.setSpacing(0)
        self.horizontalLayout_57.setObjectName("horizontalLayout_57")
        self.txt_search_url = QtWidgets.QLineEdit(self.w_url)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_url.sizePolicy().hasHeightForWidth())
        self.txt_search_url.setSizePolicy(sizePolicy)
        self.txt_search_url.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_url.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_url.setFont(font)
        self.txt_search_url.setStyleSheet("border-radius: none;\n"
                                          "border-top-left-radius: 5px;\n"
                                          "border-bottom-left-radius: 5px;")
        self.txt_search_url.setObjectName("txt_search_url")
        self.horizontalLayout_57.addWidget(self.txt_search_url)
        self.btn_search_url = QtWidgets.QPushButton(self.w_url)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_url.sizePolicy().hasHeightForWidth())
        self.btn_search_url.setSizePolicy(sizePolicy)
        self.btn_search_url.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_url.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_url.setFont(font)
        self.btn_search_url.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_url.setStyleSheet("border-top-right-radius: 5px;\n"
                                          "border-bottom-right-radius: 5px;")
        self.btn_search_url.setText("")
        self.btn_search_url.setIcon(icon4)
        self.btn_search_url.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_url.setObjectName("btn_search_url")
        self.horizontalLayout_57.addWidget(self.btn_search_url)
        self.verticalLayout_4.addLayout(self.horizontalLayout_57)
        self.lv_url = ListView(self.w_url)
        self.lv_url.setObjectName("lv_url")
        self.verticalLayout_4.addWidget(self.lv_url)
        self.verticalLayout_42.addWidget(self.w_url)
        self.horizontalLayout_10.addWidget(self.widget_12)
        self.horizontalLayout_10.setStretch(0, 2)
        self.horizontalLayout_10.setStretch(1, 1)
        self.sw_all.addWidget(self.blacklisted_url)
        self.verticalLayout_2.addWidget(self.sw_all)
        self.horizontalLayout.addWidget(self.widget_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.lbl_database_status = QtWidgets.QLabel(self.status_bar)
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
        self.sw_student_section.setCurrentIndex(0)
        self.sw_teacher_attendance.setCurrentIndex(0)
        self.sw_class.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_students_and_sections.setText(
            _translate("MainWindow", "Sections & Students"))
        self.lbl_teachers_and_attendances.setText(
            _translate("MainWindow", "Teachers & Attendances"))
        self.lbl_classes_and_members.setText(
            _translate("MainWindow", "Classes & Members"))
        self.lbl_blacklisted_url.setText(
            _translate("MainWindow", "Blacklisted URLs"))
        self.lbl_sections_table_status.setText(
            _translate("MainWindow", "Sections: 0"))
        self.lbl_students_table_status.setText(
            _translate("MainWindow", "Students: 0"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Sections"))
        self.groupBox.setTitle(_translate("MainWindow", "Students"))
        self.label_11.setText(_translate("MainWindow", "Section"))
        self.label_12.setText(_translate("MainWindow", "Name"))
        self.btn_add_edit_section.setText(_translate("MainWindow", "Add"))
        self.btn_cancel_section.setText(_translate("MainWindow", "Cancel"))
        self.label_7.setText(_translate("MainWindow", "Student"))
        self.label_8.setText(_translate("MainWindow", "Username"))
        self.label_10.setText(_translate("MainWindow", "Password"))
        self.btn_add_edit_student.setText(_translate("MainWindow", "Add"))
        self.btn_cancel_student.setText(_translate("MainWindow", "Cancel"))
        self.lbl_section_students_status.setText(
            _translate("MainWindow", "Students: 0"))
        self.lbl_teachers_table_status.setText(
            _translate("MainWindow", "Teachers: 100"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Teachers"))
        self.label_15.setText(_translate("MainWindow", "Teacher"))
        self.label_16.setText(_translate("MainWindow", "Username"))
        self.label_18.setText(_translate("MainWindow", "Password"))
        self.btn_add_edit_teacher.setText(_translate("MainWindow", "Add"))
        self.btn_cancel_teacher.setText(_translate("MainWindow", "Cancel"))
        self.lbl_attendance_status.setText(
            _translate("MainWindow", "Attendances: 100"))
        self.lbl_class_table_status.setText(
            _translate("MainWindow", "Classes: 100"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Classes"))
        self.label_20.setText(_translate("MainWindow", "Class"))
        self.label_21.setText(_translate("MainWindow", "Code"))
        self.label_25.setText(_translate("MainWindow", "Name"))
        self.label_23.setText(_translate("MainWindow", "Start"))
        self.label_24.setText(_translate("MainWindow", "End"))
        self.btn_add_edit_class.setText(_translate("MainWindow", "Add"))
        self.btn_cancel_class.setText(_translate("MainWindow", "Cancel"))
        self.lbl_class_teacher_status.setText(
            _translate("MainWindow", "Teachers: 100"))
        self.lbl_class_section_status.setText(
            _translate("MainWindow", "Sections: 100"))
        self.label_17.setText(_translate("MainWindow", "URL"))
        self.label_19.setText(_translate("MainWindow", "Domain"))
        self.btn_add_edit_url.setText(_translate("MainWindow", "Add"))
        self.btn_cancel_url.setText(_translate("MainWindow", "Cancel"))
        self.lbl_url_status.setText(
            _translate("MainWindow", "URL: 100"))

    def disable_edit_delete(self):
        self.disable_section_edit_delete()
        self.disable_student_edit_delete()

    def hide_buttons(self):
        self.w_student_btn.hide()
        self.w_section_btn.hide()
        self.w_teacher_btn.hide()
        self.w_class_btn.hide()
        self.w_url_btn.hide()

    # ==Section
    def clear_section_inputs(self):
        self.txt_section_name.clear()

    def disable_section_buttons(self):
        self.btn_init_add_section.setDisabled(True)
        self.btn_init_edit_section.setDisabled(True)
        self.btn_delete_section.setDisabled(True)
        self.w_section_btn.show()

    def disable_section_edit_delete(self):
        self.btn_init_edit_section.setDisabled(True)
        self.btn_delete_section.setDisabled(True)

    def disable_section_student_delete_clear(self):
        self.btn_delete_section_student.setDisabled(True)
        self.btn_clear_section_student_table.setDisabled(True)

    def enable_section_edit_delete(self):
        self.btn_init_edit_section.setDisabled(False)
        self.btn_delete_section.setDisabled(False)

    def enable_section_student_delete_clear(self):
        self.btn_delete_section_student.setDisabled(False)
        self.btn_clear_section_student_table.setDisabled(False)

    def enable_section_buttons(self):
        self.btn_init_add_section.setDisabled(False)
        self.btn_init_edit_section.setDisabled(False)
        self.btn_delete_section.setDisabled(False)
        self.w_section_btn.hide()

    def disable_section_inputs(self):
        self.txt_section_name.setDisabled(True)

    def enable_section_inputs(self):
        self.txt_section_name.setDisabled(False)

    def set_section(self, value):
        self.section_state = value
        self.btn_add_edit_section.setText(value)

    # ==Student
    def clear_student_inputs(self):
        self.txt_student_username.clear()
        self.txt_student_password.operation.emit()

    def disable_student_buttons(self):
        self.btn_init_add_student.setDisabled(True)
        self.btn_init_edit_student.setDisabled(True)
        self.btn_delete_student.setDisabled(True)
        self.w_student_btn.show()

    def disable_student_edit_delete(self):
        self.btn_init_edit_student.setDisabled(True)
        self.btn_delete_student.setDisabled(True)

    def enable_student_edit_delete(self):
        self.btn_init_edit_student.setDisabled(False)
        self.btn_delete_student.setDisabled(False)

    def enable_student_buttons(self):
        self.btn_init_add_student.setDisabled(False)
        self.btn_init_edit_student.setDisabled(False)
        self.btn_delete_student.setDisabled(False)
        self.w_student_btn.hide()

    def disable_student_inputs(self):
        self.txt_student_username.setDisabled(True)
        self.txt_student_password.setDisabled(True)

    def enable_student_inputs(self):
        self.txt_student_username.setDisabled(False)
        self.txt_student_password.setDisabled(False)

    def set_student(self, value):
        self.student_state = value
        self.btn_add_edit_student.setText(value)

    # ==Teacher
    def clear_teacher_inputs(self):
        self.txt_teacher_username.clear()
        self.txt_teacher_password.operation.emit()

    def disable_teacher_buttons(self):
        self.btn_init_add_teacher.setDisabled(True)
        self.btn_init_edit_teacher.setDisabled(True)
        self.btn_delete_teacher.setDisabled(True)
        self.w_teacher_btn.show()
    
    def disable_teacher_edit_delete(self):
        self.btn_init_edit_teacher.setDisabled(True)
        self.btn_delete_teacher.setDisabled(True)

    def disable_teacher_attendance_delete_clear(self):
        self.btn_delete_attendance.setDisabled(True)
        self.btn_clear_attendance_table.setDisabled(True)

    def enable_teacher_attendance_delete_clear(self):
        self.btn_delete_attendance.setDisabled(False)
        self.btn_clear_attendance_table.setDisabled(False)

    def enable_teacher_edit_delete(self):
        self.btn_init_edit_teacher.setDisabled(False)
        self.btn_delete_teacher.setDisabled(False)

    def disable_teacher_attendance_edit_delete(self):
        self.btn_delete_attendance.setDisabled(True)
        self.btn_clear_attendance_table.setDisabled(True)

    def enable_teacher_attendance_edit_delete(self):
        self.btn_delete_attendance.setDisabled(False)
        self.btn_clear_attendance_table.setDisabled(False)

    def enable_teacher_buttons(self):
        self.btn_init_add_teacher.setDisabled(False)
        self.btn_init_edit_teacher.setDisabled(False)
        self.btn_delete_teacher.setDisabled(False)
        self.w_teacher_btn.hide()

    def disable_teacher_inputs(self):
        self.txt_teacher_username.setDisabled(True)
        self.txt_teacher_password.setDisabled(True)

    def enable_teacher_inputs(self):
        self.txt_teacher_username.setDisabled(False)
        self.txt_teacher_password.setDisabled(False)

    def set_teacher(self, value):
        self.teacher_state = value
        self.btn_add_edit_teacher.setText(value)

    # ==Class
    def clear_class_inputs(self):
        self.txt_class_code.clear()
        self.txt_class_name.clear()
        self.txt_class_start.setTime(QtCore.QTime(7, 0, 0))
        self.txt_class_end.setTime(QtCore.QTime(7, 0, 0))

    def disable_class_buttons(self):
        self.btn_init_add_class.setDisabled(True)
        self.btn_init_edit_class.setDisabled(True)
        self.btn_delete_class.setDisabled(True)
        self.w_class_btn.show()
        
    def disable_class_edit_delete(self):
        self.btn_init_edit_class.setDisabled(True)
        self.btn_delete_class.setDisabled(True)

    def disable_class_teacher_delete_clear(self):
        self.btn_delete_class_teacher.setDisabled(True)
        self.btn_clear_class_teacher.setDisabled(True)

    def disable_class_section_delete_clear(self):
        self.btn_delete_class_section.setDisabled(True)
        self.btn_clear_class_student.setDisabled(True)

    def enable_class_edit_delete(self):
        self.btn_init_edit_class.setDisabled(False)
        self.btn_delete_class.setDisabled(False)

    def enable_class_teacher_delete_clear(self):
        self.btn_delete_class_teacher.setDisabled(False)
        self.btn_clear_class_teacher.setDisabled(False)

    def enable_class_section_delete_clear(self):
        self.btn_init_add_class_teacher.setDisabled(False)
        self.btn_delete_class_section.setDisabled(False)
        self.btn_clear_class_student.setDisabled(False)

    def enable_class_buttons(self):
        self.btn_init_add_class.setDisabled(False)
        self.btn_init_edit_class.setDisabled(False)
        self.btn_delete_class.setDisabled(False)
        self.w_class_btn.hide()

    def disable_class_inputs(self):
        self.txt_class_code.setDisabled(True)
        self.txt_class_name.setDisabled(True)
        self.txt_class_start.setDisabled(True)
        self.txt_class_end.setDisabled(True)

    def enable_class_inputs(self):
        self.txt_class_code.setDisabled(False)
        self.txt_class_name.setDisabled(False)
        self.txt_class_start.setDisabled(False)
        self.txt_class_end.setDisabled(False)

    def set_class(self, value):
        self.class_state = value
        self.btn_add_edit_class.setText(value)

    # URL
    def clear_url_inputs(self):
        self.txt_url.clear()

    def disable_url_edit_delete(self):
        self.btn_init_edit_url.setDisabled(True)
        self.btn_delete_url.setDisabled(True)

    def disable_url_buttons(self):
        self.btn_init_add_url.setDisabled(True)
        self.btn_init_edit_url.setDisabled(True)
        self.btn_delete_url.setDisabled(True)
        self.w_url_btn.show()

    def enable_url_edit_delete(self):
        self.btn_init_edit_url.setDisabled(False)
        self.btn_delete_url.setDisabled(False)

    def enable_url_buttons(self):
        self.btn_init_add_url.setDisabled(False)
        self.btn_init_edit_url.setDisabled(False)
        self.btn_delete_url.setDisabled(False)
        self.w_url_btn.hide()

    def disable_url_inputs(self):
        self.txt_url.setDisabled(True)

    def enable_url_inputs(self):
        self.txt_url.setDisabled(False)

    def set_url(self, value):
        self.url_state = value
        self.btn_add_edit_url.setText(value)

    def run_popup(self, message, icon='information'):
        if icon == 'question':
            self.Popup.lbl_icon.setPixmap(QtGui.QPixmap(relative_path(
            'Admin', ['Misc', 'Resources'], 'question.png')))
        elif icon == 'warning':
            self.Popup.lbl_icon.setPixmap(QtGui.QPixmap(relative_path(
            'Admin', ['Misc', 'Resources'], 'warning.png')))
        elif icon == 'critical':
            self.Popup.lbl_icon.setPixmap(QtGui.QPixmap(relative_path(
            'Admin', ['Misc', 'Resources'], 'critical.png')))
        
        self.Popup.lbl_message.setText(message)
        self.Popup.run()

    def set_database_status(self, text):
        self.lbl_database_status.setText(text)
    
    def show_confirm(self, next_step, message=None):
        self.Confirm = Confirm(self.View, message)
        self.Confirm.operation.connect(next_step)
        self.Confirm.operation.connect(self.Confirm.close)
        self.Confirm.run()

    def show_menu(self, next_step, pos):
        self.ContextMenu = ContextMenu(self)
        self.ContextMenu.delete.connect(next_step)
        self.ContextMenu.move(pos.x(), pos.y())
        self.ContextMenu.show()

    def add_section_item(self):
        sectionItem = SectionItem(self)
        sectionItem.setObjectName(f"sectionItem_{self.verticalLayout_53.count()}")
        self.verticalLayout_53.insertWidget(0, sectionItem)
        self.btn_add_section_bulk.setDisabled(False)

    def clear_section_item(self):
        for index in range(self.verticalLayout_53.count()-1):
            target = self.verticalLayout_53.itemAt(index).widget()
            target.close()
            target.deleteLater()
        self.btn_add_section_bulk.setDisabled(True)

    def add_student_item(self):
        student_item = StudentItem(self)
        student_item.setObjectName(f"studentItem_{self.verticalLayout_38.count()}")
        self.verticalLayout_38.insertWidget(0, student_item)
        self.btn_add_student_bulk.setDisabled(False)
        
    def clear_student_item(self):
        for index in range(self.verticalLayout_38.count()-1):
            target = self.verticalLayout_38.itemAt(index).widget()
            target.close()
            target.deleteLater()
        self.btn_add_student_bulk.setDisabled(True)

    def add_teacher_item(self):
        teacher_item = TeacherItem(self)
        teacher_item.setObjectName(f"teacherItem_{self.verticalLayout_47.count()}")
        self.verticalLayout_47.insertWidget(0, teacher_item)
        self.btn_add_teacher_bulk.setDisabled(False)
        
    def clear_teacher_item(self):
        for index in range(self.verticalLayout_47.count()-1):
            target = self.verticalLayout_47.itemAt(index).widget()
            target.close()
            target.deleteLater()
        self.btn_add_teacher_bulk.setDisabled(True)

    def add_class_item(self):
        class_item = ClassItem(self)
        class_item.setObjectName(f"classItem_{self.verticalLayout_50.count()}")
        self.verticalLayout_50.insertWidget(0, class_item)
        self.btn_add_class_bulk.setDisabled(False)
        
    def clear_class_item(self):
        for index in range(self.verticalLayout_50.count()-1):
            target = self.verticalLayout_50.itemAt(index).widget()
            target.close()
            target.deleteLater()
        self.btn_add_class_bulk.setDisabled(True)

    def set_admin_status(self, status):
        self.lbl_database_status.setText(status)

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()