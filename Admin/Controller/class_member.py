from PyQt5.QtWidgets import QDialog, QTableView, QWidget
from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore
from Admin.Misc.Widgets.data_table import DataTable


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

class ClassMember:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

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
        self.View.btn_delete_class.clicked.connect(self.delete_class)

        self.View.btn_init_class_bulk.clicked.connect(self.init_add_class_bulk)
        self.View.btn_back_class_bulk.clicked.connect(self.go_back_class)
        self.View.btn_add_class_item.clicked.connect(self.View.add_class_item)
        self.View.btn_clear_class_item.clicked.connect(self.View.clear_class_item)
        self.View.btn_add_class_bulk.clicked.connect(self.add_class_bulk)

        self.View.tv_class.keyPressEvent = self.tv_class_key_pressed
        self.View.tv_class.mousePressEvent = self.tv_class_mouse_press
    
    def add_class_bulk(self):
        self.AddItem = AddItem(self.Model.create_class, self.View.verticalLayout_50, self.View.scrollAreaWidgetContents_4, 'classItem_')
        self.AddItem.started.connect(self.View.TableClassLoadingScreen.run)
        self.AddItem.operation.connect(self.go_back_class)
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
        
    # Operations
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
        else:
            self.View.enable_class_edit_delete()

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

    # Buttons
    def init_add_class(self):
        self.View.clear_class_inputs()
        self.View.disable_class_buttons()
        self.View.enable_class_inputs()
        self.View.set_class('Add')

    def init_edit_class(self):
        self.View.disable_class_buttons()
        self.View.enable_class_inputs()
        self.View.set_class('Edit')

    def cancel_class(self):
        self.select_target_class_row()
        self.View.enable_class_buttons()
        self.View.disable_class_inputs()
        self.View.set_class('Read')

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

        if code == self.TargetClass.Code and name == self.TargetClass.Name and start == target_start and end == target_end:
            self.View.btn_cancel_class.click()
            return

        start = ":".join([str(start.hour()), str(start.minute()), str(start.second())])
        end = ":".join([str(end.hour()), str(end.minute()), str(end.second())])
        
        self.get_all_class_handler = self.GetAllClass()
        self.edit_class_handler = self.EditClass()

        self.edit_class_handler.val = self.TargetClass.ID, code, name, start, end
        self.edit_class_handler.operation.connect(self.get_all_class_handler.start)

        self.get_all_class_handler.finished.connect(lambda: self.select_latest_class(code))
        self.edit_class_handler.start()

    # Class Delete
    def delete_class(self):
        self.get_all_class_handler = self.GetAllClass()
        self.delete_class_handler = self.DeleteClass()

        self.delete_class_handler.val = self.TargetClass,
        self.delete_class_handler.operation.connect(self.get_all_class_handler.start)

        self.get_all_class_handler.finished.connect(self.get_latest_class)
        self.delete_class_handler.start()

    # *Class Teacher
    def class_teacher_signals(self):
        self.View.btn_init_add_class_teacher.clicked.connect(self.init_add_class_teacher)
        self.View.btn_delete_class_teacher.clicked.connect(self.delete_target_teacher)
        self.View.lv_class_teacher.clicked.connect(self.list_class_teacher_clicked)

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
        handler = Operation(self.Model.register_teacher_class)
        handler.started.connect(self.View.ClassTeacherLoadingScreen.run)
        handler.finished.connect(self.View.ClassTeacherLoadingScreen.hide)
        return handler

    def DeleteTeacher(self):
        handler = Operation(self.Model.delete_class_teacher)
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
            else:
                self.View.lbl_class_teacher_status.setText('Teachers: 0')
                self.View.disable_class_teacher_delete_clear()

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
        teacher_model = self.Model.TableModel(self.DataTable.tv_target_data, teachers, self.Model.ClassTeacher.get_headers()) 
        self.DataTable.set_model(teacher_model, True)
        self.DataTable.btn_add.clicked.connect(self.add_target_teacher_data)
        self.DataTable.run()

    def add_target_teacher_data(self):
        self.DataTable.close()
        Teacher = self.Model.Teacher(*self.DataTable.get_target_row_data())

        self.get_target_class_teacher_handler = self.GetTargetClassTeacher()
        self.register_teacher_handler = self.RegisterTeacher()

        self.get_target_class_teacher_handler.val = self.TargetClass,
        self.register_teacher_handler.val = self.TargetClass, Teacher
        self.register_teacher_handler.operation.connect(self.get_target_class_teacher_handler.start)

        self.register_teacher_handler.start()

    def delete_target_teacher(self):
        self.get_target_class_teacher_handler = self.GetTargetClassTeacher()
        self.delete_target_teacher_handler = self.DeleteTeacher()

        self.get_target_class_teacher_handler.val = self.TargetClass,
        self.delete_target_teacher_handler.val = self.TargetClassTeacher,
        self.delete_target_teacher_handler.operation.connect(self.get_target_class_teacher_handler.start)

        self.delete_target_teacher_handler.start()

    # *Class Section
    def class_section_signals(self):
        self.View.btn_init_add_class_section.clicked.connect(self.init_add_class_section)
        self.View.lv_class_section.clicked.connect(self.list_class_section_clicked)
        self.View.btn_delete_class_section.clicked.connect(self.delete_target_section)

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

    def RegisterSection(self):
        handler = Operation(self.Model.register_section_class)
        handler.started.connect(self.View.ClassSectionLoadingScreen.run)
        handler.finished.connect(self.View.ClassSectionLoadingScreen.hide)
        return handler

    def DeleteSection(self):
        handler = Operation(self.Model.delete_class_section)
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
            class_section_model = self.Model.ListModel(
                self.View.lv_class_section, sections)
            self.View.lv_class_section.setModel(class_section_model)
            self.target_class_section_row = class_section_model.createIndex(0,0).row()
            self.TargetClassSection = self.Model.ClassSection(None, self.TargetClass.Code, self.TargetClassTeacher.Teacher, class_section_model.getRowData(self.target_class_section_row))
            self.select_latest_class_section()
            self.View.enable_class_section_delete_clear()
            self.View.lbl_class_section_status.setText(f'Sections: {len(sections)}')
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
        section_model = self.Model.TableModel(self.DataTable.tv_target_data, sections, self.Model.ClassSection.get_headers()) 
        self.DataTable.set_model(section_model)
        self.DataTable.btn_add.clicked.connect(self.add_target_section_data)
        self.DataTable.run()

    def add_target_section_data(self):
        self.DataTable.close()
        Section = self.Model.Section(*self.DataTable.get_target_row_data())

        self.get_target_class_section_handler = self.GetTargetClassSection()
        self.register_section_handler = self.RegisterSection()

        self.get_target_class_section_handler.val = self.TargetClass, self.TargetClassTeacher
        self.register_section_handler.val = self.TargetClass, self.TargetClassTeacher, Section
        self.register_section_handler.operation.connect(self.get_target_class_section_handler.start)

        self.register_section_handler.start()

    def delete_target_section(self):
        self.get_target_class_section_handler = self.GetTargetClassSection()
        self.delete_section_handler = self.DeleteSection()

        self.get_target_class_section_handler.val = self.TargetClass, self.TargetClassTeacher
        self.delete_section_handler.val = self.TargetClassSection,
        self.delete_section_handler.operation.connect(self.get_target_class_section_handler.start)

        self.delete_section_handler.start()