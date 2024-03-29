import os
from PyQt5 import QtCore, QtGui, QtWidgets
from Admin.Misc.Widgets.title_bar import TitleBar
from Admin.Misc.Widgets.active_overlay import ActiveOverlay


class Import(QtWidgets.QDialog):
    operation = QtCore.pyqtSignal(str, str, str)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.connect_signals()

        self.title_bar.title.setText('Import sections and students files')

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)

        self.section = None
        self.student = None
        self.section_students = None

    def run(self):
        self.activateWindow()
        self.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(583, 396)
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Dialog.setFocusPolicy(QtCore.Qt.StrongFocus)
        Dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        Dialog.setStyleSheet("""
                            QWidget{
                                background: #102542;
                                color: white; 
                                font-family: Barlow
                            }
                            
                            QLineEdit {
                                padding: 5px;
                                border: 1px solid #0e4884;
                                border-radius: 5px;
                            }
                            
                            QPushButton {
                            padding: 5px 8px;
                            border: 1px solid #0e4884;
                            background-color: #0e4884;
                            }
                            
                            QPushButton::disabled {
                            padding: 5px;
                            color: gray;
                            border: 1px solid #0B1A30;
                            background-color: #0B1A30;
                            }
                            
                            QPushButton:focus,
                            QPushButton:hover {
                            border: 1px solid #256eff;
                            outline: none;
                            }
                            
                            QPushButton:pressed {
                            background-color: #072f49;
                            }
                            
                            QTableView{
                                border: 1px solid #0e4884;
                            }
                            
                            QHeaderView::section {
                                background-color: #0d3c6e;
                                border-top: 0px solid #97b9f4;
                                border-bottom: 1px solid #97b9f4;
                                border-right: 1px solid #97b9f4;
                            }
                            
                            QTableView {
                                outline: 0;
                                border: 1px solid #0e4884;
                                gridline-color: #97b9f4;
                            }

                            QTableView::item {
                                border: none;
                                padding-left: 10px;
                            }

                            QTableView::item:selected:active {
                                border: none;
                                background: #0078D7;
                            }

                            QTableView::item:selected:!active {
                                border: none;
                                background: white;
                                color: black;
                            }

                            QHeaderView::section {
                                background-color: #0d3c6e;
                                border-top: 0px solid #97b9f4;
                                border-bottom: 1px solid #97b9f4;
                                border-right: 1px solid #97b9f4;
                            }
                            
                            QTableCornerButton::section{
                                background-color: #0d3c6e;
                                border-top: 0px solid #97b9f4;
                                border-bottom: 1px solid #97b9f4;
                                border-right: 1px solid #97b9f4;
                            }
                            
                            QScrollBar:horizontal{
                                height: 9px;
                                background-color: #102542;    
                            }
                            
                            QScrollBar:vertical{
                                background-color: #102542;    
                                width: 9px;
                            }
                            
                            QScrollBar::handle:vertical{
                                background-color: #97b9f4;    
                                width: 18px;
                            }
                            
                            QScrollBar::handle:horizontal{
                                background-color: #97b9f4;    
                                min-width: 5px;
                            }
                            
                            QScrollBar::sub-line:horizontal,
                            QScrollBar::sub-line:vertical{
                                height: 0;
                                width: 0;
                            }
                            
                            QScrollBar::add-line:horizontal,
                            QScrollBar::add-line:vertical{
                                height: 0;
                                width: 0;
                            }
                            
                            QScrollBar::add-page:horizontal{
                                background: #102542;
                                margin-left: -3px;
                            }
                            
                            QScrollBar::add-page:vertical{
                                background: #102542;
                                margin-top: -3px;
                            }
                            
                            QScrollBar::sub-page:horizontal{
                                background: #102542;
                                margin-right: -3px;
                            }
                            
                            QScrollBar::sub-page:vertical{
                                background: #102542;
                                margin-bottom: -3px;
                            }
                             """)
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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(
            78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 2)
        self.btn_section_student = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_section_student.setFont(font)
        self.btn_section_student.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_section_student.setStyleSheet("border-radius: 5px;")
        self.btn_section_student.setObjectName("btn_section_student")
        self.gridLayout.addWidget(self.btn_section_student, 5, 2, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 1, 1, 1)
        self.txt_student = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_student.setFont(font)
        self.txt_student.setReadOnly(True)
        self.txt_student.setObjectName("txt_student")
        self.gridLayout.addWidget(self.txt_student, 2, 1, 1, 3)
        self.btn_section = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_section.setFont(font)
        self.btn_section.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_section.setStyleSheet("border-radius: 5px;")
        self.btn_section.setObjectName("btn_section")
        self.gridLayout.addWidget(self.btn_section, 1, 3, 1, 1)
        self.txt_section_student = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_section_student.setFont(font)
        self.txt_section_student.setReadOnly(True)
        self.txt_section_student.setObjectName("txt_section_student")
        self.gridLayout.addWidget(self.txt_section_student, 4, 1, 1, 3)
        self.txt_section = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.txt_section.setFont(font)
        self.txt_section.setReadOnly(True)
        self.txt_section.setObjectName("txt_section")
        self.gridLayout.addWidget(self.txt_section, 0, 1, 1, 3)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 2, 1)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.widget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
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
        self.gridLayout.addWidget(self.tableWidget_2, 2, 0, 2, 1)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.widget)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_3.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 2, item)
        self.gridLayout.addWidget(self.tableWidget_3, 4, 0, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            88, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 1, 1, 2)
        self.btn_student = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_student.setFont(font)
        self.btn_student.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_student.setStyleSheet("border-radius: 5px;")
        self.btn_student.setObjectName("btn_student")
        self.gridLayout.addWidget(self.btn_student, 3, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(11)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setStyleSheet("QPushButton{\n"
                                        "border-radius: 5px;\n"
                                        "background-color: none;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed{\n"
                                        "  background-color: #072f49;\n"
                                        "}\n")
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
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
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.btn_section_student.setText(
            _translate("Dialog", "Import Section Students"))
        self.txt_student.setPlaceholderText(
            _translate("Dialog", "Students Table.csv"))
        self.btn_section.setText(_translate("Dialog", "Import Sections"))
        self.txt_section_student.setPlaceholderText(
            _translate("Dialog", "Section Students Table.csv"))
        self.txt_section.setPlaceholderText(
            _translate("Dialog", "Section Table.csv"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Name"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Dialog", "Section"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
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
        item.setText(_translate("Dialog", "Juan"))
        item = self.tableWidget_2.item(0, 2)
        item.setText(_translate("Dialog", "Student"))
        item = self.tableWidget_2.item(0, 3)
        item.setText(_translate("Dialog", "$2b$14$CvyVRP55XtLdY/zYj6/ixu"))
        item = self.tableWidget_2.item(0, 4)
        item.setText(_translate("Dialog", "a4qNHklO8jfF6eRlrqCMBnQCb6dO/nW"))
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)
        item = self.tableWidget_3.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "ID"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Section"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Student"))
        __sortingEnabled = self.tableWidget_3.isSortingEnabled()
        self.tableWidget_3.setSortingEnabled(False)
        item = self.tableWidget_3.item(0, 0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_3.item(0, 1)
        item.setText(_translate("Dialog", "Section"))
        item = self.tableWidget_3.item(0, 2)
        item.setText(_translate("Dialog", "Juan"))
        self.tableWidget_3.setSortingEnabled(__sortingEnabled)
        self.btn_student.setText(_translate("Dialog", "Import Students"))
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

        self.btn_section.clicked.connect(self.get_section)
        self.btn_student.clicked.connect(self.get_student)
        self.btn_section_student.clicked.connect(self.get_section_student)

    def import_files(self):
        self.operation.emit(self.section, self.student, self.section_students)
        self.close()

    def get_file(self, target_file):
        default_path = os.path.expanduser('~/Documents')
        path = QtWidgets.QFileDialog.getOpenFileName(
                self, f'Select {target_file}', default_path, 'CSV (*.csv)')
        return path[0], path[0].split('/')[-1]
        
    def get_section(self):
        path = self.get_file('Section Table File')
        if path[0]:
            self.section = path[0]
            self.txt_section.setText(path[1])

            self.btn_import.setEnabled(True)

    def get_student(self):
        path = self.get_file('Student Table File')
        if path[0]:
            self.student = path[0]
            self.txt_student.setText(path[1])

            self.btn_import.setEnabled(True)

    def get_section_student(self):
        path = self.get_file('Section Students Table File')
        if path[0]:
            self.section_students = path[0]
            self.txt_section_student.setText(path[1])

            self.btn_import.setEnabled(True)
    
    def keyPressEvent(self, event):
        if event.key() == 16777220:
            return
        super().keyPressEvent(event)