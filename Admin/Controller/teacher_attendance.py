import os
from PyQt5.QtWidgets import QFileDialog, QTableView, QWidget
from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore
import csv

from Admin.Misc.Widgets.import_teachers import Import

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

class AddItem(QtCore.QThread):
    operation = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal()

    def __init__(self, fn, layout, widget, tag, additional=None):
        super().__init__()
        self.fn = fn
        self.layout = layout
        self.widget = widget
        self.tag = tag
        self.additional = additional

    def run(self):
        error_items = []
        for index in range(self.layout.count()):
            target_item = self.widget.findChild(QWidget, f'{self.tag}{index+1}')
            if target_item:
                values = target_item.get_value()
                for value in values:
                    if is_blank(value):
                        error_items.append(value)
                if self.additional:
                    values = (*self.additional, *values)
                res = self.fn(*values)
                if res == 'successful':
                    target_item.close_item()
        if error_items:
            self.error.emit()
        else:
            self.operation.emit()
        self.quit()

class Alert(QtCore.QThread):
    operation = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.val = ()

    def run(self):
        self.operation.emit(*self.val)
        self.quit()

class ExportTeacher(QtCore.QThread):
    operation = QtCore.pyqtSignal()

    def __init__(self, fn, alert):
        super().__init__()
        self.alert = alert
        self.fn = fn
        self.path = None

    def run(self):
        if self.path:
            self.alert('file', 'Exporting Tables')
            file_names = ['Teachers.csv']
            file_headers = [('UserID', 'Username','Privilege', 'Salt', 'Hash')]
            tables = self.fn()
            for index, table in enumerate(tables):
                with open(f'{self.path}\{file_names[index]}', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(file_headers[index])
                    writer.writerows(table)
            self.alert('file', 'Tables Exported')
        self.quit()

class ImportTeacherTable(QtCore.QThread):
    error = QtCore.pyqtSignal(object)

    def __init__(self, Model, alert):
        super().__init__()
        self.alert = alert
        self.Model = Model
        self.val = None

    def run(self):
        teachers = self.val
        errors = []
        if teachers:
            with open(teachers, newline='') as csvfile:
                teachers_data = list(csv.reader(csvfile))[1:]
                for index in range(len(teachers_data)):
                    teachers_data[index] = teachers_data[index][1:]
                res = self.Model.import_teacher_table(teachers_data)
                if res != 'successful':
                    errors.append('Teacher')
        if errors:
            self.error.emit(errors)
        self.quit()

class TeacherAttendance:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.target_teacher_row = None
        self.TargetTeacher = None

        self.connect_signals()

    def connect_signals(self):
        self.View.tv_teachers.clicked.connect(self.table_teacher_clicked)
        self.View.btn_init_add_teacher.clicked.connect(self.init_add_teacher)
        self.View.btn_init_edit_teacher.clicked.connect(self.init_edit_teacher)
        self.View.btn_add_edit_teacher.clicked.connect(
            self.init_add_edit_teacher)
        self.View.btn_cancel_teacher.clicked.connect(self.cancel_teacher)
        self.View.btn_delete_teacher.clicked.connect(self.init_delete_teacher)

        self.View.btn_init_teachers_bulk.clicked.connect(self.init_add_teacher_bulk)
        self.View.btn_add_teacher_item.clicked.connect(self.View.add_teacher_item)
        self.View.btn_clear_teacher_item.clicked.connect(self.View.clear_teacher_item)
        self.View.btn_back_teacher_bulk.clicked.connect(self.go_back_teacher)
        self.View.btn_add_teacher_bulk.clicked.connect(self.add_teacher_bulk)

        self.View.tv_teachers.keyPressEvent = self.tv_teachers_key_pressed
        self.View.tv_teachers.mousePressEvent = self.tv_teachers_mouse_press

        self.View.txt_search_teacher.returnPressed.connect(self.search_teacher)
        self.View.btn_search_teacher.clicked.connect(self.search_teacher)
        self.View.btn_delete_attendance.clicked.connect(self.init_delete_teacher_attendances)
        self.View.btn_clear_attendance_table.clicked.connect(self.init_clear_teacher_attendances)

        self.View.btn_import_teachers.clicked.connect(self.get_import_files)
        self.View.btn_export_teachers.clicked.connect(self.init_export_teachers)
        self.View.btn_clear_teachers_table.clicked.connect(self.init_clear_teacher_table)

    def get_import_files(self):
        self.Import = Import(self.View)
        self.Import.operation.connect(self.init_import_teachers)
        self.Import.run()

    def init_import_teachers(self, teachers):
        self.init_import_teachers_handler = self.ImportTeachersTable()
        self.init_import_teachers_handler.val = teachers

        self.get_all_teacher_handler = self.GetAllTeacher()
        self.get_all_teacher_handler.finished.connect(self.get_latest_teacher)
    
        self.init_import_teachers_handler.finished.connect(self.get_all_teacher_handler.start)
        self.init_import_teachers_handler.start()

    def init_export_teachers(self):
        default_path = os.path.expanduser('~/Documents')
        path = QFileDialog.getExistingDirectory(
                self.View, 'Export files to', default_path)
        if path:
            self.export_teachers_handler = self.ExportTeacher()
            self.export_teachers_handler.path = path
            self.export_teachers_handler.start()

    def init_clear_teacher_table(self):
        self.View.show_confirm(self.clear_teacher_table, "Are you sure you want to clear the table?")

    def clear_teacher_table(self):
        self.clear_teacher_table_handler = self.ClearTeacherTable()
        self.get_all_teacher_handler = self.GetAllTeacher()
        self.get_all_teacher_handler.finished.connect(self.get_latest_teacher)
    
        self.clear_teacher_table_handler.finished.connect(self.get_all_teacher_handler.start)
        self.clear_teacher_table_handler.start()

    def init_add_teacher_bulk(self):
        for index in range(self.View.verticalLayout_47.count()):
            target_item = self.View.scrollAreaWidgetContents_3.findChild(QWidget, f'teacherItem_{index}')
            if target_item:
                target_item.close_item()
        self.View.add_teacher_item()
        self.View.add_teacher_item()
        self.View.sw_teacher_attendance.setCurrentIndex(1)

    def add_teacher_bulk(self):
        self.AddItem = AddItem(self.Model.create_teacher, self.View.verticalLayout_47, self.View.scrollAreaWidgetContents_3, 'teacherItem_')
        self.AddItem.started.connect(self.View.TableTeacherLoadingScreen.run)
        self.AddItem.operation.connect(self.go_back_teacher)
        self.AddItem.error.connect(self.teacher_bulk_error)
        self.AddItem.finished.connect(self.View.TableTeacherLoadingScreen.hide)
        self.AddItem.start()

    def teacher_bulk_error(self):
        self.View.run_popup(f"Teacher creation error\nAlready existing or blank", 'warning')
        self.get_all_teacher_handler = self.GetAllTeacher()
        self.get_all_teacher_handler.finished.connect(self.get_latest_teacher)
        self.get_all_teacher_handler.start()

    def go_back_teacher(self):
        self.View.sw_teacher_attendance.setCurrentIndex(0)
        self.get_all_teacher_handler = self.GetAllTeacher()
        self.get_all_teacher_handler.finished.connect(self.get_latest_teacher)
        self.get_all_teacher_handler.start()

    def search_teacher(self):
        target_teacher = self.View.txt_search_teacher.text()
        if target_teacher.lower() == "null":
            return
        teachers_model = self.View.tv_teachers.model()
        teachers = teachers_model.getColumn(1)
        target_indices = []
        for index, teacher in enumerate(teachers):
            if target_teacher in teacher:
                target_indices.append(index)
            self.View.tv_teachers.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.tv_teachers.setRowHidden(target_index, False)

        self.View.txt_search_teacher.clear()
    
    def import_error(self, errors):
        self.View.run_popup(f"Import Error: {', '.join(errors)}", 'critical')

    # Operations
    def ImportTeachersTable(self):
        handler = ImportTeacherTable(self.Model, self.show_alert)
        handler.started.connect(self.View.TableTeacherLoadingScreen.run)
        handler.error.connect(self.import_error)
        handler.finished.connect(self.View.TableTeacherLoadingScreen.hide)
        return handler

    def ExportTeacher(self):
        handler = ExportTeacher(self.Model.export_teacher_table, self.show_alert)
        handler.started.connect(self.View.TableTeacherLoadingScreen.run)
        handler.finished.connect(self.View.TableTeacherLoadingScreen.hide)
        return handler

    def ClearTeacherTable(self):
        handler = Operation(self.Model.clear_teacher_table)
        handler.started.connect(self.View.TableTeacherLoadingScreen.run)
        handler.finished.connect(self.View.TableTeacherLoadingScreen.hide)
        return handler

    def GetAllTeacher(self):
        handler = Get(self.Model.get_all_teacher)
        handler.started.connect(self.View.TableTeacherLoadingScreen.run)
        handler.operation.connect(self.set_teacher_table)
        handler.finished.connect(self.View.TableTeacherLoadingScreen.hide)
        return handler

    def AddTeacher(self):
        handler = Operation(self.Model.create_teacher)
        handler.started.connect(self.View.TeacherLoadingScreen.run)
        handler.error.connect(self.teacher_error)
        handler.finished.connect(self.View.TeacherLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_teacher.click)
        return handler

    def EditTeacher(self):
        handler = Operation(self.Model.edit_teacher)
        handler.started.connect(self.View.TeacherLoadingScreen.run)
        handler.error.connect(self.teacher_error)
        handler.finished.connect(self.View.TeacherLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_teacher.click)
        return handler

    def DeleteTeacher(self):
        handler = Operation(self.Model.delete_teacher)
        handler.started.connect(self.View.TeacherLoadingScreen.run)
        handler.finished.connect(self.View.TeacherLoadingScreen.hide)
        return handler

    def DeleteManyTeacher(self):
        handler = Operation(self.Model.delete_many_teachers)
        handler.started.connect(self.View.TableTeacherLoadingScreen.run)
        handler.finished.connect(
            self.View.TableTeacherLoadingScreen.hide)
        return handler

    def tv_teachers_mouse_press(self, event):
        if event.button() == 2:
            if self.View.tv_teachers.selectionModel().selectedRows():
                self.View.show_menu(
                    self.init_delete_many_teacher, self.View.tv_teachers.mapToGlobal(event.pos()))
        super(QTableView, self.View.tv_teachers).mousePressEvent(event)

    def tv_teachers_key_pressed(self, event):
        if event.key() == 16777223:
            self.init_delete_many_teacher()

        super(QTableView, self.View.tv_teachers).keyPressEvent(event)

    def init_delete_many_teacher(self):
        self.View.show_confirm(self.delete_many_teacher)

    def delete_many_teacher(self):
        indices = self.View.tv_teachers.selectionModel().selectedRows()
        indices = [index.row() for index in indices]
        target_teachers = [[self.View.tv_teachers.model().getRowData(index)[
            0]] for index in indices]

        self.get_all_teacher_handler = self.GetAllTeacher()
        self.delete_many_teacher_handler = self.DeleteManyTeacher()

        self.delete_many_teacher_handler.val = target_teachers,
        self.delete_many_teacher_handler.operation.connect(
            self.get_all_teacher_handler.start)
        
        self.get_all_teacher_handler.finished.connect(
            self.get_latest_teacher)
        self.delete_many_teacher_handler.start()

    # Table
    def set_teacher_table(self, teachers):
        if not teachers:
            self.View.disable_teacher_attendance_edit_delete()
            self.View.disable_teacher_edit_delete()
            self.View.lbl_teachers_table_status.setText(f'Teachers: 0')
        else:
            self.View.enable_teacher_edit_delete()

        teacher_model = self.Model.TableModel(
            self.View.tv_teachers, teachers, self.Model.Teacher.get_headers())
        self.View.tv_teachers.setModel(teacher_model)
        self.View.tv_teachers.horizontalHeader().setMinimumSectionSize(150)
        self.View.lbl_teachers_table_status.setText(
            f'Teachers: {len(teachers)}')

    def table_teacher_clicked(self, index):
        row = index.row()
        teacher_model = self.View.tv_teachers.model()

        if row == teacher_model.rowCount() - 1:
            self.View.btn_init_add_teacher.click()
            return

        self.TargetTeacher = self.Model.Teacher(
            *teacher_model.getRowData(row))
        self.set_teacher_inputs()

        if self.View.teacher_state == 'Add' or self.View.teacher_state == 'Edit':
            self.View.btn_cancel_teacher.click()
            return

        self.get_target_teacher_attendances_handler = self.GetTargetTeacherAttendances()
        self.get_target_teacher_attendances_handler.val = self.TargetTeacher,
        self.get_target_teacher_attendances_handler.start()

    def set_target_teacher(self, Teacher):
        self.TargetTeacher = Teacher
        self.select_target_teacher_row()

    def select_target_teacher_row(self):
        try:
            teacher_model = self.View.tv_teachers.model()
            self.target_teacher_row = teacher_model.findRow(
                self.TargetTeacher.Username)
            self.View.tv_teachers.selectRow(self.target_teacher_row)
            self.View.tv_teachers.setFocus(True)
            self.set_teacher_inputs()
        except AttributeError:
            return
        except TypeError:
            return

    def set_teacher_inputs(self):
        self.View.txt_teacher_username.setText(self.TargetTeacher.Username)
        self.View.txt_teacher_password.setText(
            str(self.TargetTeacher.Salt + self.TargetTeacher.Hash))
        self.View.txt_teacher_password.setCursorPosition(0)

    def select_latest_teacher(self, teacher):
        teacher_model = self.View.tv_teachers.model()
        self.set_target_teacher(self.Model.Teacher(
            *teacher_model.getRowData(teacher_model.findRow(teacher))))

    def get_latest_teacher(self):
        teacher_model = self.View.tv_teachers.model()
        target_teacher_data = teacher_model.getRowData(teacher_model.rowCount() - 2)
        if "NULL" not in target_teacher_data:
            self.set_target_teacher(self.Model.Teacher(*target_teacher_data))
        else:
            self.View.tv_teachers.clearSelection()
            self.View.disable_teacher_attendance_delete_clear()
            self.empty_attendance_list()
            self.View.lbl_attendance_status.setText('Attendances: 0')
            self.View.clear_teacher_inputs()

    # Buttons
    def init_add_teacher(self):
        self.View.tv_teachers.clearSelection()
        self.View.disable_teacher_attendance_delete_clear()
        self.empty_attendance_list()
        self.View.lbl_attendance_status.setText('Attendances: 0')
        self.View.clear_teacher_inputs()
        self.View.disable_teacher_buttons()
        self.View.enable_teacher_inputs()
        self.View.set_teacher('Add')
        self.View.txt_teacher_username.setFocus(True)

    def init_edit_teacher(self):
        self.View.disable_teacher_buttons()
        self.View.enable_teacher_inputs()
        self.View.set_teacher('Edit')

    def cancel_teacher(self):
        self.select_target_teacher_row()
        self.View.enable_teacher_buttons()
        self.View.disable_teacher_inputs()
        self.View.set_teacher('Read')
        if not self.TargetTeacher:
            self.View.clear_teacher_inputs()
            self.View.disable_teacher_edit_delete()
            self.View.disable_teacher_attendance_delete_clear()
            
        if len(self.View.tv_teachers.model().data) != 1:
            self.View.enable_teacher_attendance_delete_clear()
            index = self.View.tv_teachers.model().createIndex(self.target_teacher_row, 0)
            self.table_teacher_clicked(index)
            self.View.tv_teachers.selectRow(self.target_teacher_row)
        else:
            self.View.clear_teacher_inputs()
            self.View.disable_teacher_edit_delete()
            self.View.disable_teacher_attendance_delete_clear()

    def init_add_edit_teacher(self):
        if self.View.teacher_state == "Add":
            self.add_teacher()
        elif self.View.teacher_state == "Edit":
            self.edit_teacher()

    # Teacher Error
    def teacher_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'Teacher exists')

    # Teacher Add
    def add_teacher(self):
        username = self.View.txt_teacher_username.text()
        password = self.View.txt_teacher_password.text()

        if is_blank(username) or is_blank(password):
            self.View.run_popup('Teacher fields must be filled')
            return
        
        self.get_all_teacher_handler = self.GetAllTeacher()
        self.add_teacher_handler = self.AddTeacher()

        self.add_teacher_handler.val = username, password
        self.add_teacher_handler.operation.connect(self.get_all_teacher_handler.start)

        self.get_all_teacher_handler.finished.connect(lambda: self.select_latest_teacher(username))
        self.add_teacher_handler.start()

    # Teacher Edit
    def edit_teacher(self):
        username = self.View.txt_teacher_username.text()
        password = self.View.txt_teacher_password.text()

        if is_blank(username) or is_blank(password):
            self.View.run_pop('Teacher fields must be filled')
            return

        if username == self.TargetTeacher.Username and password == str(self.TargetTeacher.Salt + self.TargetTeacher.Hash):
            self.View.btn_cancel_teacher.click()
            return

        self.get_all_teacher_handler = self.GetAllTeacher()
        self.edit_teacher_handler = self.EditTeacher()

        self.edit_teacher_handler.val = self.TargetTeacher.UserID, username, self.TargetTeacher.Salt, self.TargetTeacher.Hash, password
        self.edit_teacher_handler.operation.connect(self.get_all_teacher_handler.start)

        self.get_all_teacher_handler.finished.connect(lambda: self.select_latest_teacher(username))
        self.edit_teacher_handler.start()

    def init_delete_teacher(self):
        self.View.show_confirm(self.delete_teacher)

    # Teacher Delete
    def delete_teacher(self):
        self.get_all_teacher_handler = self.GetAllTeacher()
        self.delete_teacher_handler = self.DeleteTeacher()

        self.delete_teacher_handler.val = self.TargetTeacher,
        self.delete_teacher_handler.operation.connect(self.get_all_teacher_handler.start)

        self.get_all_teacher_handler.finished.connect(self.get_latest_teacher)
        self.delete_teacher_handler.start()

    # *Attendances
    def GetTargetTeacherAttendances(self):
        handler = Get(self.Model.get_all_attendances)
        handler.started.connect(self.View.AttendanceLoadingScreen.run)
        handler.operation.connect(self.set_teacher_attendances_list)
        handler.finished.connect(self.View.AttendanceLoadingScreen.hide)
        return handler

    def DeleteTeacherAttendances(self):
        handler = Operation(self.Model.delete_teacher_attendances)
        handler.started.connect(self.View.AttendanceLoadingScreen.run)
        handler.finished.connect(self.View.AttendanceLoadingScreen.hide)
        return handler

    def ClearTeacherAttendances(self):
        handler = Operation(self.Model.clear_teacher_attendances)
        handler.started.connect(self.View.AttendanceLoadingScreen.run)
        handler.finished.connect(self.View.AttendanceLoadingScreen.hide)
        return handler

    def set_teacher_attendances_list(self, attendances):
        if not attendances:
            self.View.disable_teacher_attendance_delete_clear()
            self.View.lbl_attendance_status.setText(f'Attendances: 0')
        else:
            self.View.enable_teacher_attendance_delete_clear()

        attendance_model = self.Model.ListModel(self.View.lv_attendance, attendances)
        self.View.lv_attendance.setModel(attendance_model)
        self.View.lbl_attendance_status.setText(f"Attendances: {len(attendances)}")
    
    def init_delete_teacher_attendances(self):
        self.View.show_confirm(self.delete_teacher_attendances)

    def delete_teacher_attendances(self):
        indices = self.View.lv_attendance.selectedIndexes()
        indices = [index.row() for index in indices]
        attendance_model = self.View.lv_attendance.model()
        targets = [[attendance_model.getRowData(index)] for index in indices]

        self.get_target_teacher_attendances_handler = self.GetTargetTeacherAttendances()
        self.delete_teacher_attendances_handler = self.DeleteTeacherAttendances()

        self.get_target_teacher_attendances_handler.val = self.TargetTeacher,
        self.delete_teacher_attendances_handler.val = targets,
        self.delete_teacher_attendances_handler.operation.connect(self.get_target_teacher_attendances_handler.start)
        self.delete_teacher_attendances_handler.start()

    def init_clear_teacher_attendances(self):
        self.View.show_confirm(self.clear_teacher_attendances, "Are you sure you want to remove everything?")

    def clear_teacher_attendances(self):
        self.get_target_teacher_attendances_handler = self.GetTargetTeacherAttendances()
        self.clear_teacher_attendances_handler = self.ClearTeacherAttendances()

        self.get_target_teacher_attendances_handler.val = self.TargetTeacher,
        self.clear_teacher_attendances_handler.val = self.TargetTeacher.Username,
        self.clear_teacher_attendances_handler.operation.connect(self.get_target_teacher_attendances_handler.start)
        self.clear_teacher_attendances_handler.start()

    def empty_attendance_list(self):
        try:
            if self.View.lv_attendance.model().rowCount() != 0:
                self.View.lv_attendance.model().removeRows(
                    0, self.View.lv_attendance.model().rowCount())
        except AttributeError:
            return

    def show_alert(self, type, message):
        self.ShowAlert = Alert()
        self.ShowAlert.operation.connect(self.View.show_alert)
        self.ShowAlert.val = type, message
        self.ShowAlert.start()
    
    