from Admin.Misc.Widgets.data_table import DataTable
from PyQt5.QtWidgets import QDialog
from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore

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
    error = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = ()

    def run(self):
        successful = self.fn(*self.val)
        if successful:
            self.operation.emit()
        else:
            self.error.emit()
        self.quit()

class SectionStudent:

    def __init__(self, Model, View, Admin):
        self.Model = Model
        self.View = View
        self.Admin = Admin

        self.target_section_row = None
        self.TargetSection = None
        self.target_student_row = None
        self.TargetStudent = None
        self.target_section_student_row = None
        self.TargetSectionStudent = None

        # self.connect_signals()

    # def connect_signals(self):
    #     self.section_signals()
    #     self.section_operations()
    #     self.student_signals()
    #     self.student_operations()

    # def section_signals(self):
    #     self.View.btn_init_section_bulk.clicked.connect(
    #         lambda: self.change_table_bulk(self.View.sw_student_section, 2)
    #     )
    #     self.View.btn_back_section_bulk.clicked.connect(
    #         lambda: self.change_table_bulk(self.View.sw_student_section, 0)
    #     )

    #     # Table
    #     self.View.tv_sections.clicked.connect(self.tables_section_row_clicked)

    #     self.View.btn_init_add_section_student.clicked.connect(lambda: self.run_data_table("Students", 1, self.View.tv_students.model()))

    # def section_operations(self):
    #     self.get_section_student = Get(self.Model.get_section_student)
    #     self.get_section_student.started.connect(self.View.StudentLoadingScreen.run)
    #     self.get_section_student.operation.connect(self.set_target_section_student)
    #     self.get_section_student.finished.connect(self.View.StudentLoadingScreen.hide)
        
    #     self.get_all_section_student = Get(self.Model.get_all_section_student)
    #     self.get_all_section_student.started.connect(self.View.SectionStudentLoadingScreen.run)
    #     self.get_all_section_student.operation.connect(self.set_target_section_students)
    #     self.get_all_section_student.finished.connect(self.View.SectionStudentLoadingScreen.hide)

    #     self.get_section_student.operation.connect(self.get_all_section_student.start)

    #     self.register_section_student = Operation(self.Model.register_student_section)
    #     self.register_section_student.started.connect(self.View.SectionStudentLoadingScreen.run)
    #     self.register_section_student.finished.connect(self.View.SectionStudentLoadingScreen.hide)


    # def student_signals(self):
    #     self.View.btn_init_student_bulk.clicked.connect(
    #         lambda: self.change_table_bulk(self.View.sw_student_section, 1)
    #     )
    #     self.View.btn_back_student_bulk.clicked.connect(
    #         lambda: self.change_table_bulk(self.View.sw_student_section, 0)
    #     )

    # def student_operations(self):
    #     pass

    # def change_table_bulk(self, target, index):
    #     target.setCurrentIndex(index)

    # def tables_section_row_clicked(self, item):
    #     index = item.row()
    #     section_model = self.View.tv_sections.model()
    #     if index == section_model.rowCount() - 1:
    #         self.View.btn_init_add_section.click()
    #         return

    #     if self.View.section_state == "add" or self.View.section_state == "edit":
    #         self.View.btn_cancel_section.click()

    #     self.target_section_row = index
    #     self.set_target_section(self.Model.Section(
    #         *section_model.getRowData(self.target_section_row)))
    #     self.set_section_input_values()
        
    #     self.get_section_student.val = self.TargetSection,
    #     self.get_all_section_student.val = self.TargetSection,
    #     self.get_section_student.start()

    # def set_target_section(self, Section):
    #     self.TargetSection = Section

    # def set_section_input_values(self):
    #     self.View.txt_section_name.setText(self.TargetSection.Name)

    # def set_target_section_student(self, student):
    #     student_model = self.View.tv_students.model()
    #     student = student[2]
    #     self.target_student_row = student_model.findRow(student)
    #     self.View.tv_students.selectRow(self.target_student_row)
    #     self.TargetStudent = self.Model.Student(*student_model.getRowData(self.target_student_row))
    #     self.set_target_section_student_input()

    # def set_target_section_student_input(self):
    #     self.View.txt_student_username.setText(self.TargetStudent.Username)
    #     self.View.txt_student_password.setText(str(self.TargetStudent.Salt + self.TargetStudent.Hash))
    #     self.View.txt_student_password.setCursorPosition(0)

    # def set_target_section_students(self, students):
    #     section_student_model = self.Model.ListModel(self.View.lv_section_student, students)
    #     self.View.lv_section_student.setModel(section_student_model)
    #     index = section_student_model.createIndex(0,0)
    #     self.View.lv_section_student.setCurrentIndex(index)

    # def run_data_table(self, target_table, target_column, table_model):
    #     self.DataTable = DataTable(self.View, target_table, target_column, table_model)
    #     table_model.parent = self.DataTable.tv_target_data
    #     self.DataTable.btn_set.clicked.connect(self.add_data_table_section_student)
    #     self.DataTable.run()

    # def add_data_table_section_student(self):
    #     table_model = self.DataTable.tv_target_data.model()
    #     Student = self.Model.Student(*table_model.getRowData(self.DataTable.target_row))
    #     section = self.View.txt_section_name.text()

    #     self.register_section_student.val = section, Student.Username
    #     self.register_section_student.operation.connect(self.get_all_section_student.start)
    #     self.register_section_student.operation.connect(lambda: self.View.set_database_status(f"Student {Student.Username} is registered to {section} successfully"))
    #     self.get_all_section_student.val = self.TargetSection,
    #     self.register_section_student.error.connect(lambda: self.View.run_popup(f"Student {Student.Username} is already registered to {section}", "warning"))
    #     self.register_section_student.error.connect(lambda: self.View.set_database_status(f"Student {Student.Username} is already registered to {section}"))

    #     self.register_section_student.start()
    #     self.DataTable.close()

    def select_target_section_row(self):
        section_model = self.View.tv_sections.model()
        self.target_section_row = section_model.findRow(self.TargetSection.Name)
        self.View.tv_section.selectRow(self.target_section_row)

        self.View.txt_section_name.setText(self.TargetSection.Name)

    def select_target_student_row(self):
        student_model = self.View.tv_students.model()
        self.target_student_row = student_model.findRow(self.TargetStudent.Username)
        self.View.tv_students.selectRow(self.target_student_row)

        self.View.txt_student_username.setText(self.TargetStudent.Username)
        self.View.txt_student_password.setText(str(self.TargetStudent.Salt + self.TargetStudent.Hash))
        self.View.txt_student_password.setCursorPosition(0)

    def select_target_section_row(self):
        section_student_model = self.View.lv_section_student.model()
        self.target_section_student_row = section_student_model.createIndex(section_student_model.findRow(self.TargetStudentSection.Student), 0)
        self.View.lv_section_student.setCurrentIndex(self.target_section_student_row)