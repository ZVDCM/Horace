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


class TeacherAttendance:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.target_teacher_row = None
        self.TargetTeacher = None

        self.connect_signals()

    def connect_signals(self):
        self.View.tv_teachers.clicked.connect(self.table_teacher_clicked)
        self.View.btn_init_add_teacher.clicked.connect(self.init_add_teacher)
        self.View.btn_init_edit_teacher.clicked.connect(self.init_edit_teacher)
        self.View.btn_add_edit_teacher.clicked.connect(
            self.init_add_edit_teacher)
        self.View.btn_cancel_teacher.clicked.connect(self.cancel_teacher)

    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)

    # Operations
    def GetAllTeacher(self):
        handler = Get(self.Model.get_all_teacher)
        handler.started.connect(self.View.TableTeacherLoadingScreen.run)
        handler.operation.connect(self.set_teacher_table)
        handler.finished.connect(self.View.TableTeacherLoadingScreen.hide)
        return handler

    def AddTeacher(self):
        handler = Operation(self.Model.create_teacher)
        handler.started.connect(self.View.TeacherLoadingScreen.run)
        handler.error.connect(self.teacher_error)
        handler.finished.connect(self.View.TeacherLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_teacher.click)
        return handler

    # Table
    def set_teacher_table(self, teachers):
        teacher_model = self.Model.TableModel(
            self.View.tv_teachers, teachers, self.Model.Teacher.get_headers())
        self.View.tv_teachers.setModel(teacher_model)
        self.View.tv_teachers.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_teachers.setFocus(True)

    def table_teacher_clicked(self, index):
        row = index.row()
        teacher_model = self.View.tv_teachers.model()
        if row == teacher_model.rowCount() - 1:
            return

        self.set_target_teacher(self.Model.Teacher(
            *teacher_model.getRowData(row)))

    def set_target_teacher(self, Teacher):
        self.TargetTeacher = Teacher
        self.select_target_teacher_row()

    def select_target_teacher_row(self):
        teacher_model = self.View.tv_teachers.model()
        self.target_teacher_row = teacher_model.findRow(
            self.TargetTeacher.Username)
        self.set_teacher_inputs()

    def set_teacher_inputs(self):
        self.View.txt_teacher_username.setText(self.TargetTeacher.Username)
        self.View.txt_teacher_password.setText(
            str(self.TargetTeacher.Salt + self.TargetTeacher.Hash))
        self.View.txt_teacher_password.setCursorPosition(0)

    def select_latest_teacher(self, teacher):
        teacher_model = self.View.tv_teachers.model()
        self.set_target_teacher(self.Model.Teacher(
            *teacher_model.getRowData(teacher_model.findRow(teacher))))

    # Buttons
    def init_add_teacher(self):
        self.View.clear_teacher_inputs()
        self.View.disable_teacher_buttons()
        self.View.enable_teacher_inputs()
        self.View.set_teacher('Add')

    def init_edit_teacher(self):
        self.View.disable_teacher_buttons()
        self.View.enable_teacher_inputs()
        self.View.set_teacher('Edit')

    def cancel_teacher(self):
        self.select_target_teacher_row()
        self.View.enable_teacher_buttons()
        self.View.disable_teacher_inputs()
        self.View.set_teacher('Read')

    def init_add_edit_teacher(self):
        if self.View.teacher_state == "Add":
            self.add_teacher()
        elif self.View.teacher_state == "Edit":
            self.edit_teacher()

    # Teacher Error
    def teacher_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'Teacher exists')

    def add_teacher(self):
        username = self.View.txt_teacher_username.text()
        password = self.View.txt_teacher_password.text()

        if is_blank(username) or is_blank(password):
            self.View.run_popup('Teacher fields must be filled')
            return
        
        self.get_all_teacher_handler = self.GetAllTeacher()
        self.add_teacher_handler = self.AddTeacher()

        self.add_teacher_handler.val = username, password
        self.add_teacher_handler.operation.connect(self.get_all_teacher_handler.start)

        self.get_all_teacher_handler.finished.connect(lambda: self.select_latest_teacher(username))
        self.add_teacher_handler.start()

    def edit_teacher(self):
        print(2)
