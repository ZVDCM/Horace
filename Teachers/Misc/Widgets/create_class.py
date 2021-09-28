from Teachers.Misc.Widgets.custom_list_view import ListView, ReadOnlyListView
from Teachers.Misc.Widgets.dialog_title_bar import TitleBar
from Teachers.Misc.Widgets.active_overlay import ActiveOverlay
from Teachers.Misc.Widgets.loading_screen import LoadingScreen
from Teachers.Misc.Functions.relative_path import relative_path
from PyQt5 import QtCore, QtGui, QtWidgets


class Get(QtCore.QThread):
    operation = QtCore.pyqtSignal(object)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = ()

    def run(self):
        res = self.fn(*self.val)
        self.operation.emit(res)
        self.quit()


class Operation(QtCore.QThread):
    operation = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(str)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = ()

    def run(self):
        res = self.fn(*self.val)
        if res == 'successful':
            self.operation.emit()
        else:
            self.error.emit(res)
        self.quit()


class CreateClass(QtWidgets.QDialog):

    def __init__(self, parent, Model):
        super().__init__()
        self.parent = parent
        self.Model = Model
        self.setupUi(self)

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)
        self.SectionLoadingScreen = LoadingScreen(self.lv_section, relative_path(
            'Teachers', ['Misc', 'Resources'], 'loading_bars.gif'))
        self.StudentLoadingScreen = LoadingScreen(self.lv_student, relative_path(
            'Teachers', ['Misc', 'Resources'], 'loading_bars.gif'))

        self.connect_signals()


    def run(self):
        self.get_all_section()
        self.activateWindow()
        self.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setMinimumSize(QtCore.QSize(779, 831))
        Dialog.setMaximumSize(QtCore.QSize(779, 831))
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                              QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        Dialog.setStyleSheet("QWidget{\n"
                             "    background: #102542;\n"
                             "    color: white; \n"
                             "    font-family: Barlow\n"
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
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.title_bar = TitleBar(self)
        self.title_bar.setStyleSheet("background: #102542;")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_4.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setSpacing(20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_title = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(14)
        self.lbl_title.setFont(font)
        self.lbl_title.setStyleSheet("")
        self.lbl_title.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lbl_title.setIndent(1)
        self.lbl_title.setObjectName("lbl_title")
        self.horizontalLayout_3.addWidget(self.lbl_title)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_5.setSpacing(25)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout()
        self.verticalLayout_27.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_27.setContentsMargins(-1, 0, 0, 0)
        self.verticalLayout_27.setSpacing(10)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.label_21 = QtWidgets.QLabel(self.groupBox_2)
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
        self.label_21.setObjectName("label_21")
        self.verticalLayout_27.addWidget(self.label_21)
        self.txt_class_code = QtWidgets.QLineEdit(self.groupBox_2)
        self.txt_class_code.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_class_code.setFont(font)
        self.txt_class_code.setMaxLength(8)
        self.txt_class_code.setObjectName("txt_class_code")
        self.verticalLayout_27.addWidget(self.txt_class_code)
        self.label_25 = QtWidgets.QLabel(self.groupBox_2)
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
        self.label_25.setObjectName("label_25")
        self.verticalLayout_27.addWidget(self.label_25)
        self.txt_class_name = QtWidgets.QLineEdit(self.groupBox_2)
        self.txt_class_name.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_class_name.setFont(font)
        self.txt_class_name.setObjectName("txt_class_name")
        self.verticalLayout_27.addWidget(self.txt_class_name)
        self.label_23 = QtWidgets.QLabel(self.groupBox_2)
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
        self.te_class_start = QtWidgets.QTimeEdit(self.groupBox_2)
        self.te_class_start.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.te_class_start.setFont(font)
        self.te_class_start.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        self.te_class_start.setTime(QtCore.QTime(7, 0, 0))
        self.te_class_start.setObjectName("te_class_start")
        self.verticalLayout_27.addWidget(self.te_class_start)
        self.label_24 = QtWidgets.QLabel(self.groupBox_2)
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
        self.te_class_end = QtWidgets.QTimeEdit(self.groupBox_2)
        self.te_class_end.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.te_class_end.setFont(font)
        self.te_class_end.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons)
        self.te_class_end.setTime(QtCore.QTime(7, 0, 0))
        self.te_class_end.setObjectName("te_class_end")
        self.verticalLayout_27.addWidget(self.te_class_end)
        self.verticalLayout_5.addLayout(self.verticalLayout_27)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btn_create_edit = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_create_edit.setFont(font)
        self.btn_create_edit.setStyleSheet("border-radius: 5px;")
        self.btn_create_edit.setObjectName("btn_create_edit")
        self.verticalLayout_6.addWidget(self.btn_create_edit)
        self.btn_cancel = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setStyleSheet("QPushButton{\n"
                                      "    border-radius: 5px;\n"
                                      "    background: none;\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:pressed {\n"
                                      "     background-color: #072f49;\n"
                                      "}")
        self.btn_cancel.setObjectName("btn_cancel")
        self.verticalLayout_6.addWidget(self.btn_cancel)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_48.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_48.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_48.setSpacing(0)
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")
        self.txt_search_section = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_search_section.sizePolicy().hasHeightForWidth())
        self.txt_search_section.setSizePolicy(sizePolicy)
        self.txt_search_section.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_search_section.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_search_section.setFont(font)
        self.txt_search_section.setStyleSheet("border-radius: none;\n"
                                              "border-top-left-radius: 5px;\n"
                                              "border-bottom-left-radius: 5px;")
        self.txt_search_section.setObjectName("txt_search_section")
        self.horizontalLayout_48.addWidget(self.txt_search_section)
        self.btn_search_section = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_section.sizePolicy().hasHeightForWidth())
        self.btn_search_section.setSizePolicy(sizePolicy)
        self.btn_search_section.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_section.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_section.setFont(font)
        self.btn_search_section.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_section.setStyleSheet("border-top-right-radius: 5px;\n"
                                              "border-bottom-right-radius: 5px;")
        self.btn_search_section.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(relative_path('Teachers', ['Misc', 'Resources'], 'search.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search_section.setIcon(icon)
        self.btn_search_section.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_section.setObjectName("btn_search_section")
        self.horizontalLayout_48.addWidget(self.btn_search_section)
        self.verticalLayout.addLayout(self.horizontalLayout_48)
        self.lv_section = ListView(self.groupBox)
        self.lv_section.setObjectName("lv_section")
        self.verticalLayout.addWidget(self.lv_section)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.groupBox_21 = QtWidgets.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.groupBox_21.setFont(font)
        self.groupBox_21.setObjectName("groupBox_21")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_21)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(
            QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.groupBox_21)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2.addWidget(self.frame)
        self.horizontalLayout_49 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_49.setSizeConstraint(
            QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_49.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_49.setSpacing(0)
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        self.txt_search_student = QtWidgets.QLineEdit(self.groupBox_21)
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
        self.horizontalLayout_49.addWidget(self.txt_search_student)
        self.btn_search_student = QtWidgets.QPushButton(self.groupBox_21)
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
        self.btn_search_student.setIcon(icon)
        self.btn_search_student.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_student.setObjectName("btn_search_student")
        self.horizontalLayout_49.addWidget(self.btn_search_student)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_49)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.lv_student = ReadOnlyListView(self.groupBox_21)
        self.lv_student.setObjectName("lv_student")
        self.verticalLayout_2.addWidget(self.lv_student)
        self.verticalLayout_3.addWidget(self.groupBox_21)
        self.verticalLayout_4.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_title.setText(_translate("Dialog", "Create Class"))
        self.groupBox_2.setTitle(_translate("Dialog", "Class"))
        self.label_21.setText(_translate("Dialog", "Code"))
        self.label_25.setText(_translate("Dialog", "Name"))
        self.label_23.setText(_translate("Dialog", "Start"))
        self.label_24.setText(_translate("Dialog", "End"))
        self.btn_create_edit.setText(_translate("Dialog", "Create"))
        self.btn_cancel.setText(_translate("Dialog", "Cancel"))
        self.groupBox.setTitle(_translate("Dialog", "Section"))
        self.groupBox_21.setTitle(_translate("Dialog", "Students"))

    def connect_signals(self):
        self.lv_section.clicked.connect(self.section_list_clicked)

    def GetAllSection(self):
        handler = Get(self.Model.get_all_section)
        handler.started.connect(self.SectionLoadingScreen.run)
        handler.operation.connect(self.set_section_model)
        handler.finished.connect(self.SectionLoadingScreen.hide)
        return handler

    def GetAllSectionStudent(self):
        handler = Get(self.Model.get_all_section_student)
        handler.started.connect(self.StudentLoadingScreen.run)
        handler.operation.connect(self.set_section_student_model)
        handler.finished.connect(self.StudentLoadingScreen.hide)
        return handler

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    def get_all_section(self):
        self.get_all_section_handler = self.GetAllSection()
        self.get_all_section_handler.start()

    def set_section_model(self, sections):
        print(sections)
        sections_model = self.Model.ListModel(self.lv_section, sections)
        self.lv_section.setModel(sections_model)
        self.lv_section.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        index = self.lv_section.model().createIndex(0, 0)
        self.lv_section.setCurrentIndex(index)
        self.lv_section.setFocus(True)

        self.get_section_students(sections[0])

    def get_section_students(self, section):
        self.get_all_section_student_handler = self.GetAllSectionStudent()
        self.get_all_section_student_handler.val = section,
        self.get_all_section_student_handler.start()

    def set_section_student_model(self, section_students):
        section_student_model = self.Model.ReadOnlyListModel(self.lv_student, section_students)
        self.lv_student.setModel(section_student_model)
        self.lv_student.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        index = self.lv_student.model().createIndex(0, 0)
        self.lv_student.setCurrentIndex(index)

    def section_list_clicked(self, index):
        row = index.row()
        section_model = self.lv_section.model()
        section = section_model.getRowData(row)
        print(section)
        self.get_section_students(section)