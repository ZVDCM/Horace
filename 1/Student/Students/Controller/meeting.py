import os
from PyQt5 import QtCore
from Students.Controller.Chat.client import Client as ChatClient
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

    def __init__(self, Controller, Class, ClassTeacher):
        self.Model = Controller.Model.Meeting
        self.View = Controller.View.Meeting
        self.Controller = Controller
        self.Class = Class
        self.ClassTeacher = ClassTeacher
        self.is_frozen = False
        self.is_connected = True
        self.is_disconnected = False

        self.View.title_bar.title.setText(self.Class.Name)

        self.ChatClient = ChatClient(self, self.Class, self.ClassTeacher, self.Model, self.View, self.Controller)
        self.connect_signals()
        self.View.run()

    def connect_signals(self):
        for interactor in self.View.interactors:
            interactor.operation.connect(self.change_right_page)

        for close_button in self.View.close_buttons:
            close_button.clicked.connect(self.View.close_right)
        
    def change_right_page(self, index):
        if self.View.sw_right.isHidden():
            self.View.sw_right.show()

        for interactor in self.View.interactors:
            if interactor.is_active:
                interactor.deactivate()
                break

        if index == 1:
            self.View.BadgeOverlay.hide()

        self.View.interactors[index].activate()
        self.View.sw_right.setCurrentIndex(index)
