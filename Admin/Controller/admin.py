from Admin.Model.model import Class
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from Admin.Controller.section_student import SectionStudent
from Admin.Controller.teacher_attendance import TeacherAttendance
from Admin.Controller.class_member import ClassMember
from Admin.Controller.blacklist_url import BlacklistURL

class GetAll(QtCore.QThread):
    section_operation = QtCore.pyqtSignal(list)
    student_operation = QtCore.pyqtSignal(list)
    teacher_operation = QtCore.pyqtSignal(list)
    class_operation = QtCore.pyqtSignal(list)

    def __init__(self, get_all_section, get_all_student, get_all_teacher, get_all_class):
        super().__init__()
        self.get_all_section = get_all_section
        self.get_all_student = get_all_student
        self.get_all_teacher = get_all_teacher
        self.get_all_class = get_all_class

    def run(self):
        res = self.get_all_section()
        self.section_operation.emit(res)
        res = self.get_all_student()
        self.student_operation.emit(res)
        res = self.get_all_teacher()
        self.teacher_operation.emit(res)
        res = self.get_all_class()
        self.class_operation.emit(res)
        self.quit()

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

class Admin:

    def __init__(self, Controller):
        self.Model = Controller.Model
        self.View = Controller.View.Admin
        self.Controller = Controller

        self.SectionStudent = SectionStudent(
            self.Model.SectionStudent, self.View, self)
        self.TeacherAttendance = TeacherAttendance(
            self.Model.TeacherAttendance, self.View, self)
        self.ClassMember = ClassMember(
            self.Model.ClassMember, self.View, self)
        self.BlacklistURL = BlacklistURL(
            self.Model, self.View, self)

        self.connect_signals()
        self.init_databases()

        self.View.run()

    def connect_signals(self):
        for side_nav in self.View.side_navs:
            side_nav.operation.connect(self.change_page)

        self.View.resizeEvent = self.resize

        self.get_all = GetAll(self.Model.SectionStudent.get_all_section, self.Model.SectionStudent.get_all_student, self.Model.TeacherAttendance.get_all_teacher, self.Model.ClassMember.get_all_class)
        self.get_all.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        self.get_all.started.connect(self.View.TableTeacherLoadingScreen.run)
        self.get_all.started.connect(self.View.TableClassLoadingScreen.run)
        self.get_all.section_operation.connect(self.SectionStudent.set_section_table)
        self.get_all.student_operation.connect(self.SectionStudent.set_student_table)
        self.get_all.teacher_operation.connect(self.TeacherAttendance.set_teacher_table)
        self.get_all.class_operation.connect(self.ClassMember.set_class_table)
        self.get_all.finished.connect(self.View.TableSectionStudentLoadingScreen.hide)
        self.get_all.finished.connect(self.View.TableTeacherLoadingScreen.hide)
        self.get_all.finished.connect(self.View.TableClassLoadingScreen.hide)
        self.get_all.finished.connect(self.get_model_latest_section)
        self.get_all.finished.connect(self.get_model_latest_teacher)
        self.get_all.finished.connect(self.get_model_latest_class)

        self.get_all_section_student = Get(self.Model.SectionStudent.get_all_section_student)
        self.get_all_section_student.started.connect(self.View.SectionStudentLoadingScreen.run)
        self.get_all_section_student.operation.connect(self.set_section_student_listview)
        self.get_all_section_student.finished.connect(self.View.SectionStudentLoadingScreen.hide)
        self.get_all_section_student.finished.connect(self.select_latest_targets)

    def change_page(self, index):
        for side_nav in self.View.side_navs:
            if side_nav.is_active:
                side_nav.deactivate()
                break
        self.View.side_navs[index].activate()
        self.View.sw_all.setCurrentIndex(index)

    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)

    def init_databases(self):
        self.get_all.start()

    # *SectionStudent
    def set_section_student_listview(self, students):
        section_student_model = self.Model.ListModel(self.View.lv_section_student, students)
        self.View.lv_section_student.setModel(section_student_model)
        index = section_student_model.createIndex(0,0)
        self.View.lv_section_student.setCurrentIndex(index)

    def get_model_latest_section(self):
        section_model = self.View.tv_sections.model()
        if section_model.rowCount() <= 1:
            self.View.TableSectionStudentLoadingScreen.hide()
            return

        self.SectionStudent.target_section_row = section_model.rowCount() - 2
        self.SectionStudent.TargetSection = self.Model.Section(*section_model.getRowData(self.SectionStudent.target_section_row))
        
        self.get_all_section_student.val = self.SectionStudent.TargetSection,
        self.get_all_section_student.start()

    def select_latest_targets(self):
        self.View.tv_sections.selectRow(self.SectionStudent.target_section_row)
        self.set_latest_section_inputs()
        section_student = self.View.lv_section_student.model().getData()

        if section_student != []:
            student_model = self.View.tv_students.model()
            student = section_student[0]
            self.SectionStudent.target_student_row = student_model.findRow(student)
            self.SectionStudent.TargetStudent = self.Model.Student(*student_model.getRowData(self.SectionStudent.target_student_row))
            self.SectionStudent.TargetStudent.Section = self.SectionStudent.TargetSection.Name

            self.View.tv_students.selectRow(self.SectionStudent.target_student_row)
            self.set_latest_section_student_inputs()

    def set_latest_section_inputs(self):
        Section = self.SectionStudent.TargetSection
        self.View.txt_section_name.setText(Section.Name)

    def set_latest_section_student_inputs(self):
        Student = self.SectionStudent.TargetStudent
        self.View.txt_student_username.setText(Student.Username)
        self.View.txt_student_password.setText(str(Student.Salt + Student.Hash))
        self.View.txt_student_password.setCursorPosition(0)

    # *Teacher
    def get_model_latest_teacher(self):
        teacher_model = self.View.tv_teachers.model()
        if teacher_model.rowCount() <= 1:
            self.View.TableTeacherLoadingScreen.hide()
            return

        self.TeacherAttendance.target_teacher_row = teacher_model.rowCount() - 2
        self.TeacherAttendance.TargetTeacher = self.Model.Teacher(*teacher_model.getRowData(self.TeacherAttendance.target_teacher_row))
        self.View.tv_teachers.selectRow(self.TeacherAttendance.target_teacher_row)

        self.set_latest_teacher_inputs()

    def set_latest_teacher_inputs(self):
        Teacher = self.TeacherAttendance.TargetTeacher
        self.View.txt_teacher_username.setText(Teacher.Username)
        self.View.txt_teacher_password.setText(str(Teacher.Salt + Teacher.Hash))
        self.View.txt_teacher_password.setCursorPosition(0)
    
    # *Class
    def get_model_latest_class(self):
        class_model = self.View.tv_class.model()
        if class_model.rowCount() <= 1:
            self.View.TableClassLoadingScreen.hide()
            return
        
        self.ClassMember.target_class_row = class_model.rowCount() - 2
        self.ClassMember.TargetClass = self.Model.Class(*class_model.getRowData(self.ClassMember.target_class_row))
        self.View.tv_class.selectRow(self.ClassMember.target_class_row)

        self.set_latest_class_inputs()

    def set_latest_class_inputs(self):
        Class = self.ClassMember.TargetClass
        self.View.txt_class_code.setText(Class.Code)
        self.View.txt_class_name.setText(Class.Name)
        self.View.txt_class_start.setTime(QtCore.QTime(*Class.Start))
        self.View.txt_class_end.setTime(QtCore.QTime(*Class.End))
    

    def resize(self, event):
        self.View.title_bar.resize_window()
        self.View.TableSectionStudentLoadingScreen.resize_loader()
        self.View.TableTeacherLoadingScreen.resize_loader()
        self.View.TableClassLoadingScreen.resize_loader()
        self.View.SectionLoadingScreen.resize_loader()
        self.View.StudentLoadingScreen.resize_loader()
        self.View.SectionStudentLoadingScreen.resize_loader()
        self.View.TeacherLoadingScreen.resize_loader()
        self.View.AttendanceLoadingScreen.resize_loader()
        self.View.AttendanceStudentLoadingScreen.resize_loader()
        self.View.ClassLoadingScreen.resize_loader()
        self.View.ClassTeacherLoadingScreen.resize_loader()
        self.View.ClassStudentLoadingScreen.resize_loader()
        self.View.URLLoadingScreen.resize_loader()
        self.View.URLSLoadingScreen.resize_loader()
        super(QMainWindow, self.View).resizeEvent(event)