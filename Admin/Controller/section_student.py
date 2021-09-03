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

class Create(QtCore.QThread):

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        self.fn(self.val)
        self.quit()


class SectionStudent:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.connect_signals()

    def connect_signals(self):
        # Section
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
        self.View.btn_cancel_section.clicked.connect(self.View.enable_section_buttons)

        # Student
        self.View.btn_add_edit_student.clicked.connect(self.add_edit_student)

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
        
        self.get_section = Get(self.Model.get_section)
        self.get_section.started.connect(self.View.SectionLoadingScreen.show)
        self.get_section.validation.connect(self.View.SectionLoadingScreen.hide)

        self.add_section =  Create(self.Model.create_section)
        self.add_section.finished.connect(self.View.SectionLoadingScreen.hide)
        self.add_section.finished.connect(self.View.btn_cancel_section.click)

    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)

    # Student
    def add_edit_student(self):
        if self.View.student_state == "add":
            self.add_student()
        else:
            self.edit_student()

    def add_student(self):
        pass

    def edit_student(self):
        pass

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