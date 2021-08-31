from PyQt5 import QtCore, QtGui, QtWidgets
from SignIn.Misc.Widgets.title_bar import TitleBar
from SignIn.Misc.Widgets.custom_lineedit import AdminPassword
from SignIn.Misc.Widgets.active_overlay import ActiveOverlay
from SignIn.Misc.Functions.relative_path import relative_path
from SignIn.Misc.Functions.is_blank import is_blank


class RegisterAdmin(QtWidgets.QDialog):

    def __init__(self, View):
        super().__init__()
        self.View = View
        self.setupUi(self)

        QtWidgets.QApplication.instance().focusChanged.connect(self.on_focus_change)
        self.ActiveOverlay = ActiveOverlay(self)
        self.dots = [self.dot_1, self.dot_2, self.dot_3, self.dot_4]
        self.validations = ["Password requirements:\n",
                            "        🗴  Password must be at least 8 characters in length.\n",
                            "        🗸  Password must be no more than 128 characters in length.\n",
                            "        🗴  Password must contain at least 1 english uppercase,\n",
                            "             english lowercase, numbers (0-9), and non-alphanumeric\n",
                            "             characters (!, $, %, etc.)."]
        self.is_password_valid = False
        self.is_cancelled = True
        self.question_and_answer = {}

    def run(self):
        self.activateWindow()
        self.exec_()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(510, 462)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        Form.setStyleSheet("QWidget{\n"
                           "    background: #102542; color: white\n"
                           "}\n"
                           "\n"
                           "QLineEdit {\n"
                           "     padding: 1px 5px;\n"
                           "     border: 1px solid #0e4884;\n"
                           "     border-radius: 5px;\n"
                           "}\n"
                           "\n"
                           "QComboBox {\n"
                           "     padding: 1px 7px;\n"
                           "     border: 1px solid #0e4884;\n"
                           "     border-radius: 5px;\n"
                           "}\n"
                           "\n"
                           "QPushButton {\n"
                           "    padding: 5px;\n"
                           "    border: 1px solid #0d3c6e;\n"
                           "    border-radius: 5px;\n"
                           "    background-color: #0d3c6e;\n"
                           "    letter-spacing: 1px\n"
                           "}\n"
                           "\n"
                           "QPushButton#btn_cancel:pressed,\n"
                           "QPushButton:pressed {\n"
                           "    background-color: #083654;\n"
                           "}\n"
                           "\n"
                           "QPushButton#btn_cancel {\n"
                           "      background-color: none;\n"
                           "}\n"
                           "\n"
                           "QLineEdit:focus,\n"
                           "QLineEdit:hover,\n"
                           "QPushButton:focus,\n"
                           "QPushButton:hover,\n"
                           "QComboBox:focus,\n"
                           "QComboBox:hover {\n"
                           "      border: 1px solid #256eff;\n"
                           "      outline: none;\n"
                           "}\n"
                           "\n"
                           "QPushButton#btn_reveal_repeat_password,\n"
                           "QPushButton#btn_reveal_password{\n"
                           "    border-radius: 0px;\n"
                           "    border-top-right-radius: 5px;\n"
                           "    border-bottom-right-radius: 5px;\n"
                           "}\n"
                           "\n"
                           "QLineEdit#txt_repeat_password,\n"
                           "QLineEdit#txt_password{\n"
                           "    border-radius: 0px;\n"
                           "    border-top-left-radius: 5px;\n"
                           "    border-bottom-left-radius: 5px;\n"
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
                           "}\n"
                           "\n"
                           "QComboBox QAbstractItemView::disabled {\n"
                           "    color: #6b6b6b;\n"
                           "}\n"
                           "\n"
                           "QScrollBar {\n"
                           "  background: blue;\n"
                           "  width: 8px;\n"
                           "}\n"
                           "\n"
                           "QScrollBar::handle {\n"
                           "  background-color: rgb(68, 68, 68);\n"
                           "}\n"
                           "\n"
                           "QScrollBar:vertical {\n"
                           "  width: 9px;\n"
                           "  margin: 0;\n"
                           "  border-radius: 5px;\n"
                           "}\n"
                           "\n"
                           "QScrollBar::handle:vertical {\n"
                           "  background-color: #97b9f4;\n"
                           "  width: 18px;\n"
                           "\n"
                           "}\n"
                           "\n"
                           "QScrollBar::sub-line:vertical {\n"
                           "  height: 0;\n"
                           "  width: 0;\n"
                           "}\n"
                           "\n"
                           "QScrollBar::add-line:vertical {\n"
                           "  height: 0;\n"
                           "  width: 0;\n"
                           "}\n"
                           "\n"
                           "QScrollBar::add-page:vertical {\n"
                           "  background: #0B1A30;\n"
                           "  margin-top: -3px;\n"
                           "}\n"
                           "\n"
                           "QScrollBar::sub-page:vertical {\n"
                           "  background: #0B1A30;\n"
                           "  margin-bottom: -3px;\n"
                           "}\n"
                           "\n"
                           "")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.title_bar = TitleBar(self, True)
        self.title_bar.setMinimumSize(QtCore.QSize(0, 30))
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.title_bar.setStyleSheet("background: #102542")
        self.title_bar.setObjectName("title_bar")
        self.verticalLayout_6.addWidget(self.title_bar)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dot_1 = QtWidgets.QLabel(self.widget)
        self.dot_1.setText("")
        self.dot_1.setPixmap(QtGui.QPixmap(relative_path(
            'SignIn', ['Misc', 'Resources'], 'dot2.png')))
        self.dot_1.setAlignment(QtCore.Qt.AlignCenter)
        self.dot_1.setObjectName("dot_1")
        self.horizontalLayout.addWidget(self.dot_1)
        self.dot_2 = QtWidgets.QLabel(self.widget)
        self.dot_2.setText("")
        self.dot_2.setPixmap(QtGui.QPixmap(relative_path(
            'SignIn', ['Misc', 'Resources'], 'dot1.png')))
        self.dot_2.setAlignment(QtCore.Qt.AlignCenter)
        self.dot_2.setObjectName("dot_2")
        self.horizontalLayout.addWidget(self.dot_2)
        self.dot_3 = QtWidgets.QLabel(self.widget)
        self.dot_3.setText("")
        self.dot_3.setPixmap(QtGui.QPixmap(relative_path(
            'SignIn', ['Misc', 'Resources'], 'dot1.png')))
        self.dot_3.setAlignment(QtCore.Qt.AlignCenter)
        self.dot_3.setObjectName("dot_3")
        self.horizontalLayout.addWidget(self.dot_3)
        self.dot_4 = QtWidgets.QLabel(self.widget)
        self.dot_4.setText("")
        self.dot_4.setPixmap(QtGui.QPixmap(relative_path(
            'SignIn', ['Misc', 'Resources'], 'dot1.png')))
        self.dot_4.setAlignment(QtCore.Qt.AlignCenter)
        self.dot_4.setObjectName("dot_4")
        self.horizontalLayout.addWidget(self.dot_4)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout.setContentsMargins(26, 0, 25, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.gridLayout_1.setVerticalSpacing(15)
        self.gridLayout_1.setObjectName("gridLayout_1")
        self.lbl_repeat_password_validation = QtWidgets.QLabel(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_repeat_password_validation.sizePolicy().hasHeightForWidth())
        self.lbl_repeat_password_validation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_repeat_password_validation.setFont(font)
        self.lbl_repeat_password_validation.setStyleSheet("color: #bd2000")
        self.lbl_repeat_password_validation.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_repeat_password_validation.setIndent(1)
        self.lbl_repeat_password_validation.setObjectName(
            "lbl_repeat_password_validation")
        self.gridLayout_1.addWidget(
            self.lbl_repeat_password_validation, 5, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.txt_repeat_password = QtWidgets.QLineEdit(self.page_1)
        self.txt_repeat_password.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_repeat_password.setFont(font)
        self.txt_repeat_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_repeat_password.setObjectName("txt_repeat_password")
        self.horizontalLayout_4.addWidget(self.txt_repeat_password)
        self.btn_reveal_repeat_password = QtWidgets.QPushButton(self.page_1)
        self.btn_reveal_repeat_password.setMinimumSize(QtCore.QSize(35, 30))
        self.btn_reveal_repeat_password.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_reveal_repeat_password.setFont(font)
        self.btn_reveal_repeat_password.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_reveal_repeat_password.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(relative_path('SignIn', ['Misc', 'Resources'], 'show.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_reveal_repeat_password.setIcon(icon)
        self.btn_reveal_repeat_password.setIconSize(QtCore.QSize(20, 20))
        self.btn_reveal_repeat_password.setObjectName(
            "btn_reveal_repeat_password")
        self.horizontalLayout_4.addWidget(self.btn_reveal_repeat_password)
        self.gridLayout_1.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setIndent(1)
        self.label_8.setObjectName("label_8")
        self.gridLayout_1.addWidget(self.label_8, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txt_password = AdminPassword(self)
        self.txt_password.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_password.setFont(font)
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_password.setObjectName("txt_password")
        self.horizontalLayout_3.addWidget(self.txt_password)
        self.btn_reveal_password = QtWidgets.QPushButton(self.page_1)
        self.btn_reveal_password.setMinimumSize(QtCore.QSize(35, 30))
        self.btn_reveal_password.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_reveal_password.setFont(font)
        self.btn_reveal_password.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_reveal_password.setText("")
        self.btn_reveal_password.setIcon(icon)
        self.btn_reveal_password.setIconSize(QtCore.QSize(20, 20))
        self.btn_reveal_password.setObjectName("btn_reveal_password")
        self.horizontalLayout_3.addWidget(self.btn_reveal_password)
        self.gridLayout_1.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setIndent(1)
        self.label_9.setObjectName("label_9")
        self.gridLayout_1.addWidget(self.label_9, 3, 0, 1, 1)
        self.lbl_password_validation = QtWidgets.QLabel(self.page_1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_password_validation.sizePolicy().hasHeightForWidth())
        self.lbl_password_validation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_password_validation.setFont(font)
        self.lbl_password_validation.setStyleSheet("color: #bd2000")
        self.lbl_password_validation.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_password_validation.setIndent(1)
        self.lbl_password_validation.setObjectName("lbl_password_validation")
        self.gridLayout_1.addWidget(self.lbl_password_validation, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_1)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_2.setContentsMargins(25, 0, 25, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setVerticalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_11 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setIndent(1)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 2, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setIndent(1)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 0, 0, 1, 1)
        self.txt_question_answer_2 = QtWidgets.QLineEdit(self.page_2)
        self.txt_question_answer_2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_question_answer_2.setFont(font)
        self.txt_question_answer_2.setObjectName("txt_question_answer_2")
        self.gridLayout_2.addWidget(self.txt_question_answer_2, 3, 0, 1, 1)
        self.cmb_question_2 = QtWidgets.QComboBox(self.page_2)
        self.cmb_question_2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.cmb_question_2.setFont(font)
        self.cmb_question_2.view().setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_question_2.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_question_2.setMaxVisibleItems(4)
        self.cmb_question_2.setSizeAdjustPolicy(
            QtWidgets.QComboBox.AdjustToContents)
        self.cmb_question_2.setObjectName("cmb_question_2")
        self.cmb_question_2.addItem("")
        self.cmb_question_2.addItem("")
        self.cmb_question_2.addItem("")
        self.cmb_question_2.addItem("")
        self.cmb_question_2.addItem("")
        self.cmb_question_2.addItem("")
        self.cmb_question_2.addItem("")
        self.gridLayout_2.addWidget(self.cmb_question_2, 1, 0, 1, 1)
        self.lbl_answer_validation_2 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_answer_validation_2.sizePolicy().hasHeightForWidth())
        self.lbl_answer_validation_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_answer_validation_2.setFont(font)
        self.lbl_answer_validation_2.setStyleSheet("color: #bd2000")
        self.lbl_answer_validation_2.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_answer_validation_2.setIndent(1)
        self.lbl_answer_validation_2.setObjectName("lbl_answer_validation_2")
        self.gridLayout_2.addWidget(self.lbl_answer_validation_2, 4, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_3.setContentsMargins(25, 0, 25, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setVerticalSpacing(15)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_15 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setIndent(1)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 2, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setIndent(1)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 0, 0, 1, 1)
        self.txt_question_answer_3 = QtWidgets.QLineEdit(self.page_3)
        self.txt_question_answer_3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_question_answer_3.setFont(font)
        self.txt_question_answer_3.setObjectName("txt_question_answer_3")
        self.gridLayout_3.addWidget(self.txt_question_answer_3, 3, 0, 1, 1)
        self.cmb_question_3 = QtWidgets.QComboBox(self.page_3)
        self.cmb_question_3.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.cmb_question_3.setFont(font)
        self.cmb_question_3.view().setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_question_3.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_question_3.setMaxVisibleItems(4)
        self.cmb_question_3.setSizeAdjustPolicy(
            QtWidgets.QComboBox.AdjustToContents)
        self.cmb_question_3.setObjectName("cmb_question_3")
        self.cmb_question_3.addItem("")
        self.cmb_question_3.addItem("")
        self.cmb_question_3.addItem("")
        self.cmb_question_3.addItem("")
        self.cmb_question_3.addItem("")
        self.cmb_question_3.addItem("")
        self.cmb_question_3.addItem("")
        self.gridLayout_3.addWidget(self.cmb_question_3, 1, 0, 1, 1)
        self.lbl_answer_validation_3 = QtWidgets.QLabel(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_answer_validation_3.sizePolicy().hasHeightForWidth())
        self.lbl_answer_validation_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_answer_validation_3.setFont(font)
        self.lbl_answer_validation_3.setStyleSheet("color: #bd2000")
        self.lbl_answer_validation_3.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_answer_validation_3.setIndent(1)
        self.lbl_answer_validation_3.setObjectName("lbl_answer_validation_3")
        self.gridLayout_3.addWidget(self.lbl_answer_validation_3, 4, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_4.setContentsMargins(25, 0, 25, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setVerticalSpacing(15)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.cmb_question_4 = QtWidgets.QComboBox(self.page_4)
        self.cmb_question_4.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.cmb_question_4.setFont(font)
        self.cmb_question_4.view().setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_question_4.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_question_4.setMaxVisibleItems(4)
        self.cmb_question_4.setSizeAdjustPolicy(
            QtWidgets.QComboBox.AdjustToContents)
        self.cmb_question_4.setObjectName("cmb_question_4")
        self.cmb_question_4.addItem("")
        self.cmb_question_4.addItem("")
        self.cmb_question_4.addItem("")
        self.cmb_question_4.addItem("")
        self.cmb_question_4.addItem("")
        self.cmb_question_4.addItem("")
        self.cmb_question_4.addItem("")
        self.gridLayout_4.addWidget(self.cmb_question_4, 1, 0, 1, 1)
        self.txt_question_answer_4 = QtWidgets.QLineEdit(self.page_4)
        self.txt_question_answer_4.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.txt_question_answer_4.setFont(font)
        self.txt_question_answer_4.setObjectName("txt_question_answer_4")
        self.gridLayout_4.addWidget(self.txt_question_answer_4, 3, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setIndent(1)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 0, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setIndent(1)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)
        self.lbl_answer_validation_4 = QtWidgets.QLabel(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_answer_validation_4.sizePolicy().hasHeightForWidth())
        self.lbl_answer_validation_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_answer_validation_4.setFont(font)
        self.lbl_answer_validation_4.setStyleSheet("color: #bd2000")
        self.lbl_answer_validation_4.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_answer_validation_4.setIndent(1)
        self.lbl_answer_validation_4.setObjectName("lbl_answer_validation_4")
        self.gridLayout_4.addWidget(self.lbl_answer_validation_4, 4, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_4)
        self.stackedWidget.addWidget(self.page_4)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(25, 25, 25, 25)
        self.horizontalLayout_2.setSpacing(25)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setStyleSheet("padding: 5px;")
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_2.addWidget(self.btn_cancel)
        self.btn_next = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_next.setFont(font)
        self.btn_next.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_next.setStyleSheet("padding: 5px;")
        self.btn_next.setObjectName("btn_next")
        self.horizontalLayout_2.addWidget(self.btn_next)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6.addWidget(self.widget)

        self.retranslateUi(Form)
        self.hide_validations()
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_repeat_password_validation.setText(
            _translate("Form", "Passwords does not match"))
        self.label_8.setText(_translate("Form", "Password"))
        self.label_9.setText(_translate("Form", "Repeat Password"))
        self.lbl_password_validation.setText(_translate("Form", "Password requirements:\n"
                                                        "        🗴  Password must be at least 8 characters in length.\n"
                                                        "        🗸  Password must be no more than 128 characters in length.\n"
                                                        "        🗴  Password must contain at least 1 english uppercase,\n"
                                                        "             english lowercase, numbers (0-9), and non-alphanumeric\n"
                                                        "             characters (!, $, %, etc.)."))
        self.label_11.setText(_translate("Form", "Answer"))
        self.label_10.setText(_translate("Form", "Question"))
        self.cmb_question_2.setItemText(0, _translate(
            "Form", "What was your childhood nickname?"))
        self.cmb_question_2.setItemText(1, _translate(
            "Form", "What is the model of your first car?"))
        self.cmb_question_2.setItemText(2, _translate(
            "Form", "When is your wedding anniversary?"))
        self.cmb_question_2.setItemText(3, _translate(
            "Form", "What is the name of your favorite snack?"))
        self.cmb_question_2.setItemText(4, _translate(
            "Form", "What was the name of your first stuffed animal?"))
        self.cmb_question_2.setItemText(5, _translate(
            "Form", "Where were you when you had your first kiss?"))
        self.cmb_question_2.setItemText(6, _translate(
            "Form", "What is the name of your first pet?"))
        self.lbl_answer_validation_2.setText(
            _translate("Form", "Answer must be filled"))
        self.label_15.setText(_translate("Form", "Answer"))
        self.label_14.setText(_translate("Form", "Question"))
        self.cmb_question_3.setItemText(0, _translate(
            "Form", "What was your childhood nickname?"))
        self.cmb_question_3.setItemText(1, _translate(
            "Form", "What is the model of your first car?"))
        self.cmb_question_3.setItemText(2, _translate(
            "Form", "When is your wedding anniversary?"))
        self.cmb_question_3.setItemText(3, _translate(
            "Form", "What is the name of your favorite snack?"))
        self.cmb_question_3.setItemText(4, _translate(
            "Form", "What was the name of your first stuffed animal?"))
        self.cmb_question_3.setItemText(5, _translate(
            "Form", "Where were you when you had your first kiss?"))
        self.cmb_question_3.setItemText(6, _translate(
            "Form", "What is the name of your first pet?"))
        self.lbl_answer_validation_3.setText(
            _translate("Form", "Answer must be filled"))
        self.cmb_question_4.setItemText(0, _translate(
            "Form", "What was your childhood nickname?"))
        self.cmb_question_4.setItemText(1, _translate(
            "Form", "What is the model of your first car?"))
        self.cmb_question_4.setItemText(2, _translate(
            "Form", "When is your wedding anniversary?"))
        self.cmb_question_4.setItemText(3, _translate(
            "Form", "What is the name of your favorite snack?"))
        self.cmb_question_4.setItemText(4, _translate(
            "Form", "What was the name of your first stuffed animal?"))
        self.cmb_question_4.setItemText(5, _translate(
            "Form", "Where were you when you had your first kiss?"))
        self.cmb_question_4.setItemText(6, _translate(
            "Form", "What is the name of your first pet?"))
        self.label_12.setText(_translate("Form", "Question"))
        self.label_13.setText(_translate("Form", "Answer"))
        self.lbl_answer_validation_4.setText(
            _translate("Form", "Answer must be filled"))
        self.btn_cancel.setText(_translate("Form", "Cancel"))
        self.btn_next.setText(_translate("Form", "Next"))

    def keyPressEvent(self, event):
        if event.key() == 16777220:
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        if self.is_cancelled:
            self.View.SignIn.stop_loading_screen()
        super().closeEvent(event)

    def showEvent(self, event):
        self.show_password_validations()
        super().showEvent(event)

    def on_focus_change(self):
        if self.isActiveWindow():
            self.ActiveOverlay.show()
        else:
            self.ActiveOverlay.hide()

    def reveal_password(self):
        icon = QtGui.QIcon()
        if self.txt_password.echoMode() == QtWidgets.QLineEdit.Password:
            self.txt_password.setEchoMode(QtWidgets.QLineEdit.Normal)
            icon.addPixmap(QtGui.QPixmap(relative_path('SignIn', ['Misc', 'Resources'], 'hide.png')),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            self.txt_password.setEchoMode(QtWidgets.QLineEdit.Password)
            icon.addPixmap(QtGui.QPixmap(relative_path('SignIn', ['Misc', 'Resources'], 'show.png')),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_reveal_password.setIcon(icon)

    def reveal_repeat_password(self):
        icon = QtGui.QIcon()
        if self.txt_repeat_password.echoMode() == QtWidgets.QLineEdit.Password:
            self.txt_repeat_password.setEchoMode(QtWidgets.QLineEdit.Normal)
            icon.addPixmap(QtGui.QPixmap(relative_path('SignIn', ['Misc', 'Resources'], 'hide.png')),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            self.txt_repeat_password.setEchoMode(QtWidgets.QLineEdit.Password)
            icon.addPixmap(QtGui.QPixmap(relative_path('SignIn', ['Misc', 'Resources'], 'show.png')),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_reveal_repeat_password.setIcon(icon)

    def show_password_validations(self):
        if self.lbl_password_validation.isHidden():
            self.setFixedSize(510, self.height()+147)
        self.lbl_password_validation.show()

    def show_validation(self, label):
        if label.isHidden():
            self.setFixedSize(510, self.height()+37)
        label.show()

    def decrement_page(self):
        current_index = self.stackedWidget.currentIndex()

        if current_index == 0:
            self.close()
            return
            
        if current_index == 1:
            self.btn_cancel.setText('Cancel')

        if current_index == 3:
            self.btn_next.setText('Next')

        self.stackedWidget.setCurrentIndex(current_index-1)
        self.redo_cmb(current_index-1)
        self.dots[current_index].setPixmap(QtGui.QPixmap(relative_path(
            "SignIn", ["Misc", "Resources"], "dot1.png")))
        self.hide_validations()

    def store_qna(self, index):
        if index < 2:
            return True

        page = self.stackedWidget.findChild(QtWidgets.QWidget, f"page_{index}")

        target_cmb = page.findChild(
            QtWidgets.QComboBox, f"cmb_question_{index}")
        target_txt = page.findChild(
            QtWidgets.QLineEdit, f"txt_question_answer_{index}")
        question = target_cmb.currentText()
        answer = target_txt.text()

        if is_blank(answer):
            target_lbl = page.findChild(
                QtWidgets.QLabel, f"lbl_answer_validation_{index}")
            self.show_validation(target_lbl)
            return False

        self.question_and_answer[question] = answer
        self.update_future_cmb(index + 1)

        return True

    def update_future_cmb(self, index):
        try:
            answered_questions = list(self.question_and_answer.keys())
            page = self.stackedWidget.findChild(
                QtWidgets.QWidget, f"page_{index}")
            target_cmb = page.findChild(
                QtWidgets.QComboBox, f"cmb_question_{index}")

            for answered_question in answered_questions:
                question_index = target_cmb.findText(answered_question)
                target_cmb.model().item(question_index).setEnabled(False)

            for i in range(target_cmb.count()):
                if target_cmb.model().item(i).isEnabled():
                    target_cmb.setCurrentIndex(i)
                    break
        except AttributeError:
            return

    def redo_cmb(self, index):
        try:
            page = self.stackedWidget.findChild(
                QtWidgets.QWidget, f"page_{index}")
            target_cmb = page.findChild(
                QtWidgets.QComboBox, f"cmb_question_{index}")
            latest_answered_question = list(
                self.question_and_answer.keys())[-1]

            index = target_cmb.findText(latest_answered_question)
            target_cmb.model().item(index).setEnabled(True)
            del self.question_and_answer[latest_answered_question]
        except AttributeError:
            return

    def at_least_8_characters(self):
        self.validations[1] = "        🗸  Password must be at least 8 characters in length.\n"
        self.is_password_valid = True

    def less_than_128_characters(self):
        self.validations[2] = "        🗸  Password must be no more than 128 characters in length.\n"
        self.is_password_valid = True

    def has_1_upper_lower_special(self):
        self.validations[3] = "        🗸  Password must contain at least 1 english uppercase,\n"
        self.is_password_valid = True

    def less_than_8_characters(self):
        self.validations[1] = "        🗴  Password must be at least 8 characters in length.\n"
        self.is_password_valid = False

    def more_than_128_characters(self):
        self.validations[2] = "        🗴  Password must be no more than 128 characters in length.\n"
        self.is_password_valid = False

    def no_1_upper_lower_special(self):
        self.validations[3] = "        🗴  Password must contain at least 1 english uppercase,\n"
        self.is_password_valid = False

    def update_validations(self):
        self.lbl_password_validation.setText("".join(self.validations))

    def hide_validations(self):
        self.lbl_password_validation.hide()
        self.lbl_repeat_password_validation.hide()
        self.lbl_answer_validation_2.hide()
        self.lbl_answer_validation_3.hide()
        self.lbl_answer_validation_4.hide()
        self.setFixedSize(510, 315)
