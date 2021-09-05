class TeacherAttendance:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.target_teacher_row = None
        self.TargetTeacher = None

        self.connect_signals()

    def connect_signals(self):
        pass
       
    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)

    def set_teacher_table(self, teachers):
        teacher_model = self.Model.TableModel(self.View.tv_teachers, teachers, self.Model.Teacher.get_headers())
        self.View.tv_teachers.setModel(teacher_model)
        self.View.tv_teachers.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_teachers.setFocus(True)
