import os
from PyQt5 import QtCore, QtGui, QtWidgets
from Admin.Misc.Widgets.title_bar import TitleBar
from Admin.Misc.Widgets.active_overlay import ActiveOverlay


class Import(QtWidgets.QDialog):
    operation = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.connect_signals()

        self.title_bar.title.setText('Import teacher file')

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)

        self.teacher = None

    def run(self):
        self.activateWindow()
        self.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(583, 208)
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Dialog.setStyleSheet("QWidget{\n"
                             "    background: #102542;\n"
                             "    color: white; \n"
                             "    font-family: Barlow\n"
                             "}\n"
                             "\n"
                             "QLineEdit {\n"
                             "      padding: 5px;\n"
                             "      border: 1px solid #0e4884;\n"
                             "      border-radius: 5px;\n"
                             "}\n"
                             "\n"
                             "QPushButton {\n"
                             "  padding: 5px 8px;\n"
                             "  border: 1px solid #0e4884;\n"
                             "  background-color: #0e4884;\n"
                             "}\n"
                             "\n"
                             "QPushButton::disabled {\n"
                             "  padding: 5px;\n"
                             " color: gray;\n"
                             "  border: 1px solid #0B1A30;\n"
                             "  background-color: #0B1A30;\n"
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
                             "QTableView{\n"
                             "    border: 1px solid #0e4884;\n"
                             "}\n"
                             "\n"
                             "QHeaderView::section {\n"
                             "    background-color: #0d3c6e;\n"
                             "    border-top: 0px solid #97b9f4;\n"
                             "    border-bottom: 1px solid #97b9f4;\n"
                             "    border-right: 1px solid #97b9f4;\n"
                             "}\n"
                             "\n"
                             "QTableView {\n"
                             "    gridline-color: #97b9f4;\n"
                             "}\n"
                             "\n"
                             "QTableCornerButton::section{\n"
                             "    background-color: #0d3c6e;\n"
                             "    border-top: 0px solid #97b9f4;\n"
                             "    border-bottom: 1px solid #97b9f4;\n"
                             "    border-right: 1px solid #97b9f4;\n"
                             "}\n"
                             "\n"
                             "QScrollBar:horizontal{\n"
                             "    height: 9px;\n"
                             "    border-radius: 5px;\n"
                             "}\n"
                             "\n"
                             "QScrollBar:vertical{\n"
                             "    width: 9px;\n"
                             "    margin: 0;\n"
                             "    border-radius: 5px;\n"
                             "}\n"
                             "\n"
                             "QScrollBar::handle:vertical{\n"
                             "    background-color: #97b9f4;    \n"
                             "    width: 18px;\n"
                             "    border-radius: 4px;\n"
                             "}\n"
                             "\n"
                             "QScrollBar::handle:horizontal{\n"
                             "    background-color: #97b9f4;    \n"
                             "    min-width: 5px;\n"
                             "    border-radius: 4px;\n"
                             "}\n"
                             "\n"
                             "QScrollBar::sub-line:horizontal,\n"
                             "QScrollBar::sub-line:vertical{\n"
                             "    height: 0;\n"
                             "    width: 0;\n"
                             "}\n"
                             "\n"
                             "QScrollBar::add-line:horizontal,\n"
                             "QScrollBar::add-line:vertical{\n"
                             "    height: 0;\n"
                             "    width: 0;\n"
                             "}\n"
                             "\n"
                             "QScrollBar::add-page:horizontal{\n"
                             "    background: #102542;\n"
                             "    border-top-right-radius: 4px;\n"
                             "    border-bottom-right-radius: 4px;\n"
                             "    margin-left: -3px;\n"
                             "}\n"
                             "\n"
                             "QScrollBar::add-page:vertical{\n"
                             "    background: #102542;\n"
                             "    border-bottom-left-radius: 4px;\n"
                             "    border-bottom-right-radius: 4px;\n"
                             "    margin-top: -3px;\n"
                             "}\n"
                             "\n"
                             "QScrollBar::sub-page:horizontal{\n"
                             "    background: #102542;\n"
                             "    border-bottom-left-radius: 4px;\n"
                             "    margin-right: -3px;\n"
                             "}\n"
                             "\n"
                             "QScrollBar::sub-page:vertical{\n"
                             "    background: #102542;\n"
                             "    border-top-left-radius: 0;\n"
                             "    border-top-right-radius: 4px;\n"
                             "    margin-bottom: -3px;\n"
                             "}\n"
                             "")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_bar = TitleBar(self)
        self.title_bar.setMinimumSize(QtCore.QSize(0, 30))
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title_bar.setStyleSheet("")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_2.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(20, 15, 20, 25)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setHorizontalSpacing(20)
        self.gridLayout_2.setVerticalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_teachers = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_teachers.setFont(font)
        self.btn_teachers.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_teachers.setStyleSheet("border-radius: 5px;")
        self.btn_teachers.setObjectName("btn_teachers")
        self.gridLayout_2.addWidget(self.btn_teachers, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            128, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 2)
        self.txt_teacher = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_teacher.setFont(font)
        self.txt_teacher.setReadOnly(True)
        self.txt_teacher.setObjectName("txt_teacher")
        self.gridLayout_2.addWidget(self.txt_teacher, 0, 1, 1, 3)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.widget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 4, item)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(False)
        self.gridLayout_2.addWidget(self.tableWidget_2, 0, 0, 2, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(11)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setStyleSheet(
            "border-radius: 5px;    background-color: none;")
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_import = QtWidgets.QPushButton(self.widget)
        self.btn_import.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(11)
        self.btn_import.setFont(font)
        self.btn_import.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_import.setStyleSheet("border-radius: 5px;")
        self.btn_import.setObjectName("btn_import")
        self.horizontalLayout.addWidget(self.btn_import)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.btn_teachers.setText(_translate("Dialog", "Import Teachers"))
        self.txt_teacher.setPlaceholderText(
            _translate("Dialog", "Teachers Table.csv"))
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "UserID"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Username"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Privilege"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Salt"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Hash"))
        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        item = self.tableWidget_2.item(0, 0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_2.item(0, 1)
        item.setText(_translate("Dialog", "Maria"))
        item = self.tableWidget_2.item(0, 2)
        item.setText(_translate("Dialog", "Teacher"))
        item = self.tableWidget_2.item(0, 3)
        item.setText(_translate("Dialog", "$2b$14$CvyVRP55XtLdY/zYj6/ixu"))
        item = self.tableWidget_2.item(0, 4)
        item.setText(_translate("Dialog", "a4qNHklO8jfF6eRlrqCMBnQCb6dO/nW"))
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)
        self.btn_cancel.setText(_translate("Dialog", "Cancel"))
        self.btn_import.setText(_translate("Dialog", "Import"))

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    def connect_signals(self):
        self.btn_cancel.clicked.connect(self.close)
        self.btn_import.clicked.connect(self.import_files)

        self.btn_teachers.clicked.connect(self.get_teacher)

    def import_files(self):
        self.operation.emit(self.teacher)
        self.close()

    def get_file(self, target_file):
        default_path = os.path.expanduser('~/Documents')
        path = QtWidgets.QFileDialog.getOpenFileName(
                self, f'Select {target_file}', default_path, 'CSV (*.csv)')
        return path[0], path[0].split('/')[-1]
        
    def get_teacher(self):
        path = self.get_file('Teacher Table File')
        if path[0]:
            self.teacher = path[0]
            self.txt_teacher.setText(path[1])

            self.btn_import.setEnabled(True)
