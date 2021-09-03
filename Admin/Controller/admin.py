from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from Admin.Controller.section_student import SectionStudent
from Admin.Controller.teacher_attendance import TeacherAttendance
from Admin.Controller.class_member import ClassMember
from Admin.Controller.blacklist_url import BlacklistURL

class GetAll(QtCore.QThread):
    operation = QtCore.pyqtSignal(list)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        res = self.fn()
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

        self.get_all_sections = GetAll(self.Model.SectionStudent.get_all_section)
        self.get_all_sections.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        self.get_all_sections.operation.connect(self.set_section_tableview)
        self.get_all_sections.finished.connect(self.View.TableSectionStudentLoadingScreen.hide)

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
        self.get_all_sections.start()

    def set_section_tableview(self, sections):
        section_model = self.Model.TableModel(self.View.tv_sections, sections, self.Model.Section.get_headers())
        self.View.tv_sections.setModel(section_model)
        self.View.tv_sections.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_sections.setFocus(True)
        index = section_model.rowCount() - 2
        self.View.tv_sections.selectRow(index)
        self.SectionStudent.set_target_section(self.Model.Section(*section_model.getRowData(index)))
        self.SectionStudent.set_section_input_values()

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