import os
from PyQt5.QtWidgets import QFileDialog, QTableView, QWidget
from Admin.Misc.Widgets.data_table import DataTable
from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore
import csv

from Admin.Misc.Widgets.import_section_student import Import


class GetTargetSectionStudent(QtCore.QThread):
    operation = QtCore.pyqtSignal(object)
    validation = QtCore.pyqtSignal()

    def __init__(self, SectionStudents):
        super().__init__()
        self.SectionStudents = SectionStudents
        self.value = ()

    def run(self):
        SectionStudents = self.SectionStudents(*self.value)
        if SectionStudents:
            self.operation.emit(SectionStudents)
        else:
            self.validation.emit()
        self.quit()


class GetTargetStudentSection(QtCore.QThread):
    operation = QtCore.pyqtSignal(object, object)
    validation = QtCore.pyqtSignal()

    def __init__(self, StudentSection, SectionStudents):
        super().__init__()
        self.StudentSection = StudentSection
        self.SectionStudents = SectionStudents
        self.value = ()

    def run(self):
        StudentSection = self.StudentSection(*self.value)
        if StudentSection:
            SectionStudents = self.SectionStudents(StudentSection)
            self.operation.emit(StudentSection, SectionStudents)
        else:
            self.validation.emit()
        self.quit()


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


class GetDifference(QtCore.QThread):
    operation = QtCore.pyqtSignal(object)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        res = self.fn()
        self.operation.emit(res)
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
            target_item = self.widget.findChild(
                QWidget, f'{self.tag}{index+1}')
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


class ExportSectionStudentTable(QtCore.QThread):
    operation = QtCore.pyqtSignal()

    def __init__(self, fn, alert):
        super().__init__()
        self.alert = alert
        self.fn = fn
        self.path = None

    def run(self):
        if self.path:
            self.alert('file', 'Exporting Tables')
            file_names = ['Sections.csv',
                          'Students.csv', 'Section Students.csv']
            file_headers = [('ID', 'Name'), ('UserID', 'Username','Privilege', 'Salt', 'Hash'), ('ID', 'Section', 'Student')]
            tables = self.fn()
            for index, table in enumerate(tables):
                with open(f'{self.path}\{file_names[index]}', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(file_headers[index])
                    writer.writerows(table)
            self.alert('file', 'Tables Exported')
        self.quit()


class ImportSectionStudentTable(QtCore.QThread):
    error = QtCore.pyqtSignal(object)

    def __init__(self, Model, alert):
        super().__init__()
        self.alert = alert
        self.Model = Model
        self.val = ()

    def run(self):
        sections, student, section_student = self.val
        errors = []
        if sections:
            with open(sections, newline='') as csvfile:
                sections_data = list(csv.reader(csvfile))[1:]
                for index in range(len(sections_data)):
                    sections_data[index] = sections_data[index][1:]
                res = self.Model.import_section_table(sections_data)
                if res != 'successful':
                    errors.append('Section')
        if student:
            with open(student, newline='') as csvfile:
                student_data = list(csv.reader(csvfile))[1:]
                for index in range(len(student_data)):
                    student_data[index] = student_data[index][1:]
                res = self.Model.import_student_table(student_data)
                if res != 'successful':
                    errors.append('Student')
        if section_student:
            with open(section_student, newline='') as csvfile:
                section_student_data = list(csv.reader(csvfile))[1:]
                for index in range(len(section_student_data)):
                    section_student_data[index] = section_student_data[index][1:]
                res = self.Model.assign_student_section(section_student_data)
                if res != 'successful':
                    errors.append('Section Student')
        if errors:
            self.error.emit(errors)
        self.quit()


class Alert(QtCore.QThread):
    operation = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.val = ()

    def run(self):
        self.operation.emit(*self.val)
        self.quit()


class SectionStudent:

    def __init__(self, Model, View, Admin):
        self.Model = Model
        self.View = View
        self.Admin = Admin

        self.target_section_row = 0
        self.TargetSection = None
        self.target_student_row = 0
        self.TargetStudent = None
        self.target_section_student_row = 0
        self.TargetSectionStudent = None

        self.connect_signals()

    def connect_signals(self):
        self.section_signals()
        self.student_signals()
        self.sectionstudent_signals()

        self.View.btn_import_students_sections.clicked.connect(
            self.get_import_files)
        self.View.btn_export_students_sections.clicked.connect(
            self.init_export_section_student)
        self.View.btn_clear_students_sections_table.clicked.connect(
            self.init_clear_section_student)

    def ImportSectionStudentTable(self):
        handler = ImportSectionStudentTable(self.Model, self.show_alert)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.error.connect(self.import_error)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def ExportSectionStudentTable(self):
        handler = ExportSectionStudentTable(
            self.Model.export_section_student_table, self.show_alert)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def ClearSectionStudentTable(self):
        handler = Operation(self.Model.clear_section_student_table)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def import_error(self, errors):
        self.View.run_popup(f"Import Error: {', '.join(errors)}", 'critical')

    def get_import_files(self):
        self.Import = Import(self.View)
        self.Import.operation.connect(self.init_import_section_student)
        self.Import.run()

    def init_import_section_student(self, section, students, section_students):
        self.init_import_section_student_handler = self.ImportSectionStudentTable()
        self.init_import_section_student_handler.val = section, students, section_students

        self.get_all_section_handler = self.GetAllSection()
        self.get_all_student_handler = self.GetAllStudents()

        self.init_import_section_student_handler.finished.connect(
            self.get_all_section_handler.start)
        self.get_all_section_handler.finished.connect(
            self.get_all_student_handler.start)
        self.get_all_student_handler.finished.connect(
            self.View.btn_cancel_section.click)
        self.get_all_student_handler.finished.connect(lambda: self.Admin.set_admin_status("Sections and Students imported successfully"))

        self.init_import_section_student_handler.start()

    def init_export_section_student(self):
        default_path = os.path.expanduser('~/Documents')
        path = QFileDialog.getExistingDirectory(
            self.View, 'Export files to', default_path)
        if path:
            self.init_export_section_student_handler = self.ExportSectionStudentTable()
            self.init_export_section_student_handler.path = path
            self.init_export_section_student_handler.finished.connect(lambda: self.Admin.set_admin_status("Sections and Students exported successfully"))
            self.init_export_section_student_handler.start()

    def show_alert(self, type, message):
        self.ShowAlert = Alert()
        self.ShowAlert.operation.connect(self.View.show_alert)
        self.ShowAlert.val = type, message
        self.ShowAlert.start()

    def init_clear_section_student(self):
        self.View.show_confirm(self.clear_section_student,
                               "Are you sure you want to clear both tables?")

    def clear_section_student(self):
        self.clear_section_student_handler = self.ClearSectionStudentTable()
        self.clear_section_student_handler.finished.connect(self.Admin.init_databases)
        self.clear_section_student_handler.finished.connect(lambda: self.Admin.set_admin_status("Sections and Students table cleared successfully"))
        self.clear_section_student_handler.start()

    # *SectionStudent
    def sectionstudent_signals(self):
        self.View.lv_section_student.clicked.connect(
            self.list_sectionstudent_clicked)
        self.View.btn_init_add_section_student.clicked.connect(
            self.get_all_unassigned_students)
        self.View.btn_delete_section_student.clicked.connect(
            self.init_delete_section_student)
        self.View.btn_clear_section_student_table.clicked.connect(
            self.init_remove_all_section_students)

        self.View.txt_search_section_student.returnPressed.connect(
            self.search_section_student)
        self.View.btn_search_section_student.clicked.connect(
            self.search_section_student)

    def search_section_student(self):
        target_student = self.View.txt_search_section_student.text()
        section_student_model = self.View.lv_section_student.model()
        students = section_student_model.data
        target_indices = []
        for index, student in enumerate(students):
            if target_student in student:
                target_indices.append(index)
            self.View.lv_section_student.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.lv_section_student.setRowHidden(target_index, False)

        self.View.txt_search_section_student.clear()

    # SectionStudent Operation
    def GetAllUnassignedStudents(self):
        handler = Get(self.Model.get_all_unassigned_students)
        return handler

    def AssignStudentSection(self):
        handler = Operation(self.Model.assign_student_section)
        handler.started.connect(self.View.SectionStudentLoadingScreen.show)
        handler.finished.connect(self.View.SectionStudentLoadingScreen.hide)
        return handler

    def DeleteStudentSection(self):
        handler = Operation(self.Model.delete_section_student)
        handler.started.connect(self.View.SectionStudentLoadingScreen.show)
        handler.finished.connect(self.View.SectionStudentLoadingScreen.hide)
        return handler

    def RemoveAllStudentSection(self):
        handler = Operation(self.Model.remove_all_section_students)
        handler.started.connect(self.View.SectionStudentLoadingScreen.show)
        handler.finished.connect(self.View.SectionStudentLoadingScreen.hide)
        return handler

    # List
    def set_target_section_student(self, SectionStudent):
        self.TargetSectionStudent = SectionStudent
        self.select_target_section_student_row()

    def select_target_section_student_row(self):
        section_student_model = self.View.lv_section_student.model()
        self.target_section_student_row = section_student_model.createIndex(
            section_student_model.findRow(self.TargetSectionStudent.Student), 0)
        self.View.lv_section_student.setCurrentIndex(
            self.target_section_student_row)

    def set_section_student_list(self, sectionstudents):
        if not sectionstudents:
            self.View.disable_section_student_delete_clear()

        section_student_model = self.Model.ListModel(
            self.View.lv_section_student, sectionstudents)
        self.View.lv_section_student.setModel(section_student_model)

    def list_sectionstudent_clicked(self, index):
        row = index.row()
        self.TargetSectionStudent = self.Model.SectionStudent(
            None, self.View.txt_section_name.text(), self.View.lv_section_student.model().getRowData(row))
        student_model = self.View.tv_students.model()
        self.set_target_student(self.Model.Student(
            *student_model.getRowData(student_model.findRow(self.TargetSectionStudent.Student))))

    def empty_section_student_list(self):
        try:
            if self.View.lv_section_student.model().rowCount() != 0:
                self.View.lv_section_student.model().removeRows(
                    0, self.View.lv_section_student.model().rowCount())
        except AttributeError:
            return

    def get_all_unassigned_students(self):
        self.get_all_unassigned_students_handler = self.GetAllUnassignedStudents()
        self.get_all_unassigned_students_handler.started.connect(
            self.View.SectionStudentLoadingScreen.show)
        self.get_all_unassigned_students_handler.finished.connect(
            self.View.SectionStudentLoadingScreen.hide)
        self.get_all_unassigned_students_handler.operation.connect(
            self.init_add_section_student)
        self.get_all_unassigned_students_handler.start()

    def init_add_section_student(self, students):
        self.DataTable = DataTable(self.View, "Students")
        self.DataTable.operation.connect(self.assign_student_section)
        target_model = self.Model.TableModel(
            self.DataTable.tv_target_data, students, self.Model.Student.get_headers())
        self.DataTable.set_model(target_model, True)
        self.DataTable.run()

    # Add
    def assign_student_section(self):
        self.DataTable.close()
        section_students = [[self.TargetSection.Name, student]
                            for student in self.DataTable.get_target_row_data()]

        self.assign_student_section_handler = self.AssignStudentSection()
        self.assign_student_section_handler.val = section_students,
        self.assign_student_section_handler.finished.connect(
            lambda: self.View.lbl_section_students_status.setText(f'Students: {len(section_students)}'))

        self.get_target_section_student_handler = self.GetTargetSectionStudent()
        self.get_target_section_student_handler.value = self.TargetSection,
        self.get_target_section_student_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(section_students)} students added to {self.TargetSection.Name} successfully"))

        self.assign_student_section_handler.operation.connect(
            self.get_target_section_student_handler.start)
        self.assign_student_section_handler.start()

    # Delete
    def init_delete_section_student(self):
        self.View.show_confirm(self.delete_section_student)

    def delete_section_student(self):
        indices = self.View.lv_section_student.selectedIndexes()
        indices = [index.row() for index in indices]
        section_student_model = self.View.lv_section_student.model()
        targets = [[self.TargetSection.Name, section_student_model.getRowData(
            index)] for index in indices]

        self.delete_section_student_handler = self.DeleteStudentSection()
        self.delete_section_student_handler.val = targets,

        self.get_target_section_student_handler = self.GetTargetSectionStudent()
        self.get_target_section_student_handler.value = self.TargetSection,
        self.get_target_section_student_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(targets)} students removed from {self.TargetSection.Name} successfully"))

        self.delete_section_student_handler.operation.connect(
            self.get_target_section_student_handler.start)
        self.delete_section_student_handler.start()

    def init_remove_all_section_students(self):
        self.View.show_confirm(
            self.remove_all_section_students, "Are you sure you want to remove everyone?")

    def remove_all_section_students(self):
        self.remove_all_section_students_handler = self.RemoveAllStudentSection()
        self.remove_all_section_students_handler.val = self.TargetSection.Name,

        self.get_target_section_student_handler = self.GetTargetSectionStudent()
        self.get_target_section_student_handler.value = self.TargetSection,
        self.get_target_section_student_handler.finished.connect(lambda: self.Admin.set_admin_status(f"All students removed from {self.TargetSection.Name} successfully"))

        self.remove_all_section_students_handler.operation.connect(
            self.get_target_section_student_handler.start)
        self.remove_all_section_students_handler.start()

    # *Section
    def section_signals(self):
        self.View.tv_sections.clicked.connect(self.table_section_clicked)
        self.View.tv_sections.doubleClicked.connect(self.table_section_clicked)
        self.View.btn_init_add_section.clicked.connect(self.init_add_section)
        self.View.btn_init_edit_section.clicked.connect(self.init_edit_section)
        self.View.btn_add_edit_section.clicked.connect(
            self.init_add_edit_section)
        self.View.btn_cancel_section.clicked.connect(self.cancel_section)
        self.View.btn_delete_section.clicked.connect(self.init_delete_section)

        self.View.txt_section_name.returnPressed.connect(
            self.init_add_edit_section)

        self.View.tv_sections.keyPressEvent = self.tv_sections_key_pressed
        self.View.tv_sections.mousePressEvent = self.tv_sections_mouse_press

        self.View.txt_search_section.returnPressed.connect(
            self.search_section)
        self.View.btn_search_sections.clicked.connect(
            self.search_section)

        self.View.btn_init_section_bulk.clicked.connect(
            self.init_add_section_bulk
        )
        self.View.btn_back_section_bulk.clicked.connect(
            self.go_back_section
        )
        self.View.btn_add_section_item.clicked.connect(
            self.View.add_section_item)
        self.View.btn_clear_section_items.clicked.connect(
            self.View.clear_section_item)
        self.View.btn_add_section_bulk.clicked.connect(
            self.add_section_bulk)

    def init_add_section_bulk(self):
        for index in range(self.View.verticalLayout_53.count()):
            target_item = self.View.scrollAreaWidgetContents_5.findChild(
                QWidget, f'sectionItem_{index}')
            if target_item:
                target_item.close_item()
        self.View.add_section_item()
        self.View.add_section_item()
        self.View.sw_student_section.setCurrentIndex(2)

    def add_section_bulk(self):
        self.AddItem = AddItem(self.Model.create_section, self.View.verticalLayout_53,
                               self.View.scrollAreaWidgetContents_5, 'sectionItem_')
        self.AddItem.started.connect(
            self.View.TableSectionStudentLoadingScreen.run)
        self.AddItem.operation.connect(self.go_back_section)
        items = self.View.verticalLayout_53.count()-1
        self.AddItem.operation.connect(lambda: self.Admin.set_admin_status(f"{items} sections added successfully"))
        self.AddItem.error.connect(self.section_bulk_error)
        self.AddItem.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        self.AddItem.start()

    def go_back_section(self):
        self.View.sw_student_section.setCurrentIndex(0)
        self.get_all_section_handler = self.GetAllSection()
        self.get_all_section_handler.finished.connect(
            self.get_latest_target_section_student)
        self.get_all_section_handler.start()

    def section_bulk_error(self):
        self.View.run_popup(
            f"Section creation error\nAlready existing or blank", 'warning')
        self.get_all_section_handler = self.GetAllSection()
        self.get_all_section_handler.finished.connect(
            self.get_latest_target_section_student)
        self.get_all_section_handler.start()

    def search_section(self):
        target_section = self.View.txt_search_section.text()
        if target_section.lower() == "null":
            return
        sections_model = self.View.tv_sections.model()
        sections = sections_model.getColumn(1)
        target_indices = []
        for index, section in enumerate(sections):
            if target_section in section:
                target_indices.append(index)
            self.View.tv_sections.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.tv_sections.setRowHidden(target_index, False)

        self.View.txt_search_section.clear()

    def reset_target_section(self):
        self.TargetSection = None

    # Section Operations
    def GetTargetSectionStudent(self):
        handler = GetTargetSectionStudent(
            self.Model.get_all_section_student)
        handler.operation.connect(
            self.get_target_section_student)
        handler.operation.connect(
            self.View.enable_student_edit_delete)
        handler.operation.connect(
            self.View.enable_section_student_delete_clear)
        handler.operation.connect(
            lambda: self.View.btn_init_add_section_student.setDisabled(False)
        )
        handler.validation.connect(
            self.View.tv_students.clearSelection)
        handler.validation.connect(
            self.empty_section_student_list)
        handler.validation.connect(
            self.View.clear_student_inputs)
        handler.validation.connect(
            self.View.disable_student_edit_delete)
        handler.validation.connect(
            self.reset_target_student)
        handler.validation.connect(
            lambda: self.View.lbl_section_students_status.setText('Students: 0'))
        handler.validation.connect(
            self.View.disable_section_student_delete_clear
        )
        return handler

    def GetAllSection(self):
        handler = Get(self.Model.get_all_section)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.operation.connect(self.set_section_table)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def AddSection(self):
        handler = Operation(self.Model.create_section)
        handler.started.connect(self.View.SectionLoadingScreen.run)
        handler.error.connect(self.section_error)
        handler.finished.connect(self.View.SectionLoadingScreen.hide)
        return handler

    def EditSection(self):
        handler = Operation(self.Model.edit_section)
        handler.started.connect(self.View.SectionLoadingScreen.run)
        handler.error.connect(self.section_error)
        handler.finished.connect(self.View.SectionLoadingScreen.hide)
        return handler

    def DeleteSection(self):
        handler = Operation(self.Model.delete_section)
        handler.started.connect(self.View.SectionLoadingScreen.run)
        handler.finished.connect(self.View.SectionLoadingScreen.hide)
        return handler

    def DeleteManySection(self):
        handler = Operation(self.Model.delete_many_sections)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def tv_sections_mouse_press(self, event):
        if event.button() == 2:
            if self.View.tv_sections.selectionModel().selectedRows():
                self.View.show_menu(
                    self.init_delete_many_section, self.View.tv_sections.mapToGlobal(event.pos()))
        super(QTableView, self.View.tv_sections).mousePressEvent(event)

    def tv_sections_key_pressed(self, event):
        if event.key() == 16777223:
            self.init_delete_many_section()

        super(QTableView, self.View.tv_sections).keyPressEvent(event)

    def init_delete_many_section(self):
        self.View.show_confirm(self.delete_many_section)

    def delete_many_section(self):
        indices = self.View.tv_sections.selectionModel().selectedRows()
        indices = [index.row() for index in indices]
        target_sections = [[self.View.tv_sections.model().getRowData(index)[
            0]] for index in indices]

        self.get_all_section_handler = self.GetAllSection()
        self.delete_many_section_handler = self.DeleteManySection()

        self.delete_many_section_handler.val = target_sections,
        self.delete_many_section_handler.operation.connect(
            self.get_all_section_handler.start)

        self.get_all_section_handler.finished.connect(
            self.get_latest_target_section_student)
        self.get_all_section_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(target_sections)} sections deleted successfully"))
        self.delete_many_section_handler.start()

    # Table
    def table_section_clicked(self, index):
        row = index.row()
        section_model = self.View.tv_sections.model()

        if section_model.getRowData(row)[0] == 'NULL':
            self.View.btn_init_add_section.click()
            return

        self.View.enable_section_buttons()
        self.TargetSection = self.Model.Section(
            *section_model.getRowData(row))
        self.target_section_row = row
        self.View.txt_section_name.setText(self.TargetSection.Name)

        if self.View.section_state == 'Add' or self.View.section_state == 'Edit':
            self.View.btn_cancel_section.click()
            return

        self.get_target_section_student_handler = self.GetTargetSectionStudent()
        self.get_target_section_student_handler.value = self.TargetSection,
        self.get_target_section_student_handler.start()

    def get_target_section_student(self, sectionstudents):
        try:
            if sectionstudents != ():
                target_section_student = sectionstudents[-1]
                student_model = self.View.tv_students.model()
                target_student = self.Model.Student(
                    *student_model.getRowData(student_model.findRow(target_section_student.Student)))

                self.set_section_student_list(sectionstudents)
                self.View.lbl_section_students_status.setText(
                    f'Students: {len(sectionstudents)}')
                self.set_target_section_student(target_section_student)
                self.set_target_student(target_student)
                self.View.enable_section_edit_delete()
                self.View.enable_section_student_delete_clear()
            else:
                self.View.tv_students.clearSelection()
                self.View.clear_student_inputs()
                self.View.lv_section_student.model().removeRows(
                    0, self.View.lv_section_student.model().rowCount())
                self.View.disable_section_edit_delete()
                self.View.disable_section_student_delete_clear()
        except AttributeError:
            return

    def set_target_section(self, Section):
        self.TargetSection = Section
        self.select_target_section_row()

    def select_target_section_row(self):
        try:
            section_model = self.View.tv_sections.model()
            self.target_section_row = section_model.findRow(
                self.TargetSection.Name)
            self.View.tv_sections.selectRow(self.target_section_row)
            self.set_section_inputs()
        except AttributeError:
            self.View.clear_section_inputs()
            self.View.disable_section_edit_delete()

    def set_section_inputs(self):
        self.View.tv_sections.selectRow(self.target_section_row)
        self.View.txt_section_name.setText(self.TargetSection.Name)

    def set_section_table(self, sections):
        if not sections:
            self.View.disable_section_edit_delete()
            self.View.disable_student_edit_delete()
            self.View.disable_section_student_delete_clear()
            self.View.clear_section_inputs()
            self.View.lbl_sections_table_status.setText(f'Sections: 0')
            self.View.btn_init_add_section_student.setDisabled(True)
        else:
            self.View.btn_init_add_section_student.setDisabled(False)
            self.View.enable_section_edit_delete()

        section_model = self.Model.TableModel(
            self.View.tv_sections, sections, self.Model.Section.get_headers())
        self.View.tv_sections.setModel(section_model)
        self.View.tv_sections.horizontalHeader().setMinimumSectionSize(150)
        self.View.lbl_sections_table_status.setText(
            f'Sections: {len(sections)}')

    def select_latest_section(self, section):
        section_model = self.View.tv_sections.model()
        self.set_target_section(self.Model.Section(
            *section_model.getRowData(section_model.findRow(section))))

    def get_latest_target_section_student(self):
        section_model = self.View.tv_sections.model()
        if section_model.rowCount() - 1 == 0:
            self.View.txt_section_name.clear()
            self.View.disable_section_edit_delete()
            self.reset_target_section()
            return
        self.set_target_section(self.Model.Section(
            *section_model.getRowData(section_model.rowCount() - 2)))

        self.get_target_section_student_handler = self.GetTargetSectionStudent()
        self.get_target_section_student_handler.value = self.TargetSection,
        self.get_target_section_student_handler.start()

    # Buttons
    def init_add_section(self):
        self.View.disable_student_edit_delete()
        self.View.disable_section_student_delete_clear()
        self.View.btn_init_add_section_student.setDisabled(True)
        self.View.tv_sections.clearSelection()
        self.View.tv_students.clearSelection()
        self.empty_section_student_list()
        self.View.clear_student_inputs()
        self.View.clear_section_inputs()
        self.View.disable_section_buttons()
        self.View.enable_section_inputs()
        self.View.set_section('Add')
        self.View.tv_sections.clearSelection()
        self.View.tv_students.clearSelection()
        self.View.lv_section_student.clearSelection()
        self.View.lbl_section_students_status.setText("Students: 0")
        self.View.txt_section_name.setFocus(True)

    def init_edit_section(self):
        self.View.disable_section_buttons()
        self.View.enable_section_inputs()
        self.View.set_section('Edit')

    def cancel_section(self):
        self.View.clear_section_inputs()
        self.View.enable_section_buttons()
        self.View.disable_section_inputs()
        self.View.set_section('Read')
        if not self.TargetSection:
            self.View.disable_section_edit_delete()
            self.View.disable_student_edit_delete()
            self.View.disable_section_student_delete_clear()
        if len(self.View.tv_sections.model().data) != 1:
            index = self.View.tv_sections.model().createIndex(self.target_section_row, 0)
            self.table_section_clicked(index)
            self.View.tv_sections.selectRow(self.target_section_row)

    def init_add_edit_section(self):
        if self.View.section_state == "Add":
            self.add_section()
        elif self.View.section_state == "Edit":
            self.edit_section()

    # Section Error
    def section_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'Section exists')

    # Section Add
    def add_section(self):
        section = self.View.txt_section_name.text()
        if is_blank(section):
            self.View.run_popup('Section fields must be filled')
            return

        try:
            self.get_all_section_handler = self.GetAllSection()
            self.add_section_handler = self.AddSection()

            self.add_section_handler.val = section,
            self.add_section_handler.operation.connect(
                self.get_all_section_handler.start)

            self.get_all_section_handler.finished.connect(
                lambda: self.select_latest_section(section))
            self.get_all_section_handler.finished.connect(
                self.View.tv_students.clearSelection)
            self.get_all_section_handler.finished.connect(
                self.empty_section_student_list)
            self.get_all_section_handler.finished.connect(
                self.View.btn_cancel_section.click)
            self.get_all_section_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Section {section} added successfully"))
            self.add_section_handler.start()
        except AttributeError:
            return

    # Section Edit
    def edit_section(self):
        section = self.View.txt_section_name.text()
        if is_blank(section):
            self.View.run_popup('Section fields must be filled')
            return
        
        prev = self.TargetSection.Name
        new = None
        if section != self.TargetSection.Name:
            new = section

        if section == self.TargetSection.Name:
            self.View.btn_cancel_section.click()
            return

        self.get_all_section_handler = self.GetAllSection()
        self.edit_section_handler = self.EditSection()

        self.edit_section_handler.val = self.TargetSection.ID, prev, section
        self.edit_section_handler.operation.connect(
            self.get_all_section_handler.start)

        self.get_all_section_handler.finished.connect(
            lambda: self.select_latest_section(section))
        self.get_all_section_handler.finished.connect(
            self.View.btn_cancel_section.click)
        if new:
            self.get_all_section_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Section {prev} updated to {new} successfully"))
        else:
            self.get_all_section_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Section {prev} updated successfully"))
        self.edit_section_handler.start()

    # Section Delete
    def init_delete_section(self):
        self.View.show_confirm(self.delete_section)

    def delete_section(self):
        self.get_all_section_handler = self.GetAllSection()
        self.delete_section_handler = self.DeleteSection()
        target = self.TargetSection
        self.delete_section_handler.val = self.TargetSection,
        self.delete_section_handler.operation.connect(
            self.get_all_section_handler.start)

        self.get_all_section_handler.finished.connect(
            self.get_latest_target_section_student)
        self.get_all_section_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Section {target.Name} deleted successfully"))
        self.delete_section_handler.start()

    # *Student
    def student_signals(self):
        self.View.tv_students.doubleClicked.connect(self.table_student_clicked)
        self.View.tv_students.clicked.connect(self.table_student_clicked)
        self.View.btn_init_add_student.clicked.connect(self.init_add_student)
        self.View.btn_init_edit_student.clicked.connect(self.init_edit_student)
        self.View.btn_add_edit_student.clicked.connect(
            self.init_add_edit_student)
        self.View.btn_cancel_student.clicked.connect(self.cancel_student)
        self.View.btn_delete_student.clicked.connect(self.init_delete_student)

        self.View.txt_student_username.returnPressed.connect(
            self.init_add_edit_student)

        self.View.tv_students.mousePressEvent = self.tv_students_mouse_press
        self.View.tv_students.keyPressEvent = self.tv_students_key_pressed

        self.View.txt_search_student.returnPressed.connect(
            self.search_student)
        self.View.btn_search_students.clicked.connect(
            self.search_student)

        self.View.btn_init_student_bulk.clicked.connect(
            self.init_add_student_bulk
        )
        self.View.btn_back_student_bulk.clicked.connect(
            self.go_back_student
        )
        self.View.btn_add_student_item.clicked.connect(
            self.View.add_student_item
        )
        self.View.btn_clear_student_items.clicked.connect(
            self.View.clear_student_item
        )
        self.View.btn_add_student_bulk.clicked.connect(
            self.add_student_bulk
        )
        self.View.section_combobox.currentIndexChanged.connect(
            self.combobox_index_changed)

    def init_add_student_bulk(self):
        self.View.section_combobox.clear()
        sections = self.View.tv_sections.model().getColumn(1)

        for section in sections:
            self.View.section_combobox.addItem(section)

        self.View.section_combobox.adjustSize()

        for index in range(self.View.verticalLayout_38.count()):
            target_item = self.View.widget_11.findChild(
                QWidget, f'studentItem_{index}')
            if target_item:
                target_item.close_item()
        self.View.add_student_item()
        self.View.add_student_item()

        self.View.sw_student_section.setCurrentIndex(1)

    def add_student_bulk(self):
        self.AddItem = AddItem(self.Model.create_student, self.View.verticalLayout_38,
                               self.View.widget_11, 'studentItem_', (self.TargetSection.Name,))
        self.AddItem.started.connect(
            self.View.TableSectionStudentLoadingScreen.run)
        self.AddItem.operation.connect(self.go_back_student)
        items = self.View.verticalLayout_38.count()-1
        self.AddItem.operation.connect(lambda: self.Admin.set_admin_status(f"{items} students added successfully"))
        self.AddItem.error.connect(self.student_bulk_error)
        self.AddItem.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        self.AddItem.start()

    def student_bulk_error(self):
        self.View.run_popup(
            f"Student creation error\nAlready existing or blank", 'warning')
        self.get_all_student_handler = self.GetAllStudents()
        self.get_all_section_student_handler = self.GetAllSectionStudents()

        if self.TargetSection:
            self.get_all_section_student_handler = self.GetAllSectionStudents()
            self.get_all_student_handler.finished.connect(
                self.get_all_section_student_handler.start)
            self.get_all_section_student_handler.val = self.TargetSection,
            self.get_all_section_student_handler.finished.connect(
                self.View.btn_cancel_section.click)

        self.get_all_student_handler.start()

    def combobox_index_changed(self, index):
        sections_model = self.View.tv_sections.model()
        self.set_target_section(self.Model.Section(
            *sections_model.getRowData(index)))
        index = sections_model.createIndex(index, 0)
        self.table_section_clicked(index)

    def go_back_student(self):
        self.View.sw_student_section.setCurrentIndex(0)
        self.get_all_student_handler = self.GetAllStudents()

        if self.TargetSection:
            self.get_all_section_student_handler = self.GetAllSectionStudents()
            self.get_all_student_handler.finished.connect(
                self.get_all_section_student_handler.start)
            self.get_all_section_student_handler.val = self.TargetSection,
            self.get_all_section_student_handler.finished.connect(
                self.View.btn_cancel_section.click)
        else:
            self.get_all_student_handler.finished.connect(
                self.get_latest_student)

        self.get_all_student_handler.start()

    def search_student(self):
        target_student = self.View.txt_search_student.text()
        if target_student.lower() == "null":
            return
        student_model = self.View.tv_students.model()
        students = student_model.getColumn(1)
        target_indices = []
        for index, student in enumerate(students):
            if target_student in student:
                target_indices.append(index)
            self.View.tv_students.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.tv_students.setRowHidden(target_index, False)

        self.View.txt_search_student.clear()

    def reset_target_student(self):
        self.TargetStudent = None

    # Student Operations
    def GetTargetStudentSection(self):
        handler = GetTargetStudentSection(
            self.Model.get_student_section, self.Model.get_all_section_student)
        handler.operation.connect(
            self.get_target_student_section)
        handler.operation.connect(
            self.View.enable_section_student_delete_clear
        )
        handler.operation.connect(
            self.View.enable_section_edit_delete)
        handler.validation.connect(
            self.empty_section_student_list
        )
        handler.validation.connect(
            self.View.tv_sections.clearSelection
        )
        handler.validation.connect(
            self.View.clear_section_inputs
        )
        handler.validation.connect(
            self.View.disable_section_edit_delete
        )
        handler.validation.connect(
            self.reset_target_section
        )
        handler.validation.connect(
            self.View.disable_section_student_delete_clear
        )
        handler.validation.connect(
            lambda: self.View.lbl_section_students_status.setText(
                'Students: 0')
        )
        handler.validation.connect(
            lambda: self.View.btn_init_add_section.setDisabled(True)
        )
        handler.validation.connect(
            lambda: self.View.btn_init_add_section_student.setDisabled(True)
        )
        return handler

    def GetAllStudents(self):
        handler = Get(self.Model.get_all_student)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.operation.connect(self.set_student_table)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def GetAllSectionStudents(self):
        handler = Get(self.Model.get_all_section_student)
        handler.finished.connect(self.View.SectionStudentLoadingScreen.run)
        handler.operation.connect(self.set_section_student_list)
        handler.finished.connect(self.View.SectionStudentLoadingScreen.hide)
        return handler

    def AddStudent(self):
        handler = Operation(self.Model.create_student)
        handler.started.connect(self.View.StudentLoadingScreen.run)
        handler.error.connect(self.student_error)
        handler.finished.connect(self.View.StudentLoadingScreen.hide)
        return handler

    def EditStudent(self):
        handler = Operation(self.Model.edit_student)
        handler.started.connect(self.View.StudentLoadingScreen.run)
        handler.error.connect(self.student_error)
        handler.finished.connect(self.View.StudentLoadingScreen.hide)
        return handler

    def DeleteStudent(self):
        handler = Operation(self.Model.delete_student)
        handler.started.connect(self.View.StudentLoadingScreen.run)
        handler.finished.connect(self.View.StudentLoadingScreen.hide)
        return handler

    def DeleteManyStudent(self):
        handler = Operation(self.Model.delete_many_students)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def tv_students_mouse_press(self, event):
        if event.button() == 2:
            if self.View.tv_students.selectionModel().selectedRows():
                self.View.show_menu(
                    self.init_delete_many_section, self.View.tv_students.mapToGlobal(event.pos()))
        super(QTableView, self.View.tv_students).mousePressEvent(event)

    def tv_students_key_pressed(self, event):
        if event.key() == 16777223:
            self.init_delete_many_student()

        super(QTableView, self.View.tv_students).keyPressEvent(event)

    def init_delete_many_student(self):
        self.View.show_confirm(self.delete_many_student)

    def delete_many_student(self):
        indices = self.View.tv_students.selectionModel().selectedRows()
        indices = [index.row() for index in indices]
        target_students = [[self.View.tv_students.model().getRowData(index)[
            0]] for index in indices]

        self.get_all_student_handler = self.GetAllStudents()
        self.delete_many_student_handler = self.DeleteManyStudent()

        self.delete_many_student_handler.val = target_students,
        self.delete_many_student_handler.operation.connect(
            self.get_all_student_handler.start)

        if self.TargetSection:
            self.get_all_section_student_handler = self.GetAllSectionStudents()
            self.get_all_section_student_handler.val = self.TargetSection,
            self.get_all_student_handler.finished.connect(
                self.get_all_section_student_handler.start)
            self.get_all_section_student_handler.finished.connect(
                self.get_latest_section_student)
        self.get_all_student_handler.finished.connect(
            self.View.btn_cancel_section.click)
        self.get_all_student_handler.finished.connect(lambda: self.Admin.set_admin_status(f"{len(target_students)} students deleted successfully"))
        self.delete_many_student_handler.start()

        self.View.txt_student_username.clear()
        self.View.txt_student_password.operation.emit()

    # Table
    def table_student_clicked(self, index):
        row = index.row()
        student_model = self.View.tv_students.model()

        if row == student_model.rowCount() - 1:
            self.View.btn_init_add_student.click()
            return

        self.View.enable_student_buttons()
        self.TargetStudent = self.Model.Student(
            *student_model.getRowData(row))
        self.target_student_row = row
        self.set_student_inputs()

        if self.View.student_state == 'Add' or self.View.student_state == 'Edit':
            self.View.btn_cancel_student.click()
            return

        self.get_target_student_section_handler = self.GetTargetStudentSection()
        self.get_target_student_section_handler.value = self.TargetStudent,
        self.get_target_student_section_handler.start()

    def get_target_student_section(self, Section, sectionstudents):
        if Section and sectionstudents:
            for sectionstudent in sectionstudents:
                if sectionstudent.Student == self.TargetStudent.Username:
                    target_section_student = sectionstudent
                    break
            self.set_target_section(Section)
            self.set_section_student_list(sectionstudents)
            self.View.lbl_section_students_status.setText(
                f'Students: {len(sectionstudents)}')
            self.set_target_section_student(target_section_student)

    def set_target_student(self, Student):
        self.TargetStudent = Student
        self.select_target_student_row()

    def select_target_student_row(self):
        try:
            student_model = self.View.tv_students.model()
            self.target_student_row = student_model.findRow(
                self.TargetStudent.Username)
            self.View.tv_students.selectRow(self.target_student_row)
            self.set_student_inputs()
        except (AttributeError, TypeError):
            self.View.disable_student_edit_delete()
            return

    def set_student_inputs(self):
        self.View.txt_student_username.setText(self.TargetStudent.Username)
        self.View.txt_student_password.setText(
            str(self.TargetStudent.Salt + self.TargetStudent.Hash))
        self.View.txt_student_password.setCursorPosition(0)

    def set_student_table(self, students):
        if not students:
            self.View.disable_section_edit_delete()
            self.View.clear_student_inputs()
            self.empty_section_student_list()
        else:
            self.View.enable_section_edit_delete()

        student_model = self.Model.TableModel(
            self.View.tv_students, students, self.Model.Student.get_headers())
        self.View.tv_students.setModel(student_model)
        self.View.tv_students.horizontalHeader().setMinimumSectionSize(150)
        self.View.lbl_students_table_status.setText(
            f'Students: {len(students)}')

        if self.View.tv_sections.model().rowCount() == 1:
            self.get_latest_student()

    def select_latest_student(self, username):
        student_model = self.View.tv_students.model()
        self.set_target_student(self.Model.Student(
            *student_model.getRowData(student_model.findRow(username))))

    def get_latest_student(self):
        student_model = self.View.tv_students.model()
        if student_model.rowCount() != 1:
            self.set_target_student(self.Model.Student(
                *student_model.getRowData(student_model.rowCount()-2)))

    def get_latest_section_student(self):
        try:
            section_model = self.View.lv_section_student.model()
            self.set_target_section_student(self.Model.SectionStudent(
                None, self.TargetSection.Name, section_model.getData()[0]))
            student_model = self.View.tv_students.model()
            self.set_target_student(self.Model.Student(
                *student_model.getRowData(student_model.findRow(self.TargetSectionStudent.Student))))
        except IndexError:
            self.View.clear_student_inputs()

    # Buttons
    def init_add_student(self):
        self.View.tv_students.clearSelection()
        self.View.clear_student_inputs()
        self.View.disable_student_buttons()
        self.View.enable_student_inputs()
        self.View.set_student('Add')
        self.View.tv_students.clearSelection()
        self.View.lv_section_student.clearSelection()
        self.View.txt_student_username.setFocus(True)

    def init_edit_student(self):
        self.View.disable_student_buttons()
        self.View.enable_student_inputs()
        self.View.set_student('Edit')

    def cancel_student(self):
        self.View.enable_student_buttons()
        self.View.disable_student_inputs()
        self.View.set_student('Read')
        if self.View.tv_sections.model().rowCount() == 1:
            self.get_latest_student()
        if not self.TargetStudent:
            self.View.disable_student_edit_delete()
            if len(self.View.tv_students.model().data) != 1:
                self.target_student_row = self.View.tv_students.model().rowCount() - 2
        if len(self.View.tv_students.model().data) != 1:
            index = self.View.tv_students.model().createIndex(self.target_student_row, 0)
            self.table_student_clicked(index)
            self.View.tv_students.selectRow(self.target_student_row)

    def init_add_edit_student(self):
        if self.View.student_state == "Add":
            self.add_student()
        elif self.View.student_state == "Edit":
            self.edit_student()

    # Student Error
    def student_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'Student exists')
        elif error == "section exists":
            self.View.run_popup(f'Student already in section')

    # Student Add
    def add_student(self):
        username = self.View.txt_student_username.text()
        password = self.View.txt_student_password.text()
        if is_blank(username) or is_blank(password):
            self.View.run_popup('Student fields must be filled')
            return

        self.get_all_student_handler = self.GetAllStudents()
        self.add_student_handler = self.AddStudent()

        if self.TargetSection:
            self.get_all_section_student_handler = self.GetAllSectionStudents()
            self.add_student_handler.val = self.TargetSection.Name, username, password
            self.get_all_student_handler.finished.connect(
                self.get_all_section_student_handler.start)
        else:
            self.add_student_handler.val = "", username, password
        self.add_student_handler.operation.connect(
            self.get_all_student_handler.start)
        self.get_all_student_handler.finished.connect(
            lambda: self.select_latest_student(username))
        self.get_all_student_handler.finished.connect(
            self.View.btn_cancel_student.click)
        self.get_all_student_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Student {username} added successfully"))

        if self.TargetSection:
            self.get_all_section_student_handler.val = self.TargetSection,
            self.get_all_section_student_handler.finished.connect(lambda: self.set_target_section_student(
                self.Model.SectionStudent(None, self.TargetSection.Name, username)))
        self.add_student_handler.start()

    # Student Edit
    def edit_student(self):
        username = self.View.txt_student_username.text()
        password = self.View.txt_student_password.text()

        if is_blank(username) or is_blank(password):
            self.View.run_popup('Student fields must be filled')
            return

        prev = self.TargetStudent.Username
        new = None
        if username != self.TargetStudent.Username:
            new = username

        if username == self.TargetStudent.Username and password == str(self.TargetStudent.Salt + self.TargetStudent.Hash):
            self.View.btn_cancel_student.click()
            return

        self.get_all_student_handler = self.GetAllStudents()
        self.edit_student_handler = self.EditStudent()

        self.edit_student_handler.val = self.TargetStudent.UserID, prev, username, self.TargetStudent.Salt, self.TargetStudent.Hash, password
        self.edit_student_handler.operation.connect(
            self.get_all_student_handler.start)

        if self.TargetSection:
            self.get_all_section_student_handler = self.GetAllSectionStudents()
            self.get_all_section_student_handler.val = self.TargetSection,
            self.get_all_section_student_handler.finished.connect(lambda: self.set_target_section_student(
                self.Model.SectionStudent(None, self.TargetSection.Name, username)))
            self.get_all_student_handler.finished.connect(
                self.get_all_section_student_handler.start)

        self.get_all_student_handler.finished.connect(
            lambda: self.select_latest_student(username))
        self.get_all_student_handler.finished.connect(
            self.View.btn_cancel_student.click)
        if new:
            self.get_all_student_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Student {prev} updated to {new} successfully"))
        else:
            self.get_all_student_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Student {prev} successfully"))
        self.edit_student_handler.start()
    
    # Student Delete
    def init_delete_student(self):
        self.View.show_confirm(self.delete_student)

    def delete_student(self):
        self.get_all_student_handler = self.GetAllStudents()
        self.delete_student_handler = self.DeleteStudent()
        target = self.TargetStudent

        self.delete_student_handler.val = self.TargetStudent,
        self.delete_student_handler.operation.connect(
            self.get_all_student_handler.start)

        if self.TargetSection:
            self.get_all_section_student_handler = self.GetAllSectionStudents()
            self.get_all_section_student_handler.val = self.TargetSection,
            self.get_all_student_handler.finished.connect(
                self.get_all_section_student_handler.start)
            self.get_all_section_student_handler.finished.connect(
                self.get_latest_section_student)
        self.get_all_student_handler.finished.connect(
            self.View.btn_cancel_section.click)
        self.get_all_student_handler.finished.connect(lambda: self.Admin.set_admin_status(f"Student {target.Username} deleted successfully"))
        self.delete_student_handler.start()

        self.View.txt_student_username.clear()
        self.View.txt_student_password.operation.emit()
