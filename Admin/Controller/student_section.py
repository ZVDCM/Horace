from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore

class GetUser(QtCore.QThread):
    operation = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        res = self.fn(self.val)
        self.operation.emit(res)
        self.quit()



class StudentSection:

    def __init__(self, Model, View, Contoller):
        self.Model = Model.StudentSection
        self.View = View
        self.Contoller = Contoller

        self.connect_signals()

    def connect_signals(self):
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

        self.get_section = GetUser(self.Model.get_section)

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

    def add_section(self, name):
        pass

    def edit_section_input(self):
        name = self.View.txt_section_name.text()
        if is_blank(name):
            self.View.run_popup("Section fields must be filled")
            return

    def edit_section(self, name):
        pass