from PyQt5 import QtCore
from Teachers.Controller.Chat.host import Host as ChatHost
from Teachers.Controller.Stream.host import Host as StreamHost
import threading

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


class Meeting:

    is_frozen = False
    is_connected = True
    is_disconnected = False

    def __init__(self, Controller, Class):
        self.Model = Controller.Model.Meeting
        self.View = Controller.View.Meeting
        self.Controller = Controller
        self.Class = Class

        self.StreamHost = StreamHost(self, self.Class, self.Model, self.View, self.Controller)
        self.ChatHost = ChatHost(self, self.Class, self.Model, self.View, self.Controller)
        self.connect_signals()
        self.View.run()

    def connect_signals(self):
        for screen in self.View.screens:
            screen.operation.connect(self.change_left_page)

        for interactor in self.View.interactors:
            interactor.operation.connect(self.change_right_page)

        for close_button in self.View.close_buttons:
            close_button.clicked.connect(self.View.close_right)

        self.View.btn_leave.clicked.connect(self.list_all_threads)

    def change_left_page(self, index):
        for screen in self.View.screens:
            if screen.is_active:
                screen.deactivate()
                break

        self.View.screens[index].activate()
        self.View.sw_left.setCurrentIndex(index)

    def change_right_page(self, index):
        if self.View.sw_right.isHidden():
            self.View.sw_right.show()

        for interactor in self.View.interactors:
            if interactor.is_active:
                interactor.deactivate()
                break

        self.View.interactors[index].activate()
        self.View.sw_right.setCurrentIndex(index)

    def list_all_threads(self):
        for i in threading.enumerate():
            print(i)