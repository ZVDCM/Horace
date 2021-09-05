from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from Admin.Controller.section_student import SectionStudent
from Admin.Controller.teacher_attendance import TeacherAttendance
from Admin.Controller.class_member import ClassMember
from Admin.Controller.blacklist_url import BlacklistURL

class GetAllSectionAndStudent(QtCore.QThread):
    section_operation = QtCore.pyqtSignal(list)
    student_operation = QtCore.pyqtSignal(list)

    def __init__(self, get_all_section, get_all_student):
        super().__init__()
        self.get_all_section = get_all_section
        self.get_all_student = get_all_student

    def run(self):
        res = self.get_all_section()
        self.section_operation.emit(res)
        res = self.get_all_student()
        self.student_operation.emit(res)
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
        self.StudentSection = TeacherAttendance(
            self.Model, self.View, self)
        self.StudentSection = ClassMember(
            self.Model, self.View, self)
        self.StudentSection = BlacklistURL(
            self.Model, self.View, self)

        self.connect_signals()
        self.init_databases()

        self.View.run()

    def connect_signals(self):
        for side_nav in self.View.side_navs:
            side_nav.operation.connect(self.change_page)

        self.View.resizeEvent = self.resize

        self.get_all_sections_and_students = GetAllSectionAndStudent(self.Model.SectionStudent.get_all_section, self.Model.SectionStudent.get_all_student)
        self.get_all_sections_and_students.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        self.get_all_sections_and_students.section_operation.connect(self.set_section_tableview)
        self.get_all_sections_and_students.student_operation.connect(self.set_student_tableview)
        self.get_all_sections_and_students.finished.connect(self.View.TableSectionStudentLoadingScreen.hide)
        self.get_all_sections_and_students.finished.connect(self.get_model_latest_section)

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
        self.get_all_sections_and_students.start()

    def set_section_tableview(self, sections):
        section_model = self.Model.TableModel(self.View.tv_sections, sections, self.Model.Section.get_headers())
        self.View.tv_sections.setModel(section_model)
        self.View.tv_sections.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_sections.setFocus(True)

    def set_student_tableview(self, students):
        student_model = self.Model.TableModel(self.View.tv_students, students, self.Model.Student.get_headers())
        self.View.tv_students.setModel(student_model)
        self.View.tv_students.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_students.setFocus(True)

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
        section_student = self.View.lv_section_student.model().getData()[0]
        self.set_latest_section_inputs()

        if section_student != ():
            student_model = self.View.tv_students.model()
            student = section_student
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