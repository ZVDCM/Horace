from Teachers.Misc.Widgets.change_password import ChangePassword
import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QMainWindow, QPushButton, QWidget
import socket

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

class Alert(QtCore.QThread):
    operation = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.val = ()

    def run(self):
        self.operation.emit(*self.val)
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

        self.target_attendance = None
        self.target_attendance_data = None

        self.connect_signals()
        self.get_classes()
        self.get_attendances()

        self.View.run()

    def connect_signals(self):
        for side_nav in self.View.side_navs:
            side_nav.operation.connect(self.change_page)
        self.View.resizeEvent = self.resize

        self.View.lv_attendance.clicked.connect(self.attendance_list_clicked)
        self.View.btn_download.clicked.connect(self.download_attendance)

        self.View.txt_search_attendance.returnPressed.connect(self.search_attendance)
        self.View.btn_search_attendance.clicked.connect(self.search_attendance)
        self.View.lv_attendance.hideEvent = self.reset_list_target

        self.View.btn_more.clicked.connect(self.more_clicked)
        self.View.ContextMenu.password.connect(self.change_password)
        self.View.ContextMenu.sign_out.connect(self.sign_out)

        self.View.closeEvent = self.lobby_closed

    def GetAllClass(self):
        handler = Get(self.Model.get_all_class)
        handler.started.connect(self.View.ClassLoadingScreen.show)
        handler.operation.connect(self.set_classes)
        handler.finished.connect(self.View.ClassLoadingScreen.hide)
        return handler

    def SetClassTeacherAddress(self):
        return Operation(self.Model.set_class_teacher_address)
        
    def GetAllAttendances(self):
        handler = Get(self.Model.get_all_attendances)
        handler.started.connect(self.View.AttendanceListLoadingScreen.show)
        handler.operation.connect(self.set_attendances)
        handler.finished.connect(self.View.AttendanceListLoadingScreen.hide)
        return handler

    def GetAttendanceData(self):
        handler = Get(self.Model.get_attendance_data)
        handler.started.connect(self.View.AttendanceTableLoadingScreen.show)
        handler.operation.connect(self.set_attendance_data)
        handler.finished.connect(self.View.AttendanceTableLoadingScreen.hide)
        return handler

    def get_classes(self):
        self.get_all_class_handler = self.GetAllClass()
        self.get_all_class_handler.val = self.Controller.User,
        self.get_all_class_handler.finished.connect(self.set_classes_operation)
        self.get_all_class_handler.finished.connect(lambda: self.set_lobby_status_handler(f'Classes loaded successfully'))
        self.get_all_class_handler.start()

    def set_classes_operation(self):
        for index in range(self.View.flow_layout.count()):
            target_class_item = self.View.flow_layout.itemAt(index).widget()
            target_class_item.operation.connect(self.class_item_clicked)

    def set_classes(self, classes):
        for _class in classes:
            self.View.add_class_item(_class)

    def class_item_clicked(self, Class):
        address = self.get_local_ip()
        Class.HostAddress = address
        self.set_class_teacher_address_handler = self.SetClassTeacherAddress()
        self.set_class_teacher_address_handler.val = address, Class, self.Controller.User
        self.set_class_teacher_address_handler.operation.connect(lambda: self.init_meeting(Class))
        self.set_class_teacher_address_handler.start()

    @staticmethod
    def get_local_ip():
        return socket.gethostbyname(socket.gethostname())

    def change_page(self, index):
        for side_nav in self.View.side_navs:
            if side_nav.is_active:
                side_nav.deactivate()
                break
        self.View.side_navs[index].activate()
        self.View.sw_all.setCurrentIndex(index)

    def resize(self, event):
        self.View.ClassLoadingScreen.resize_loader()
        self.View.AttendanceTableLoadingScreen.resize_loader()
        self.View.AttendanceListLoadingScreen.resize_loader()
        try:
            self.View.tv_attendance.model().layoutChanged.emit()
            self.View.lv_attendance.model().layoutChanged.emit()
        except AttributeError:
            pass
        self.View.ActiveOverlay.resized.emit()
        super(QMainWindow, self.View).resizeEvent(event)

    def init_meeting(self, Class):
        self.Controller.Model.init_meeting()
        self.Controller.View.init_meeting()
        self.Controller.init_meeting(Class)

    def get_attendances(self):
        self.get_all_attendances_handler = self.GetAllAttendances()
        self.get_all_attendances_handler.val = self.Controller.User,
        self.get_all_attendances_handler.finished.connect(lambda: self.set_lobby_status_handler(f'Attendances loaded successfully'))
        self.get_all_attendances_handler.start()

    def set_attendances(self, attendances):
        if attendances:
            attendance_model = self.Model.ListModel(self.View.lv_attendance, attendances)
            self.View.lv_attendance.setModel(attendance_model)
            index = attendance_model.createIndex(0,0)
            self.View.lv_attendance.setCurrentIndex(index)
            self.View.lv_attendance.model().layoutChanged.emit()

            self.target_attendance = attendances[0]
            self.get_attendance_data(self.target_attendance)

    def attendance_list_clicked(self, index):
        row = index.row()
        attendance_model = self.View.lv_attendance.model()
        self.target_attendance = attendance_model.getRowData(row)
        self.get_attendance_data(self.target_attendance)

    def get_attendance_data(self, attendance):
        self.get_attendance_data_handler = self.GetAttendanceData()
        self.get_attendance_data_handler.val = self.Controller.User, attendance
        self.get_attendance_data_handler.start()
    
    def set_attendance_data(self, attendance_data):
        self.target_attendance_data = attendance_data
        attendance_data = attendance_data.decode('utf-8')
        table_data = []
        rows = attendance_data.split('\n')
        for row in rows:
            table_row = ["","",""]
            current_row = [*row.split(',')]
            for i in range(len(current_row)):
                table_row[i] = current_row[i]
            table_data.append(table_row)

        attendance_model = self.Model.TableModel(self.View.tv_attendance, table_data)
        self.View.tv_attendance.setModel(attendance_model)
        self.View.tv_attendance.horizontalHeader().setMinimumSectionSize(300)

    def download_attendance(self):
        path = os.path.join(os.path.expanduser('~/Documents'), self.target_attendance)
        ext = self.target_attendance.split('.')[-1]
        path = QFileDialog.getSaveFileName(
            self.View, 'Save File', path, ext)[0]
        if path:
            self.show_alert('file', 'Downloading file...')
            with open(path, 'wb') as file:
                file.write(self.target_attendance_data)
            self.show_alert('file', 'File downloaded')

    def show_alert(self, type, message):
        self.ShowAlert = Alert()
        self.ShowAlert.operation.connect(self.View.show_alert)
        self.ShowAlert.val = type, message
        self.ShowAlert.start()

    def search_attendance(self):
        target_attendance = self.View.txt_search_attendance.text()
        attendance_model = self.View.lv_attendance.model()
        attendances = attendance_model.data
        target_indices = []
        for index, attendance in enumerate(attendances):
            if target_attendance in attendance:
                target_indices.append(index)
            self.View.lv_attendance.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.lv_attendance.setRowHidden(target_index, False)

        self.View.txt_search_attendance.clear()

    def reset_list_target(self, event):
        self.View.txt_search_attendance.clear()
        attendance_model = self.View.lv_attendance.model()
        try:
            attendances = attendance_model.data
            for index, attendance in enumerate(attendances):
                self.View.lv_attendance.setRowHidden(index, False)
        except AttributeError:
            pass

    def more_clicked(self):
        pos = self.View.btn_more.mapToGlobal(self.View.btn_more.rect().bottomLeft())
        height = GetSystemMetrics(1)
        if pos.y() > height - self.View.ContextMenu.height():
            pos_up = self.View.btn_more.mapToGlobal(self.View.btn_more.rect().topLeft())
            self.View.ContextMenu.move(pos_up.x(), pos_up.y()- self.View.ContextMenu.height())
        else:
            self.View.ContextMenu.move(pos)
        self.View.ContextMenu.show()

    def change_password(self):
        self.ChangePassword = ChangePassword(self, self.View, self.Controller.User, self.Model)
        self.ChangePassword.run()

    def sign_out(self):
        self.View.close()

    def lobby_closed(self, event):
        try:
            if self.Controller.View.Meeting.isVisible():
                return
        except AttributeError:
            pass
        self.Controller.SignInController.View.init_sign_in()
        self.Controller.SignInController.Model.init_sign_in()
        self.Controller.SignInController.init_sign_in()
        super(QMainWindow, self.View).closeEvent(event)

    def set_lobby_status_handler(self, status):
        self.handler = SetLobbyStatus(self.View.set_lobby_status)
        self.handler.val = status
        self.handler.start()
        QtCore.QTimer.singleShot(5000, self.View.lbl_lobby_status.clear)