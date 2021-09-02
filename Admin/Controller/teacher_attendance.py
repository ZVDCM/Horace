class TeacherAttendance:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.connect_signals()

    def connect_signals(self):
        self.View.btn_init_teachers_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_teacher_attendance, 1)
        )

        self.View.btn_back_teacher_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_teacher_attendance, 0)
        )
        
        # Add
        self.View.btn_init_add_teacher.clicked.connect(self.View.disable_teacher_buttons)
        self.View.btn_init_add_teacher.clicked.connect(self.View.enable_teacher_inputs)
        self.View.btn_init_add_teacher.clicked.connect(self.View.w_teacher_btn.show)

        # Edit
        
        # Cancel
        self.View.btn_cancel_teacher.clicked.connect(self.View.w_teacher_btn.hide)
        self.View.btn_cancel_teacher.clicked.connect(self.View.disable_teacher_inputs)
        self.View.btn_cancel_teacher.clicked.connect(self.View.enable_teacher_buttons)

    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)