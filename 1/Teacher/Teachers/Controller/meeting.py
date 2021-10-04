import os
import socket
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
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

    def __init__(self, Controller, Class):
        self.Model = Controller.Model.Meeting
        self.View = Controller.View.Meeting
        self.Controller = Controller
        self.Class = Class
        self.is_frozen = False
        self.is_connected = True
        self.is_disconnected = False

        student_model = self.Model.ListModel(self.View.lv_student, [])
        self.View.lv_student.setModel(student_model)

        self.View.title_bar.title.setText(self.Class.Name)

        self.connect_signals()
        self.View.run()

        self.StreamHost = StreamHost(self, self.Class, self.Model, self.View, self.Controller)
        self.ChatHost = ChatHost(self, self.Class, self.Model, self.View, self.Controller)

    def connect_signals(self):
        for screen in self.View.screens:
            screen.operation.connect(self.change_left_page)

        for interactor in self.View.interactors:
            interactor.operation.connect(self.change_right_page)

        for close_button in self.View.close_buttons:
            close_button.clicked.connect(self.View.close_right)

        self.View.hideEvent = self.parent_hid

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

        if index == 1:
            self.View.BadgeOverlay.hide()

        self.View.interactors[index].activate()
        self.View.sw_right.setCurrentIndex(index)

    def parent_hid(self, event):
        self.View.sw_right.hide()
        for interactor in self.View.interactors:
            if interactor.is_active:
                interactor.deactivate()
                break