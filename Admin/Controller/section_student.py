from Admin.Misc.Functions.password import generate_password
from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore

class Get(QtCore.QThread):
    operation = QtCore.pyqtSignal()
    validation = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        is_exist = self.fn(self.val)
        if not is_exist:
            self.operation.emit()
        else:
            self.validation.emit()
        self.quit()

class SectionOperation(QtCore.QThread):
    operation = QtCore.pyqtSignal(list)

    def __init__(self, fn, re):
        super().__init__()
        self.fn = fn
        self.val = None
        self.re = re

    def run(self):
        self.fn(self.val)
        res = self.re()
        if res:
            self.operation.emit(res)
        self.quit()

class ValidateStudentSection(QtCore.QThread):
    operation = QtCore.pyqtSignal()
    validation = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        is_exist = self.fn(self.val)
        if is_exist:
            self.operation.emit()
        else:
            self.validation.emit()
        self.quit()

class StudentOperation(QtCore.QThread):
    operation = QtCore.pyqtSignal(list)

    def __init__(self, fn, re):
        super().__init__()
        self.fn = fn
        self.val = ()
        self.re = re

    def run(self):
        self.fn(*self.val)
        res = self.re()
        if res:
            self.operation.emit(res)
        self.quit()

class Register(QtCore.QThread):

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = ()

    def run(self):
        self.fn(*self.val)
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

        self.connect_signals()

    def connect_signals(self):
        self.section_signals()
        self.section_operations()
        self.student_signals()
        self.student_operations()

    def section_signals(self):
        self.View.btn_add_edit_section.clicked.connect(self.add_edit_section)

        self.View.btn_init_section_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 2)
        )

        self.View.btn_back_section_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 0)
        )

        # Add
        self.View.btn_init_add_section.clicked.connect(
            lambda: self.View.set_section("add"))
        self.View.btn_init_add_section.clicked.connect(
            self.View.disable_section_buttons)
        self.View.btn_init_add_section.clicked.connect(
            self.View.clear_section_inputs)
        self.View.btn_init_add_section.clicked.connect(
            self.View.enable_section_inputs)
        self.View.btn_init_add_section.clicked.connect(
            lambda: self.View.btn_add_edit_section.setText("Add"))
        self.View.btn_init_add_section.clicked.connect(
            self.View.w_section_btn.show)

        # Edit
        self.View.btn_init_edit_section.clicked.connect(
            lambda: self.View.set_section("edit"))
        self.View.btn_init_edit_section.clicked.connect(
            self.View.disable_section_buttons)
        self.View.btn_init_edit_section.clicked.connect(
            self.View.enable_section_inputs)
        self.View.btn_init_edit_section.clicked.connect(
            lambda: self.View.btn_add_edit_section.setText("Edit"))
        self.View.btn_init_edit_section.clicked.connect(
            self.View.w_section_btn.show)

        # Delete
        self.View.btn_delete_section.clicked.connect(self.delete_section_input)

        # Cancel
        self.View.btn_cancel_section.clicked.connect(
            lambda: self.View.set_section("read"))
        self.View.btn_cancel_section.clicked.connect(
            self.View.w_section_btn.hide)
        self.View.btn_cancel_section.clicked.connect(
            self.View.disable_section_inputs)
        self.View.btn_cancel_section.clicked.connect(
            self.set_section_input_values)
        self.View.btn_cancel_section.clicked.connect(
            self.View.enable_section_buttons)

        # Table
        self.View.tv_sections.clicked.connect(self.section_table_row_clicked)
    
    def section_operations(self):
        self.get_section = Get(self.Model.get_section)
        self.get_section.started.connect(self.View.SectionLoadingScreen.run)
        self.get_section.validation.connect(
            self.View.SectionLoadingScreen.hide)

        self.add_section = SectionOperation(self.Model.create_section, self.Model.get_all_section)
        self.add_section.operation.connect(self.reload_section_table)
        self.add_section.finished.connect(self.View.SectionLoadingScreen.hide)
        self.add_section.finished.connect(self.View.btn_cancel_section.click)

        self.edit_section = SectionOperation(self.Model.edit_section, self.Model.get_all_section)
        self.edit_section.started.connect(self.View.SectionLoadingScreen.run)
        self.edit_section.operation.connect(self.reload_section_table)
        self.edit_section.finished.connect(self.View.SectionLoadingScreen.hide)
        self.edit_section.finished.connect(self.View.btn_cancel_section.click)

        self.delete_section = SectionOperation(self.Model.delete_section, self.Model.get_all_section)
        self.delete_section.started.connect(self.View.SectionLoadingScreen.run)
        self.delete_section.operation.connect(self.reload_section_table)
        self.delete_section.finished.connect(self.View.SectionLoadingScreen.hide)

    def student_signals(self):
        self.View.btn_add_edit_student.clicked.connect(self.add_edit_student)
        self.View.btn_init_student_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 1)
        )

        self.View.btn_back_student_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 0)
        )

        # Add
        self.View.btn_init_add_student.clicked.connect(
            lambda: self.View.set_student("add"))
        self.View.btn_init_add_student.clicked.connect(
            self.View.disable_student_buttons)
        self.View.btn_init_add_student.clicked.connect(
            self.View.clear_student_inputs)
        self.View.btn_init_add_student.clicked.connect(
            self.View.enable_student_inputs)
        self.View.btn_init_add_student.clicked.connect(
            lambda: self.View.set_password(self.View.txt_student_password))
        self.View.btn_init_add_student.clicked.connect(
            lambda: self.View.btn_add_edit_student.setText("Add"))
        self.View.btn_init_add_student.clicked.connect(
            self.View.w_student_btn.show)

        # Edit
        self.View.btn_init_edit_student.clicked.connect(
            lambda: self.View.set_student("edit"))
        self.View.btn_init_edit_student.clicked.connect(
            self.View.disable_student_buttons)
        self.View.btn_init_edit_student.clicked.connect(
            self.View.enable_student_inputs)
        self.View.btn_init_edit_student.clicked.connect(
            lambda: self.View.btn_add_edit_student.setText("Edit"))
        self.View.btn_init_edit_student.clicked.connect(
            self.View.w_student_btn.show)

        # Cancel
        self.View.btn_cancel_student.clicked.connect(
            lambda: self.View.set_student("read"))
        self.View.btn_cancel_student.clicked.connect(
            self.View.w_student_btn.hide)
        self.View.btn_cancel_student.clicked.connect(
            self.View.disable_student_inputs)
        self.View.btn_cancel_student.clicked.connect(
            self.View.txt_student_password.clear)
        self.View.btn_cancel_student.clicked.connect(
            self.View.enable_student_buttons)

        # Table
        self.View.tv_students.clicked.connect(self.student_table_row_clicked)

        self.View.btn_student_get_section.clicked.connect(lambda: self.View.run_data_table("Section", 1, self.View.txt_student_section ,self.View.tv_sections.model()))

    def student_operations(self):
        self.get_student_section = ValidateStudentSection(self.Model.get_section)
        self.get_student_section.started.connect(self.View.StudentLoadingScreen.run)

        self.get_student = Get(self.Model.get_student)

        self.add_student = StudentOperation(self.Model.create_student, self.Model.get_all_student)
        self.add_student.operation.connect(self.reload_student_table)

        self.register_student_section = Register(self.Model.register_student_section)
        self.register_student_section.finished.connect(self.View.StudentLoadingScreen.hide)
        self.register_student_section.finished.connect(self.View.btn_cancel_student.click)

        self.add_student.finished.connect(self.register_student_section.start)

    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)

    # Section
    def add_edit_section(self):
        if self.View.section_state == "add":
            self.add_section_input()
        else:
            self.edit_section_input()

    def add_section_input(self):
        name = self.View.txt_section_name.text()
        if is_blank(name):
            self.View.run_popup("Section fields must be filled")
            return

        self.get_section.val = name
        self.get_section.operation.connect(self.add_section.start)
        self.get_section.validation.connect(
            lambda: self.View.set_database_status(f'{name} exists'))
        self.get_section.validation.connect(
            lambda: self.View.run_popup(f'{name} exists', 'warning'))

        self.add_section.val = name
        self.add_section.finished.connect(
            lambda: self.View.set_database_status(f'{name} added successfully'))
        self.add_section.finished.connect(self.select_last_section_row)

        self.get_section.start()

    def edit_section_input(self):
        name = self.View.txt_section_name.text()
        if is_blank(name):
            self.View.run_popup("Section fields must be filled")
            return

        if name == self.TargetSection.Name:
            self.View.btn_cancel_section.click()
            self.View.set_database_status(f'No changes with {name}')
            return

        self.TargetSection.Name = name
        self.edit_section.val = self.TargetSection
        self.edit_section.finished.connect(
            lambda: self.View.set_database_status(f'{name} updated successfully'))
        self.edit_section.finished.connect(lambda: self.View.tv_sections.selectRow(self.target_section_row))
        self.edit_section.start()

    def delete_section_input(self):
        self.delete_section.val = self.TargetSection
        self.delete_section.finished.connect(lambda: self.View.set_database_status(
            f'{self.TargetSection.Name} deleted successfully'))
        self.delete_section.finished.connect(self.select_last_section_row)
        self.delete_section.start()

    def reload_section_table(self, sections):
        section_model = self.Model.TableModel(
            self.View.tv_sections, sections, self.Model.Section.get_headers())
        self.View.tv_sections.setModel(section_model)
        self.View.tv_sections.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_sections.setFocus(True)
       
    def select_last_section_row(self):
        section_model = self.View.tv_sections.model()
        self.target_section_row = section_model.rowCount() - 2
        self.View.tv_sections.selectRow(self.target_section_row)
        self.set_target_section(self.Model.Section(
            *section_model.getRowData(self.target_section_row)))
        self.set_section_input_values()

    def section_table_row_clicked(self, item):
        index = item.row()
        section_model = self.View.tv_sections.model()
        if index == section_model.rowCount() - 1:
            self.View.btn_init_add_section.click()
            return
        
        if self.View.section_state == "add" or self.View.section_state == "edit":
            self.View.btn_cancel_section.click()

        self.target_section_row = index
        self.set_target_section(self.Model.Section(
            *section_model.getRowData(self.target_section_row)))
        self.set_section_input_values()

    def set_target_section(self, new_section):
        self.TargetSection = new_section

    def set_section_input_values(self):
        try:
            self.View.txt_section_name.setText(self.TargetSection.Name)
        except AttributeError:
            return

    # Student
    def add_edit_student(self):
        if self.View.student_state == "add":
            self.add_student_input()
        else:
            self.edit_student_input()

    def add_student_input(self):
        username = self.View.txt_student_username.text()
        section = self.View.txt_student_section.text()
        password = self.View.txt_student_password.text()
        if is_blank(username) or is_blank(section) or is_blank(password):
            self.View.run_popup("Student fields must be filled")
            return

        self.get_student_section.val = section
        self.get_student_section.operation.connect(self.get_student.start)
        self.get_student_section.validation.connect(lambda: self.View.run_popup(f'{section} does not exist', 'warning'))
        self.get_student_section.validation.connect(self.View.StudentLoadingScreen.hide)
        self.get_student_section.finished.connect(
            lambda: self.View.set_database_status(f'{username} creation failed')
        )
        
        self.get_student.val = username
        self.get_student.operation.connect(self.add_student.start)
        self.get_student.validation.connect(
            lambda: self.View.set_database_status(f'{username} exists'))
        self.get_student.validation.connect(
            lambda: self.View.run_popup(f'{username} exists', 'warning'))

        self.add_student.val = username, password
        self.add_student.finished.connect(
            lambda: self.View.set_database_status(f'{username} added successfully'))

        self.register_student_section.val = section, username
        self.register_student_section.finished.connect(
            lambda: self.View.set_database_status(f'{username} added to {section}'))
        self.register_student_section.finished.connect(self.select_last_student_row)
        
        self.get_student_section.start()

    def edit_student_input(self):
        print(2)

    def reload_student_table(self, students):
        student_model = self.Model.TableModel(
            self.View.tv_students, students, self.Model.Student.get_headers())
        self.View.tv_students.setModel(student_model)
        self.View.tv_students.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_students.setFocus(True)

    def student_table_row_clicked(self, item):
        index = item.row()
        student_model = self.View.tv_students.model()
        if index == student_model.rowCount() - 1:
            self.View.btn_init_add_student.click()
            return
        
        if self.View.student_state == "add" or self.View.student_state == "edit":
            self.View.btn_cancel_student.click()

        self.target_student_row = index
        self.set_target_student(self.Model.Student(
            *student_model.getRowData(self.target_student_row)))
        self.set_student_input_values()

    def select_last_student_row(self):
        student_model = self.View.tv_students.model()
        self.target_student_row = student_model.rowCount() - 2
        self.View.tv_students.selectRow(self.target_student_row)
        self.set_target_student(self.Model.Student(
            *student_model.getRowData(self.target_student_row)))
        self.set_student_input_values()

    def set_target_student(self, new_student):
        self.TargetStudent = new_student

    def set_student_input_values(self):
        self.View.txt_student_username.setText(self.TargetStudent.Username)
        self.View.txt_student_password.setText(str(self.TargetStudent.Salt + self.TargetStudent.Hash))
        self.View.txt_student_password.setCursorPosition(0)