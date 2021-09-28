from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
import socket


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


class Lobby:

    def __init__(self, Controller):
        self.Model = Controller.Model.Lobby
        self.View = Controller.View.Lobby
        self.Controller = Controller

        self.connect_signals()
        self.get_classes()
        self.get_attendances()

        self.View.run()

    def connect_signals(self):
        for side_nav in self.View.side_navs:
            side_nav.operation.connect(self.change_page)
        self.View.resizeEvent = self.resize

        self.View.lv_attendance.clicked.connect(self.attendance_list_clicked)

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
        super(QMainWindow, self.View).resizeEvent(event)

    def init_meeting(self, Class):
        self.Controller.Model.init_meeting()
        self.Controller.View.init_meeting()
        self.Controller.init_meeting(Class)

    def get_attendances(self):
        self.get_all_attendances_handler = self.GetAllAttendances()
        self.get_all_attendances_handler.val = self.Controller.User,
        self.get_all_attendances_handler.start()

    def set_attendances(self, attendances):
        attendance_model = self.Model.ListModel(self.View.lv_attendance, attendances)
        self.View.lv_attendance.setModel(attendance_model)
        index = attendance_model.createIndex(0,0)
        self.View.lv_attendance.setCurrentIndex(index)
        self.View.lv_attendance.model().layoutChanged.emit()
        self.get_attendance_data(attendances[0])

    def attendance_list_clicked(self, index):
        row = index.row()
        attendance_model = self.View.lv_attendance.model()
        attendance = attendance_model.getRowData(row)
        self.get_attendance_data(attendance)

    def get_attendance_data(self, attendance):
        self.get_attendance_data_handler = self.GetAttendanceData()
        self.get_attendance_data_handler.val = self.Controller.User, attendance
        self.get_attendance_data_handler.start()
    
    def set_attendance_data(self, attendance_data):
        data = attendance_data.decode('utf-8')
        table_data = []
        rows = data.split('\n')
        for row in rows:
            table_row = ["","",""]
            current_row = [*row.split(',')]
            for i in range(len(current_row)):
                table_row[i] = current_row[i]
            table_data.append(table_row)

        attendance_model = self.Model.TableModel(self.View.tv_attendance, table_data)
        self.View.tv_attendance.setModel(attendance_model)
        self.View.tv_attendance.horizontalHeader().setMinimumSectionSize(300)



