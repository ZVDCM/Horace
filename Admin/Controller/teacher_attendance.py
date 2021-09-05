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
       
    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)

    def set_teacher_table(self, teachers):
        teacher_model = self.Model.TableModel(self.View.tv_teachers, teachers, self.Model.Teacher.get_headers())
        self.View.tv_teachers.setModel(teacher_model)
        self.View.tv_teachers.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_teachers.setFocus(True)
