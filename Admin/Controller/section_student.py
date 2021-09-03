from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore

class GetAll(QtCore.QThread):
    operation = QtCore.pyqtSignal(list)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        res = self.fn()
        self.operation.emit(res)
        self.quit()

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

class Operation(QtCore.QThread):

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        self.fn(self.val)
        self.quit()


class SectionStudent:

    def __init__(self, Model, View, Admin):
        self.Model = Model
        self.View = View
        self.Admin = Admin

        self.target_section_row = None
        self.TargetSection = None
        self.TargetStudent = None
     
        self.connect_signals()

    def connect_signals(self):
        # ==Section
        self.View.btn_add_edit_section.clicked.connect(self.add_edit_section)

        self.View.btn_init_section_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 2)
        )

        self.View.btn_back_section_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 0)
        )

        # Add
        self.View.btn_init_add_section.clicked.connect(lambda: self.View.set_section("add"))
        self.View.btn_init_add_section.clicked.connect(self.View.disable_section_buttons)
        self.View.btn_init_add_section.clicked.connect(self.View.txt_section_name.clear)
        self.View.btn_init_add_section.clicked.connect(self.View.enable_section_inputs)
        self.View.btn_init_add_section.clicked.connect(lambda: self.View.btn_add_edit_section.setText("Add"))
        self.View.btn_init_add_section.clicked.connect(self.View.w_section_btn.show)

        # Edit
        self.View.btn_init_edit_section.clicked.connect(lambda: self.View.set_section("edit"))
        self.View.btn_init_edit_section.clicked.connect(self.View.disable_section_buttons)
        self.View.btn_init_edit_section.clicked.connect(self.View.enable_section_inputs)
        self.View.btn_init_edit_section.clicked.connect(lambda: self.View.btn_add_edit_section.setText("Edit"))
        self.View.btn_init_edit_section.clicked.connect(self.View.w_section_btn.show)

        # Cancel
        self.View.btn_cancel_section.clicked.connect(lambda: self.View.set_section("read"))
        self.View.btn_cancel_section.clicked.connect(self.View.w_section_btn.hide)
        self.View.btn_cancel_section.clicked.connect(self.View.disable_section_inputs)
        self.View.btn_cancel_section.clicked.connect(self.set_section_input_values)
        self.View.btn_cancel_section.clicked.connect(self.View.enable_section_buttons)

        # Table
        self.View.tv_sections.clicked.connect(self.section_table_row_clicked)

        # ==Student

        self.View.btn_init_student_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 1)
        )

        self.View.btn_back_student_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 0)
        )

        # Add
        self.View.btn_init_add_student.clicked.connect(lambda: self.View.set_student("add"))
        self.View.btn_init_add_student.clicked.connect(self.View.disable_student_buttons)
        self.View.btn_init_add_student.clicked.connect(self.View.enable_student_inputs)
        self.View.btn_init_add_student.clicked.connect(lambda: self.View.btn_add_edit_student.setText("Add"))
        self.View.btn_init_add_student.clicked.connect(self.View.w_student_btn.show)

        # Edit
        self.View.btn_init_edit_student.clicked.connect(lambda: self.View.set_student("edit"))
        self.View.btn_init_edit_student.clicked.connect(self.View.disable_student_buttons)
        self.View.btn_init_edit_student.clicked.connect(self.View.enable_student_inputs)
        self.View.btn_init_edit_student.clicked.connect(lambda: self.View.btn_add_edit_student.setText("Edit"))
        self.View.btn_init_edit_student.clicked.connect(self.View.w_student_btn.show)

        # Cancel
        self.View.btn_cancel_student.clicked.connect(lambda: self.View.set_student("read"))
        self.View.btn_cancel_student.clicked.connect(self.View.w_student_btn.hide)
        self.View.btn_cancel_student.clicked.connect(self.View.disable_student_inputs)
        self.View.btn_cancel_student.clicked.connect(self.View.enable_student_buttons)
        
        # Operations
        self.get_all_section = GetAll(self.Model.get_all_section)
        self.get_all_section.started.connect(self.View.SectionLoadingScreen.run)
        self.get_all_section.operation.connect(self.reload_section_table)
        self.get_all_section.finished.connect(self.View.SectionLoadingScreen.hide)

        self.get_section = Get(self.Model.get_section)
        self.get_section.started.connect(self.View.SectionLoadingScreen.run)
        self.get_section.validation.connect(self.View.SectionLoadingScreen.hide)

        self.add_section =  Operation(self.Model.create_section)
        self.add_section.finished.connect(self.View.SectionLoadingScreen.hide)
        self.add_section.finished.connect(self.View.btn_cancel_section.click)

        self.edit_section =  Operation(self.Model.edit_section)
        self.edit_section.started.connect(self.View.SectionLoadingScreen.run)
        self.edit_section.finished.connect(self.View.SectionLoadingScreen.hide)
        self.edit_section.finished.connect(self.View.btn_cancel_section.click)

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
        self.get_section.validation.connect(lambda: self.View.set_database_status(f'{name} exists'))
        self.get_section.validation.connect(lambda: self.View.run_popup(f'{name} exists', 'warning'))
        
        self.add_section.val = name
        self.add_section.finished.connect(lambda: self.View.set_database_status(f'{name} added successfully'))
        
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
        self.edit_section.finished.connect(self.get_all_section.start)
        self.edit_section.finished.connect(lambda: self.View.set_database_status(f'{name} updated successfully'))
        self.edit_section.start()

    def reload_section_table(self, sections):
        section_model = self.Model.TableModel(self.View.tv_sections, sections, self.Model.Section.get_headers())
        self.View.tv_sections.setModel(section_model)
        self.View.tv_sections.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_sections.setFocus(True)
        self.View.tv_sections.selectRow(self.target_section_row)

    def section_table_row_clicked(self, item):
        self.target_section_row = item.row()
        self.TargetSection = self.Model.Section(*self.View.tv_sections.model().getRowData(self.target_section_row))
        self.set_section_input_values()
        
    def set_target_section(self, new_section):
        self.TargetSection = new_section

    def set_section_input_values(self):
        self.View.txt_section_name.setText(self.TargetSection.Name)