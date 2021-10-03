import csv
import os
from PyQt5.QtWidgets import QDialog, QFileDialog, QTableView, QWidget
from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore
from Admin.Misc.Widgets.data_table import DataTable
from Admin.Misc.Widgets.import_classes_members import Import


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
                else:
                    error_items.append(values)
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

class ExportClassesMembers(QtCore.QThread):
    operation = QtCore.pyqtSignal()

    def __init__(self, fn, alert):
        super().__init__()
        self.alert = alert
        self.fn = fn
        self.path = None

    def run(self):
        if self.path:
            self.alert('file', 'Exporting Tables')
            file_names = ['Classes.csv', 'Class Teachers.csv', 'Class Sections.csv']
            file_headers = [('ID', 'Code', 'Name', 'Start', 'End'), ('ID', 'Code', 'Teacher', 'Host_Address'), ('ID', 'Code', 'Teacher', 'Section')]
            tables = self.fn()
            for index, table in enumerate(tables):
                with open(f'{self.path}\{file_names[index]}', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(file_headers[index])
                    writer.writerows(table)
            self.alert('file', 'Tables Exported')
        self.quit()

class ImportClassesMembersTable(QtCore.QThread):
    error = QtCore.pyqtSignal(object)

    def __init__(self, Model, alert):
        super().__init__()
        self.alert = alert
        self.Model = Model
        self.val = ()

    def run(self):
        _classes, class_teachers, class_sections = self.val
        errors = []
        if _classes:
            with open(_classes, newline='') as csvfile:
                _classes_data = list(csv.reader(csvfile))[1:]
                for index in range(len(_classes_data)):
                    _classes_data[index] = _classes_data[index][1:]
                res = self.Model.import_class_table(_classes_data)
                if res != 'successful':
                    errors.append('Class')
        if class_teachers:
            with open(class_teachers, newline='') as csvfile:
                class_teachers_data = list(csv.reader(csvfile))[1:]
                for index in range(len(class_teachers_data)):
                    class_teachers_data[index] = class_teachers_data[index][1:len(class_teachers_data)]
                res = self.Model.register_teachers_class(class_teachers_data)
                if res != 'successful':
                    errors.append('Class Teacher')
        if class_sections:
            with open(class_sections, newline='') as csvfile:
                class_sections_data = list(csv.reader(csvfile))[1:]
                for index in range(len(class_sections_data)):
                    class_sections_data[index] = class_sections_data[index][1:]
                res = self.Model.register_sections_class(class_sections_data)
                if res != 'successful':
                    errors.append('Class Section')
        if errors:
            self.error.emit(errors)
        self.quit()

class ClassMember:

    def __init__(self, Model, View, Admin):
        self.Model = Model
        self.View = View
        self.Admin = Admin

        self.target_class_row = None
        self.TargetClass = None

        self.target_class_teacher_row = None
        self.TargetClassTeacher = None

        self.target_class_section_row = None
        self.TargetClassSection = None

        self.connect_signals()

    def connect_signals(self):
        self.class_signals()
        self.class_teacher_signals()
        self.class_section_signals()

    # *Class
    def class_signals(self):
        self.View.tv_class.clicked.connect(self.table_class_clicked)
        self.View.btn_init_add_class.clicked.connect(self.init_add_class)
        self.View.btn_init_edit_class.clicked.connect(self.init_edit_class)
        self.View.btn_add_edit_class.clicked.connect(self.init_add_edit_class)
        self.View.btn_cancel_class.clicked.connect(self.cancel_class)
        self.View.btn_delete_class.clicked.connect(self.init_delete_class)

        self.View.btn_init_class_bulk.clicked.connect(self.init_add_class_bulk)
        self.View.btn_back_class_bulk.clicked.connect(self.go_back_class)
        self.View.btn_add_class_item.clicked.connect(self.View.add_class_item)
        self.View.btn_clear_class_item.clicked.connect(self.View.clear_class_item)
        self.View.btn_add_class_bulk.clicked.connect(self.add_class_bulk)

        self.View.tv_class.keyPressEvent = self.tv_class_key_pressed
        self.View.tv_class.mousePressEvent = self.tv_class_mouse_press

        self.View.txt_search_class.returnPressed.connect(self.search_class)
        self.View.btn_search_class.clicked.connect(self.search_class)

        self.View.btn_import_class.clicked.connect(self.get_import_files)
        self.View.btn_export_class.clicked.connect(self.init_export_classes_members)
        self.View.btn_clear_class_table.clicked.connect(self.init_clear_classes_members)

    def get_import_files(self):
        self.Import = Import(self.View)
        self.Import.operation.connect(self.init_import_classes_members)
        self.Import.run()

    def init_import_classes_members(self, _class, class_teachers, class_sections):
        self.init_import_classes_members_handler = self.ImportClassesMembersTable()
        self.init_import_classes_members_handler.val = _class, class_teachers, class_sections

        self.get_all_class_handler = self.GetAllClass()
        self.get_all_class_handler.finished.connect(self.get_latest_class)
        self.get_all_class_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Classes and Members imported successfully"))
    
        self.init_import_classes_members_handler.finished.connect(self.get_all_class_handler.start)
        self.init_import_classes_members_handler.start()

    def import_error(self, errors):
        self.View.run_popup(f"Import Error: {', '.join(errors)}", 'critical') 

    def init_export_classes_members(self):
        default_path = os.path.expanduser('~/Documents')
        path = QFileDialog.getExistingDirectory(
                self.View, 'Export files to', default_path)
        if path:
            self.export_classes_members_handler = self.ExportClassesMembers()
            self.export_classes_members_handler.path = path
            self.export_classes_members_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Classes and Members exported successfully"))
            self.export_classes_members_handler.start()

    def init_clear_classes_members(self):
        self.View.show_confirm(self.clear_classes_members, "Are you sure you want to clear both tables?")

    def clear_classes_members(self):
        self.clear_section_student_handler = self.ClearClassesMembersTable()
        self.get_all_class_handler = self.GetAllClass()
        self.get_all_class_handler.finished.connect(self.get_latest_class)
        self.get_all_class_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Classes and Members table cleared successfully"))
    
        self.clear_section_student_handler.finished.connect(self.get_all_class_handler.start)
        self.clear_section_student_handler.finished.connect(self.View.btn_cancel_class.click)
        self.clear_section_student_handler.finished.connect(lambda: self.View.btn_init_add_class_teacher.setDisabled(True))
        self.clear_section_student_handler.start()

    def add_class_bulk(self):
        self.AddItem = AddItem(self.Model.create_class, self.View.verticalLayout_50, self.View.scrollAreaWidgetContents_4, 'classItem_')
        self.AddItem.started.connect(self.View.TableClassLoadingScreen.run)
        self.AddItem.operation.connect(self.go_back_class)
        items = self.View.verticalLayout_50.count() - 1
        self.AddItem.operation.connect(lambda: self.Admin.set_admin_status(f"{items} classes added successfully"))
        self.AddItem.error.connect(self.class_bulk_error)
        self.AddItem.finished.connect(self.View.TableClassLoadingScreen.hide)
        self.AddItem.start()

    def init_add_class_bulk(self):
        for index in range(self.View.verticalLayout_50.count()):
            target_item = self.View.scrollAreaWidgetContents_4.findChild(QWidget, f'classItem_{index}')
            if target_item:
                target_item.close_item()
        self.View.add_class_item()
        self.View.add_class_item()
        self.View.sw_class.setCurrentIndex(1)

    def show_alert(self, type, message):
        self.ShowAlert = Alert()
        self.ShowAlert.operation.connect(self.View.show_alert)
        self.ShowAlert.val = type, message
        self.ShowAlert.start()

    def go_back_class(self):
        self.View.sw_class.setCurrentIndex(0)
        self.get_all_class_handler = self.GetAllClass()
        self.get_all_class_handler.finished.connect(self.get_latest_class)
        self.get_all_class_handler.start()

    def class_bulk_error(self):
        self.View.run_popup(f"Class creation error\nAlready existing or blank", 'warning')
        self.get_all_class_handler = self.GetAllClass()
        self.get_all_class_handler.finished.connect(self.get_latest_class)
        self.get_all_class_handler.start()

    def search_class(self):
        target_class = self.View.txt_search_class.text()
        if target_class.lower() == "null":
            return
        class_model = self.View.tv_class.model()
        classes = class_model.getColumn(1)
        target_indices = []
        for index, _class in enumerate(classes):
            if target_class in _class:
                target_indices.append(index)
            self.View.tv_class.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.tv_class.setRowHidden(target_index, False)

        self.View.txt_search_class.clear()
        
    # Operations
    def ImportClassesMembersTable(self):
        handler = ImportClassesMembersTable(self.Model, self.show_alert)
        handler.started.connect(self.View.TableClassLoadingScreen.run)
        handler.error.connect(self.import_error)
        handler.finished.connect(self.View.TableClassLoadingScreen.hide)
        return handler

    def ExportClassesMembers(self):
        handler = ExportClassesMembers(self.Model.export_classes_members_table, self.show_alert)
        handler.started.connect(self.View.TableClassLoadingScreen.run)
        handler.finished.connect(self.View.TableClassLoadingScreen.hide)
        return handler

    def ClearClassesMembersTable(self):
        handler = Operation(self.Model.clear_classes_members_table)
        handler.started.connect(self.View.TableClassLoadingScreen.run)
        handler.finished.connect(self.View.TableClassLoadingScreen.hide)
        return handler

    def GetAllClass(self):
        handler = Get(self.Model.get_all_class)
        handler.started.connect(self.View.TableClassLoadingScreen.run)
        handler.operation.connect(self.set_class_table)
        handler.finished.connect(self.View.TableClassLoadingScreen.hide)
        return handler

    def AddClass(self):
        handler = Operation(self.Model.create_class)
        handler.started.connect(self.View.ClassLoadingScreen.run)
        handler.error.connect(self.class_error)
        handler.finished.connect(self.View.ClassLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_class.click)
        return handler 

    def EditClass(self):
        handler = Operation(self.Model.edit_class)
        handler.started.connect(self.View.ClassLoadingScreen.run)
        handler.error.connect(self.class_error)
        handler.finished.connect(self.View.ClassLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_class.click)
        return handler

    def DeleteClass(self):
        handler = Operation(self.Model.delete_class)
        handler.started.connect(self.View.ClassLoadingScreen.run)
        handler.finished.connect(self.View.ClassLoadingScreen.hide)
        return handler 

    def DeleteManyClass(self):
        handler = Operation(self.Model.delete_many_class)
        handler.started.connect(self.View.ClassLoadingScreen.run)
        handler.finished.connect(self.View.ClassLoadingScreen.hide)
        return handler
    
    def tv_class_mouse_press(self, event):
        if event.button() == 2:
            if self.View.tv_class.selectionModel().selectedRows():
                self.View.show_menu(
                    self.init_delete_many_class, self.View.tv_class.mapToGlobal(event.pos()))
        super(QTableView, self.View.tv_class).mousePressEvent(event)

    def tv_class_key_pressed(self, event):
        if event.key() == 16777223:
            self.init_delete_many_class()

        super(QTableView, self.View.tv_class).keyPressEvent(event)

    def init_delete_many_class(self):
        self.View.show_confirm(self.delete_many_class)

    def delete_many_class(self):
        indices = self.View.tv_class.selectionModel().selectedRows()
        indices = [index.row() for index in indices]
        target_classes = [[self.View.tv_class.model().getRowData(index)[
            0]] for index in indices]

        self.get_all_class_handler = self.GetAllClass()
        self.delete_many_class_handler = self.DeleteManyClass()

        self.delete_many_class_handler.val = target_classes,
        self.delete_many_class_handler.operation.connect(
            self.get_all_class_handler.start)
        
        self.get_all_class_handler.finished.connect(
            self.get_latest_class)
        self.get_all_class_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(target_classes)} classes deleted successfully"))
        self.delete_many_class_handler.start()

    # Table
    def table_class_clicked(self, index):
        row = index.row()
        class_model = self.View.tv_class.model()

        if row == class_model.rowCount() - 1:
            self.View.btn_init_add_class.click()
            return

        self.TargetClass = self.Model.Class(
            *class_model.getRowData(row))
        self.target_class_row = row
        self.set_class_inputs()

        if self.View.class_state == 'Add' or self.View.class_state == 'Edit':
            self.View.btn_cancel_class.click()
            return

        self.get_target_class_teacher_handler = self.GetTargetClassTeacher()
        self.get_target_class_teacher_handler.val = self.TargetClass,
        self.get_target_class_teacher_handler.start()

    def set_class_table(self, classes):
        if not classes:
            self.View.disable_class_edit_delete()
            self.View.disable_class_teacher_delete_clear()
            self.View.disable_class_section_delete_clear()
            self.View.lbl_class_table_status.setText('Class: 0')
            self.View.lbl_class_teacher_status.setText('Teachers: 0')
            self.View.lbl_class_section_status.setText('Sections: 0')
            self.View.btn_init_add_class_teacher.setDisabled(True)
            self.View.btn_init_add_class_section.setDisabled(True)
            self.View.disable_class_teacher_delete_clear()
            self.View.disable_class_section_delete_clear()
        else:
            self.View.enable_class_edit_delete()
            self.View.btn_init_add_class_teacher.setDisabled(False)

        class_model = self.Model.TableModel(
            self.View.tv_class, classes, self.Model.Class.get_headers())
        self.View.tv_class.setModel(class_model)
        self.View.tv_class.horizontalHeader().setMinimumSectionSize(150)
        self.View.lbl_class_table_status.setText(
            f'Class: {len(classes)}')

    def set_target_class(self, Class):
        self.TargetClass = Class
        self.select_target_class_row()

    def select_target_class_row(self):
        try:
            class_model = self.View.tv_class.model()
            self.target_class_row = class_model.findRow(
                self.TargetClass.Code)
            self.View.tv_class.selectRow(self.target_class_row)
            self.View.tv_class.setFocus(True)
            self.set_class_inputs()
        except AttributeError:
            return
        except TypeError:
            return

    def set_class_inputs(self):
        try:
            self.View.txt_class_code.setText(self.TargetClass.Code)
            self.View.txt_class_name.setText(self.TargetClass.Name)
            self.View.txt_class_start.setTime(
                QtCore.QTime(*self.TargetClass.Start))
            self.View.txt_class_end.setTime(QtCore.QTime(*self.TargetClass.End))
        except ValueError:
            self.View.clear_class_inputs()

    def select_latest_class(self, _class):
        class_model = self.View.tv_class.model()
        self.set_target_class(self.Model.Class(
            *class_model.getRowData(class_model.findRow(_class))))

    def get_latest_class(self):
        class_model = self.View.tv_class.model()
        self.set_target_class(self.Model.Class(
            *class_model.getRowData(class_model.rowCount() - 2)))
        index = class_model.createIndex(class_model.rowCount() - 2, 0)
        self.table_class_clicked(index)

    # Buttons
    def init_add_class(self):
        self.View.tv_class.clearSelection()
        self.empty_class_teacher_list()
        self.empty_class_section_list()
        self.View.lbl_class_teacher_status.setText('Teachers: 0')
        self.View.lbl_class_section_status.setText('Sections: 0')
        self.View.btn_init_add_class_teacher.setDisabled(True)
        self.View.btn_init_add_class_section.setDisabled(True)
        self.View.disable_class_teacher_delete_clear()
        self.View.disable_class_section_delete_clear()
        self.View.clear_class_inputs()
        self.View.disable_class_buttons()
        self.View.enable_class_inputs()
        self.View.set_class('Add')
        self.View.txt_class_code.setFocus(True)

    def init_edit_class(self):
        self.View.disable_class_buttons()
        self.View.enable_class_inputs()
        self.View.set_class('Edit')

    def cancel_class(self):
        self.View.enable_class_buttons()
        self.View.disable_class_inputs()
        self.View.set_class('Read')
        if not self.TargetClass:
            self.View.clear_class_inputs()
            self.View.disable_class_edit_delete()
            self.View.disable_class_teacher_delete_clear()
            self.View.disable_class_teacher_delete_clear()
            self.View.btn_init_add_class_teacher.setDisabled(True)
            self.View.btn_init_add_class_section.setDisabled(True)
            
        if len(self.View.tv_class.model().data) != 1:
            self.View.btn_init_add_class_teacher.setDisabled(False)
            index = self.View.tv_class.model().createIndex(self.target_class_row, 0)
            self.table_class_clicked(index)
            self.View.tv_class.selectRow(self.target_class_row)
        else:
            self.View.clear_class_inputs()
            self.View.disable_class_edit_delete()
            self.View.disable_class_teacher_delete_clear()
            self.View.disable_class_teacher_delete_clear()
            self.View.btn_init_add_class_teacher.setDisabled(True)
            self.View.btn_init_add_class_section.setDisabled(True)

    def init_add_edit_class(self):
        if self.View.class_state == "Add":
            self.add_class()
        elif self.View.class_state == "Edit":
            self.edit_class()

    # Class Error
    def class_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'Class exists')

    # Class Add
    def add_class(self):
        code = self.View.txt_class_code.text()
        name = self.View.txt_class_name.text()
        start = self.View.txt_class_start.time()
        start = ":".join([str(start.hour()), str(start.minute()), str(start.second())])
        end = self.View.txt_class_end.time()
        end = ":".join([str(end.hour()), str(end.minute()), str(end.second())])

        if is_blank(code) or is_blank(name):
            self.View.run_popup('Class fields must be filled')
            return

        self.get_all_class_handler = self.GetAllClass()
        self.add_class_handler = self.AddClass()

        self.add_class_handler.val = code, name, start, end
        self.add_class_handler.operation.connect(self.get_all_class_handler.start)

        self.get_all_class_handler.finished.connect(lambda: self.select_latest_class(code))
        self.get_all_class_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{code} class added successfully"))
        self.add_class_handler.start()

    # Class Edit
    def edit_class(self):
        code = self.View.txt_class_code.text()
        name = self.View.txt_class_name.text()
        start = self.View.txt_class_start.time()
        end = self.View.txt_class_end.time()
        
        if is_blank(code) or is_blank(name):
            self.View.run_popup(f'Class fields must be filled')
            return

        target_start = QtCore.QTime(*self.TargetClass.Start)
        target_end = QtCore.QTime(*self.TargetClass.End)

        prev = self.TargetClass.Code
        new = None
        if code != self.TargetClass.Code:
            new = code

        if code == self.TargetClass.Code and name == self.TargetClass.Name and start == target_start and end == target_end:
            self.View.btn_cancel_class.click()
            return

        start = ":".join([str(start.hour()), str(start.minute()), str(start.second())])
        end = ":".join([str(end.hour()), str(end.minute()), str(end.second())])
        
        self.get_all_class_handler = self.GetAllClass()
        self.edit_class_handler = self.EditClass()

        self.edit_class_handler.val = self.TargetClass.ID, prev, code, name, start, end
        self.edit_class_handler.operation.connect(self.get_all_class_handler.start)

        self.get_all_class_handler.finished.connect(lambda: self.select_latest_class(code))
        if new:
            self.get_all_class_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Class {prev} updated to {new} successfully"))
        else:
            self.get_all_class_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Class {prev} updated successfully"))

        self.edit_class_handler.start()

    # Class Delete
    def init_delete_class(self):
        self.View.show_confirm(self.delete_class)

    def delete_class(self):
        self.get_all_class_handler = self.GetAllClass()
        self.delete_class_handler = self.DeleteClass()
        target = self.TargetClass

        self.delete_class_handler.val = self.TargetClass,
        self.delete_class_handler.operation.connect(self.get_all_class_handler.start)

        self.get_all_class_handler.finished.connect(self.get_latest_class)
        self.get_all_class_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Class {target.Code} deleted successfully"))
        self.delete_class_handler.start()

    # *Class Teacher
    def class_teacher_signals(self):
        self.View.btn_init_add_class_teacher.clicked.connect(self.init_add_class_teacher)
        self.View.btn_delete_class_teacher.clicked.connect(self.init_delete_target_class_teacher)
        self.View.btn_clear_class_teacher.clicked.connect(self.init_clear_class_teachers)
        self.View.lv_class_teacher.clicked.connect(self.list_class_teacher_clicked)

        self.View.txt_search_class_teacher.returnPressed.connect(self.search_class_teacher)
        self.View.btn_search_class_teacher.clicked.connect(self.search_class_teacher)

    def search_class_teacher(self):
        target_class_teacher = self.View.txt_search_class_teacher.text()
        class_teacher_model = self.View.lv_class_teacher.model()
        class_teachers = class_teacher_model.data
        target_indices = []
        for index, class_teacher in enumerate(class_teachers):
            if target_class_teacher in class_teacher:
                target_indices.append(index)
            self.View.lv_class_teacher.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.lv_class_teacher.setRowHidden(target_index, False)

        self.View.txt_search_class_teacher.clear()

    # Operation
    def GetTargetClassTeacher(self):
        handler = Get(self.Model.get_target_class_teacher)
        handler.started.connect(self.View.ClassTeacherLoadingScreen.run)
        handler.operation.connect(self.set_class_teacher_list)
        handler.finished.connect(self.View.ClassTeacherLoadingScreen.hide)
        return handler

    def GetTeachersNotInClass(self):
        handler = Get(self.Model.get_teacher_not_in_class)
        handler.started.connect(self.View.ClassTeacherLoadingScreen.run)
        handler.operation.connect(self.run_teacher_data_table)
        handler.finished.connect(self.View.ClassTeacherLoadingScreen.hide)
        return handler

    def RegisterTeacher(self):
        handler = Operation(self.Model.register_teachers_class)
        handler.started.connect(self.View.ClassTeacherLoadingScreen.run)
        handler.finished.connect(self.View.ClassTeacherLoadingScreen.hide)
        return handler

    def DeleteClassTeacher(self):
        handler = Operation(self.Model.delete_class_teacher)
        handler.started.connect(self.View.ClassTeacherLoadingScreen.run)
        handler.finished.connect(self.View.ClassTeacherLoadingScreen.hide)
        return handler

    def ClearClassTeacher(self):
        handler = Operation(self.Model.clear_class_teacher)
        handler.started.connect(self.View.ClassTeacherLoadingScreen.run)
        handler.finished.connect(self.View.ClassTeacherLoadingScreen.hide)
        return handler

    # List
    def list_class_teacher_clicked(self, index):
        self.target_class_teacher_row = index.row()
        self.set_target_class_teacher(self.Model.ClassTeacher(
            None, self.TargetClass.Code, self.View.lv_class_teacher.model().getRowData(self.target_class_teacher_row)))

        self.get_target_class_section_handler = self.GetTargetClassSection()
        self.get_target_class_section_handler.val = self.TargetClass, self.TargetClassTeacher
        self.get_target_class_section_handler.start()

    def set_target_class_teacher(self, ClassTeacher):
        self.TargetClassTeacher = ClassTeacher

    def set_class_teacher_list(self, teachers):
        try:
            if teachers:
                class_teacher_model = self.Model.ListModel(
                    self.View.lv_class_teacher, teachers)
                self.View.lv_class_teacher.setModel(class_teacher_model)
                self.target_class_teacher_row = class_teacher_model.createIndex(0,0).row()
                self.TargetClassTeacher = self.Model.ClassTeacher(None, self.TargetClass.Code, class_teacher_model.getRowData(self.target_class_teacher_row))
                self.select_latest_class_teacher()
                self.View.enable_class_teacher_delete_clear()
                self.View.lbl_class_teacher_status.setText(f'Teachers: {len(teachers)}')
                self.View.btn_init_add_class_section.setDisabled(False)
            else:
                self.empty_class_teacher_list()
                self.View.lbl_class_teacher_status.setText('Teachers: 0')
                self.View.disable_class_teacher_delete_clear()
                self.View.btn_init_add_class_section.setDisabled(True)

        except IndexError:
            pass
        
        if self.TargetClass and self.TargetClassTeacher:
            self.get_target_class_section_handler = self.GetTargetClassSection()
            self.get_target_class_section_handler.val = self.TargetClass, self.TargetClassTeacher
            self.get_target_class_section_handler.start()
        else:
            self.View.btn_init_add_class_section.setDisabled(True)
            self.View.lbl_class_section_status.setText('Sections: 0')
            self.View.disable_class_section_delete_clear()

    def select_latest_class_teacher(self):
        class_teachers_model = self.View.lv_class_teacher.model()
        class_teachers = class_teachers_model.getData()
        if class_teachers != []:
            index  = class_teachers_model.createIndex(0,0)
            self.View.lv_class_teacher.setCurrentIndex(index)

    # Buttons
    def init_add_class_teacher(self):
        self.get_teachers_not_in_class_handler = self.GetTeachersNotInClass()
        self.get_teachers_not_in_class_handler.val = self.TargetClass,
        self.get_teachers_not_in_class_handler.start()

    def run_teacher_data_table(self, teachers):
        self.DataTable = DataTable(self.View, 'Teachers')
        self.DataTable.operation.connect(self.add_target_teacher_data)
        teacher_model = self.Model.TableModel(self.DataTable.tv_target_data, teachers, self.Model.ClassTeacher.get_headers()) 
        self.DataTable.set_model(teacher_model, True)
        self.DataTable.run()

    def empty_class_teacher_list(self):
        try:
            if self.View.lv_class_teacher.model().rowCount() != 0:
                self.View.lv_class_teacher.model().removeRows(
                    0, self.View.lv_class_teacher.model().rowCount())
        except AttributeError:
            return

    def add_target_teacher_data(self):
        self.DataTable.close()
        class_teachers = [[self.TargetClass.Code, teacher]
                            for teacher in self.DataTable.get_target_row_data()]

        self.get_target_class_teacher_handler = self.GetTargetClassTeacher()
        self.register_teacher_handler = self.RegisterTeacher()

        self.get_target_class_teacher_handler.val = self.TargetClass,
        self.get_target_class_teacher_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(class_teachers)} teachers added to {self.TargetClass.Code} successfully"))
        self.register_teacher_handler.val = class_teachers,
        self.register_teacher_handler.operation.connect(self.get_target_class_teacher_handler.start)

        self.register_teacher_handler.start()

    def init_delete_target_class_teacher(self):
        self.View.show_confirm(self.delete_target_class_teachers)

    def delete_target_class_teachers(self):
        indices = self.View.lv_class_teacher.selectedIndexes()
        indices = [index.row() for index in indices]
        class_teacher_model = self.View.lv_class_teacher.model()
        targets = [[self.TargetClass.Code, class_teacher_model.getRowData(
            index)] for index in indices]

        self.get_target_class_teacher_handler = self.GetTargetClassTeacher()
        self.delete_target_class_teachers_handler = self.DeleteClassTeacher()

        self.get_target_class_teacher_handler.val = self.TargetClass,
        self.get_target_class_teacher_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(targets)} teachers removed from {self.TargetClass.Code} successfully"))
        self.delete_target_class_teachers_handler.val = targets,
        self.delete_target_class_teachers_handler.operation.connect(self.get_target_class_teacher_handler.start)

        self.delete_target_class_teachers_handler.start()

    def init_clear_class_teachers(self):
        self.View.show_confirm(self.clear_class_teachers, "Are you sure you want to remove everyone?")

    def clear_class_teachers(self):
        self.clear_class_teachers_handler = self.ClearClassTeacher()
        self.clear_class_teachers_handler.val = self.TargetClass.Code,
        index = self.View.tv_class.model().createIndex(self.target_class_row, 0)
        self.clear_class_teachers_handler.operation.connect(lambda: self.table_class_clicked(index))

        self.clear_class_teachers_handler.finished.connect(lambda: self.Admin.set_admin_status("Class teachers list cleared successfully"))
        self.clear_class_teachers_handler.start()

    # *Class Section
    def class_section_signals(self):
        self.View.btn_init_add_class_section.clicked.connect(self.init_add_class_section)
        self.View.lv_class_section.clicked.connect(self.list_class_section_clicked)
        self.View.btn_clear_class_student.clicked.connect(self.init_clear_target_section)
        self.View.btn_delete_class_section.clicked.connect(self.init_delete_target_section)

        self.View.txt_search_class_section.returnPressed.connect(self.search_class_section)
        self.View.btn_search_class_section.clicked.connect(self.search_class_section)

    def search_class_section(self):
        target_class_section = self.View.txt_search_class_section.text()
        class_section_model = self.View.lv_class_section.model()
        class_sections = class_section_model.data
        target_indices = []
        for index, class_section in enumerate(class_sections):
            if target_class_section in class_section:
                target_indices.append(index)
            self.View.lv_class_section.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.lv_class_section.setRowHidden(target_index, False)

        self.View.txt_search_class_section.clear()

    # Operation
    def GetTargetClassSection(self):
        handler = Get(self.Model.get_target_class_section)
        handler.started.connect(self.View.ClassSectionLoadingScreen.run)
        handler.operation.connect(self.set_class_section_list)
        handler.finished.connect(self.View.ClassSectionLoadingScreen.hide)
        return handler

    def GetSectionsNotInClass(self):
        handler = Get(self.Model.get_section_not_in_class)
        handler.started.connect(self.View.ClassSectionLoadingScreen.run)
        handler.operation.connect(self.run_section_data_table)
        handler.finished.connect(self.View.ClassSectionLoadingScreen.hide)
        return handler

    def RegisterSections(self):
        handler = Operation(self.Model.register_sections_class)
        handler.started.connect(self.View.ClassSectionLoadingScreen.run)
        handler.finished.connect(self.View.ClassSectionLoadingScreen.hide)
        return handler

    def DeleteClassSection(self):
        handler = Operation(self.Model.delete_class_section)
        handler.started.connect(self.View.ClassSectionLoadingScreen.run)
        handler.finished.connect(self.View.ClassSectionLoadingScreen.hide)
        return handler

    def ClearClassSection(self):
        handler = Operation(self.Model.clear_class_section)
        handler.started.connect(self.View.ClassSectionLoadingScreen.run)
        handler.finished.connect(self.View.ClassSectionLoadingScreen.hide)
        return handler

    # List
    def list_class_section_clicked(self, index):
        self.target_class_section_row = index.row()
        self.set_target_class_section(self.Model.ClassSection(
            None, self.TargetClass.Code, self.TargetClassTeacher.Teacher, self.View.lv_class_section.model().getRowData(self.target_class_section_row)))

    def set_target_class_section(self, ClassSection):
        self.TargetClassSection = ClassSection

    def set_class_section_list(self, sections):
        try:
            if sections:
                class_section_model = self.Model.ListModel(
                    self.View.lv_class_section, sections)
                self.View.lv_class_section.setModel(class_section_model)
                self.target_class_section_row = class_section_model.createIndex(0,0).row()
                self.TargetClassSection = self.Model.ClassSection(None, self.TargetClass.Code, self.TargetClassTeacher.Teacher, class_section_model.getRowData(self.target_class_section_row))
                self.select_latest_class_section()
                self.View.enable_class_section_delete_clear()
                self.View.lbl_class_section_status.setText(f'Sections: {len(sections)}')
            else:
                self.View.disable_class_section_delete_clear()
                self.View.lbl_class_section_status.setText('Sections: 0')
                self.empty_class_section_list()
        except IndexError:
            return

    def select_latest_class_section(self):
        class_sections_model = self.View.lv_class_section.model()
        class_sections = class_sections_model.getData()
        if class_sections != []:
            index  = class_sections_model.createIndex(0,0)
            self.View.lv_class_section.setCurrentIndex(index)

    # Buttons
    def init_add_class_section(self):
        self.get_sections_not_in_class_handler = self.GetSectionsNotInClass()
        self.get_sections_not_in_class_handler.val = self.TargetClass, self.TargetClassTeacher
        self.get_sections_not_in_class_handler.start()

    def run_section_data_table(self, sections):
        self.DataTable = DataTable(self.View, 'Sections')
        self.DataTable.operation.connect(self.add_target_section_data)
        section_model = self.Model.TableModel(self.DataTable.tv_target_data, sections, self.Model.Section.get_headers()) 
        self.DataTable.set_model(section_model, True)
        self.DataTable.run()
    
    def empty_class_section_list(self):
        try:
            if self.View.lv_class_section.model().rowCount() != 0:
                self.View.lv_class_section.model().removeRows(
                    0, self.View.lv_class_section.model().rowCount())
        except AttributeError:
            return

    def add_target_section_data(self):
        self.DataTable.close()
        class_sections = [[self.TargetClass.Code, self.TargetClassTeacher.Teacher, section]
                            for section in self.DataTable.get_target_row_data()]

        self.get_target_class_section_handler = self.GetTargetClassSection()
        self.register_sections_handler = self.RegisterSections()

        self.get_target_class_section_handler.val = self.TargetClass, self.TargetClassTeacher
        self.get_target_class_section_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(class_sections)} sections added to {self.TargetClassTeacher.Teacher}'s {self.TargetClass.Code} successfully"))
        self.register_sections_handler.val = class_sections,
        self.register_sections_handler.operation.connect(self.get_target_class_section_handler.start)

        self.register_sections_handler.start()

    def init_delete_target_section(self):
        self.View.show_confirm(self.delete_target_section)
    
    def delete_target_section(self):
        indices = self.View.lv_class_section.selectedIndexes()
        indices = [index.row() for index in indices]
        class_section_model = self.View.lv_class_section.model()
        targets = [[self.TargetClass.Code, self.TargetClassTeacher.Teacher, class_section_model.getRowData(
            index)] for index in indices]

        self.get_target_class_section_handler = self.GetTargetClassSection()
        self.delete_section_handler = self.DeleteClassSection()

        self.get_target_class_section_handler.val = self.TargetClass, self.TargetClassTeacher
        self.get_target_class_section_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(targets)} sections removed from {self.TargetClassTeacher.Teacher}'s {self.TargetClass.Code} successfully"))
        self.delete_section_handler.val = targets,
        self.delete_section_handler.operation.connect(self.get_target_class_section_handler.start)

        self.delete_section_handler.start()

    def init_clear_target_section(self):
        self.View.show_confirm(self.clear_target_class_section, "Are you sure you want to remove everyone?")

    def clear_target_class_section(self):
        self.get_target_class_section_handler = self.GetTargetClassSection()
        self.clear_target_class_section_handler = self.ClearClassSection()

        self.get_target_class_section_handler.val = self.TargetClass, self.TargetClassTeacher
        self.get_target_class_section_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{self.TargetClassTeacher.Teacher}'s {self.TargetClass.Code} sections cleared successfully"))
        self.clear_target_class_section_handler.val = self.TargetClass.Code, self.TargetClassTeacher.Teacher
        self.clear_target_class_section_handler.operation.connect(self.get_target_class_section_handler.start)

        self.clear_target_class_section_handler.start()