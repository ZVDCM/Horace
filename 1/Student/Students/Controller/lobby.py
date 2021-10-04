from PyQt5.QtWidgets import QMainWindow
from Students.Misc.Widgets.change_password import ChangePassword
from PyQt5 import QtCore
from win32api import GetSystemMetrics


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

class SetLobbyStatus(QtCore.QThread):

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        self.fn(self.val)
        self.quit()

class Lobby:

    def __init__(self, Controller):
        self.Model = Controller.Model.Lobby
        self.View = Controller.View.Lobby
        self.Controller = Controller

        self.TargetClass = None

        self.connect_signals()
        self.get_classes()

        self.View.title_bar.title.setText('Lobby')

        self.View.run()

    def connect_signals(self):
        self.get_all_class = Get(self.Model.get_all_class)
        self.get_all_class.started.connect(self.View.ClassLoadingScreen.run)
        self.get_all_class.operation.connect(self.set_classes)
        self.get_all_class.finished.connect(self.View.ClassLoadingScreen.hide)

        self.View.btn_more.clicked.connect(self.more_clicked)
        self.View.ContextMenu.password.connect(self.change_password)
        self.View.ContextMenu.sign_out.connect(self.View.close)

        self.View.closeEvent = self.lobby_closed
    
    def GetClassSectionAddress(self):
        return Get(self.Model.get_class_section_address)

    def get_classes(self):
        self.get_all_class.val = self.Controller.User,
        self.get_all_class.finished.connect(self.set_classes_operation)
        self.get_all_class.start()
    
    def set_classes_operation(self):
        for index in range(self.View.flow_layout.count()):
            target_class_item = self.View.flow_layout.itemAt(index).widget()
            target_class_item.operation.connect(self.class_item_clicked)
        self.set_lobby_status_handler('Classes loaded successfully')

    def set_classes(self, classes):
        for _class in classes:
            self.View.add_class_item(_class)

    def class_item_clicked(self, Class):
        self.TargetClass = Class
        self.get_class_section_address_handler = self.GetClassSectionAddress()
        self.get_class_section_address_handler.val = Class, self.Controller.User
        self.get_class_section_address_handler.operation.connect(self.init_meeting)
        self.get_class_section_address_handler.start()

    def init_meeting(self, ClassTeacher):
        self.Controller.Model.init_meeting()
        self.Controller.View.init_meeting()
        self.Controller.init_meeting(self.TargetClass, ClassTeacher)

        self.disable_classes()

    def disable_classes(self):
        if self.View.flow_layout.count():
            for i in range(self.View.flow_layout.count()):
                self.View.flow_layout.itemAt(i).widget().disable()

    def enable_classes(self):
        try:
            if self.View.flow_layout.count():
                for i in range(self.View.flow_layout.count()):
                    self.View.flow_layout.itemAt(i).widget().activate()
        except AttributeError:
            return

    def more_clicked(self):
        pos = self.View.btn_more.mapToGlobal(self.View.btn_more.rect().bottomRight())
        height = GetSystemMetrics(1)
        if pos.y() > height - self.View.ContextMenu.height():
            pos_up = self.View.btn_more.mapToGlobal(self.View.btn_more.rect().topRight())
            self.View.ContextMenu.move(pos_up.x()-self.View.ContextMenu.width(), pos_up.y()-self.View.ContextMenu.height()-5)
        else:
            self.View.ContextMenu.move(pos.x()-self.View.ContextMenu.width(), pos.y()+5)
        self.View.ContextMenu.show()

    def change_password(self):
        self.ChangePassword = ChangePassword(self, self.View, self.Controller.User, self.Model)
        self.ChangePassword.run()

    def set_lobby_status_handler(self, status):
        self.handler = SetLobbyStatus(self.View.set_lobby_status)
        self.handler.val = status
        self.handler.start()
        self.timer = QtCore.QTimer.singleShot(5000, self.View.lbl_lobby_status.clear)
    
    def lobby_closed(self, event):
        try:
            if self.Controller.View.Meeting.isVisible():
                return
        except (AttributeError, RuntimeError):
            pass
        
        try:
            if self.View.isVisible():
                self.View.close()
        except RuntimeError:
            pass

        self.Controller.SignInController.View.init_sign_in()
        self.Controller.SignInController.Model.init_sign_in()
        self.Controller.SignInController.init_sign_in()
        super(QMainWindow, self.View).closeEvent(event)