
class StudentSection:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.connect_signals()

    def connect_signals(self):
        # Student
        self.View.btn_init_student_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 1)
        )

        self.View.btn_back_student_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 0)
        )

        # Add
        self.View.btn_init_add_student.clicked.connect(self.View.disable_student_buttons)
        self.View.btn_init_add_student.clicked.connect(self.View.enable_student_inputs)
        self.View.btn_init_add_student.clicked.connect(self.View.w_student_btn.show)

        # Edit
        
        # Cancel
        self.View.btn_cancel_student.clicked.connect(self.View.w_student_btn.hide)
        self.View.btn_cancel_student.clicked.connect(self.View.disable_student_inputs)
        self.View.btn_cancel_student.clicked.connect(self.View.enable_student_buttons)
        
        # Section
        self.View.btn_init_section_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 2)
        )

        self.View.btn_back_section_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_student_section, 0)
        )

        # Add
        self.View.btn_init_add_section.clicked.connect(self.View.disable_section_buttons)
        self.View.btn_init_add_section.clicked.connect(self.View.enable_section_inputs)
        self.View.btn_init_add_section.clicked.connect(self.View.w_section_btn.show)

        # Edit
        
        # Cancel
        self.View.btn_cancel_section.clicked.connect(self.View.w_section_btn.hide)
        self.View.btn_cancel_section.clicked.connect(self.View.disable_section_inputs)
        self.View.btn_cancel_section.clicked.connect(self.View.enable_section_buttons)

    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)
