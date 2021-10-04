from PyQt5 import QtCore, QtGui, QtWidgets
from Teachers.Misc.Widgets.context_menu import ContextMenu


class StudentItem(QtWidgets.QWidget):
    operation = QtCore.pyqtSignal(str)

    def __init__(self, parent, name):
        super().__init__(parent=parent)
        self.name = name
        self.setupUi(self)
        self.ContextMenu = ContextMenu(self)
        self.ContextMenu.showEvent = self.show_context_menu
        self.lbl_student_name.setText(self.name)
        self.mouse_pos = QtCore.QPoint(0, 0)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(430, 280)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_student_name = QtWidgets.QLabel(Form)
        self.lbl_student_name.setText("")
        self.lbl_student_name.setIndent(1)
        font = QtGui.QFont()
        font.setFamily("Barlow")
        font.setPointSize(10)
        self.lbl_student_name.setFont(font)
        self.lbl_student_name.setObjectName("lbl_student_name")
        self.verticalLayout.addWidget(self.lbl_student_name)
        self.lbl_student_screen = QtWidgets.QLabel(Form)
        self.lbl_student_screen.setText("")
        self.lbl_student_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_student_screen.setObjectName("lbl_student_screen")
        self.verticalLayout.addWidget(self.lbl_student_screen)
        self.verticalLayout.setStretch(1, 1)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            self.mouse_pos = self.mapToGlobal(event.pos())
            self.ContextMenu.show()
            self.operation.emit(self.name)
        super().mousePressEvent(event)

    def show_context_menu(self, event):
        self.ContextMenu.setFocus(True)
        self.ContextMenu.move(self.mouse_pos)