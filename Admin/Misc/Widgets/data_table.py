from PyQt5 import QtCore, QtGui, QtWidgets
from Admin.Misc.Widgets.title_bar import TitleBar
from Admin.Misc.Widgets.loading_screen import LoadingScreen
from Admin.Misc.Widgets.active_overlay import ActiveOverlay
from Admin.Misc.Widgets.custom_table_view import TableView
from Admin.Misc.Functions.relative_path import relative_path

class DataTable(QtWidgets.QDialog):

    def __init__(self, parent, target_table, target_column, table_model):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.target_table = target_table
        self.target_column = target_column
        self.table_model = table_model
        self.target_row = self.table_model.rowCount() - 2

        self.lbl_target_table.setText(self.target_table)
        self.tv_target_data.setModel(self.table_model)
        self.tv_target_data.horizontalHeader().setMinimumSectionSize(150)
        self.tv_target_data.setFocus(True)
        self.tv_target_data.selectRow(self.target_row)

        self.remove_null_row()

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)

        self.LoadingScreen = LoadingScreen(self.widget, relative_path(
            'Admin', ['Misc', 'Resources'], 'loading_squares.gif'))
        self.ActiveOverlay = ActiveOverlay(self)

        self.connect_signals()

    def run(self):
        self.activateWindow()
        self.exec_()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(711, 427)
        Form.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                              QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setStyleSheet("QWidget{\n"
                           "    background: #102542;\n"
                           "    color: white; \n"
                           "    font-family: Barlow\n"
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
                           )
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title_bar = TitleBar(self)
        self.title_bar.setMinimumSize(QtCore.QSize(0, 30))
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title_bar.setStyleSheet("background: #102542;")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_2.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(25, 25, 25, 25)
        self.verticalLayout.setSpacing(25)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_target_table = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(14)
        self.lbl_target_table.setFont(font)
        self.lbl_target_table.setObjectName("lbl_target_table")
        self.horizontalLayout.addWidget(self.lbl_target_table)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_54 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_54.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_54.setSpacing(0)
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")
        self.tv_search_target = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tv_search_target.sizePolicy().hasHeightForWidth())
        self.tv_search_target.setSizePolicy(sizePolicy)
        self.tv_search_target.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.tv_search_target.setFont(font)
        self.tv_search_target.setStyleSheet("border-radius: none;\n"
                                            "border-top-left-radius: 5px;\n"
                                            "border-bottom-left-radius: 5px;")
        self.tv_search_target.setObjectName("tv_search_target")
        self.horizontalLayout_54.addWidget(self.tv_search_target)
        self.btn_search_target = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_search_target.sizePolicy().hasHeightForWidth())
        self.btn_search_target.setSizePolicy(sizePolicy)
        self.btn_search_target.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_search_target.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_search_target.setFont(font)
        self.btn_search_target.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_search_target.setStyleSheet("border-top-right-radius: 5px;\n"
                                             "border-bottom-right-radius: 5px;")
        self.btn_search_target.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(relative_path('Admin', ['Misc', 'Resources'], 'search.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search_target.setIcon(icon)
        self.btn_search_target.setIconSize(QtCore.QSize(18, 18))
        self.btn_search_target.setObjectName("btn_search_target")
        self.horizontalLayout_54.addWidget(self.btn_search_target)
        self.horizontalLayout.addLayout(self.horizontalLayout_54)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tv_target_data = TableView(self.widget)
        self.tv_target_data.setObjectName("tv_target_data")
        self.verticalLayout.addWidget(self.tv_target_data)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        self.btn_cancel.setMinimumSize(QtCore.QSize(150, 0))
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
        self.horizontalLayout_3.addWidget(self.btn_cancel)
        spacerItem1 = QtWidgets.QSpacerItem(
            0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btn_set = QtWidgets.QPushButton(self.widget)
        self.btn_set.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.btn_set.setFont(font)
        self.btn_set.setStyleSheet("border-radius: 5px;")
        self.btn_set.setObjectName("btn_set")
        self.horizontalLayout_3.addWidget(self.btn_set)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_target_table.setText(_translate("Form", "Table"))
        self.btn_cancel.setText(_translate("Form", "Cancel"))
        self.btn_set.setText(_translate("Form", "Set"))

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.is_focused = True
            self.ActiveOverlay.update()
        else:
            self.ActiveOverlay.is_focused = False
            self.ActiveOverlay.update()

    def connect_signals(self):
        self.tv_target_data.clicked.connect(self.table_clicked)
        self.btn_cancel.clicked.connect(self.close)

    def table_clicked(self, item):
        self.target_row = item.row()

    def remove_null_row(self):
        table_model = self.tv_target_data.model()
        last_row_index = table_model.rowCount() - 1
        self.tv_target_data.setRowHidden(last_row_index, True)



