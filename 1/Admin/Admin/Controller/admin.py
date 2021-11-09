import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from Admin.Controller.section_student import SectionStudent
from Admin.Controller.teacher_attendance import TeacherAttendance
from Admin.Controller.class_member import ClassMember
from Admin.Controller.blacklist_url import BlacklistURL
import threading
from win32api import GetSystemMetrics
from Admin.Misc.Functions.relative_path import relative_path

from Admin.Misc.Widgets.change_password import ChangePassword


class SetAdminStatus(QtCore.QThread):

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        self.fn(self.val)
        self.quit()

class GetAll(QtCore.QThread):
    operation = QtCore.pyqtSignal(object)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        res = self.fn()
        self.operation.emit(res)
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
            self.Model.BlacklistURL, self.View, self)

        self.connect_signals()
        self.init_databases()

        self.View.title_bar.title.setText("Admin")

        self.start_time = QtCore.QTime(0, 0, 0)
        self.status_time = 0

        self.View.run()

    def connect_signals(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000)

        for side_nav in self.View.side_navs:
            side_nav.operation.connect(self.change_page)

        self.View.resizeEvent = self.resize

        self.get_all_section = GetAll(self.Model.SectionStudent.get_all_section)
        self.get_all_section.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        self.get_all_section.operation.connect(self.SectionStudent.set_section_table)
        self.get_all_section.finished.connect(self.View.TableSectionStudentLoadingScreen.hide)
        
        self.get_all_student = GetAll(self.Model.SectionStudent.get_all_student)
        self.get_all_student.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        self.get_all_student.operation.connect(self.SectionStudent.set_student_table)
        self.get_all_student.finished.connect(self.View.TableSectionStudentLoadingScreen.hide)
        self.get_all_student.finished.connect(lambda: self.set_admin_status_handler("Sections and Students loaded successfully"))
        
        self.get_all_teacher_and_attendances = GetAll(self.Model.TeacherAttendance.get_all_teacher)
        self.get_all_teacher_and_attendances.started.connect(self.View.TableTeacherLoadingScreen.run)
        self.get_all_teacher_and_attendances.operation.connect(self.TeacherAttendance.set_teacher_table)
        self.get_all_teacher_and_attendances.finished.connect(self.View.TableTeacherLoadingScreen.hide)
        self.get_all_teacher_and_attendances.finished.connect(self.get_model_latest_teacher)
        self.get_all_teacher_and_attendances.finished.connect(lambda: self.set_admin_status_handler("Teacher and Attendances loaded successfully"))

        self.get_all_class = GetAll(self.Model.ClassMember.get_all_class)
        self.get_all_class.started.connect(self.View.TableClassLoadingScreen.run)
        self.get_all_class.operation.connect(self.ClassMember.set_class_table)
        self.get_all_class.finished.connect(self.View.TableClassLoadingScreen.hide)
        self.get_all_class.finished.connect(self.get_model_latest_class)
        self.get_all_class.finished.connect(lambda: self.set_admin_status_handler("Classes and Members loaded successfully"))
        
        self.get_all_url = GetAll(self.Model.BlacklistURL.get_all_url)
        self.get_all_url.started.connect(self.View.URLSLoadingScreen.run)
        self.get_all_url.operation.connect(self.BlacklistURL.set_url_list)
        self.get_all_url.finished.connect(self.View.URLSLoadingScreen.hide)
        self.get_all_url.finished.connect(self.get_model_latest_url)
        self.get_all_url.finished.connect(lambda: self.set_admin_status_handler("Blacklisted URLs loaded successfully"))

        self.get_all_section.finished.connect(self.get_all_student.start)
        self.get_all_student.finished.connect(self.get_all_teacher_and_attendances.start)
        self.get_all_teacher_and_attendances.finished.connect(self.get_all_class.start)
        self.get_all_class.finished.connect(self.get_all_url.start)

        self.get_all_section_student = Get(self.Model.SectionStudent.get_all_section_student)
        self.get_all_section_student.started.connect(self.View.SectionStudentLoadingScreen.run)
        self.get_all_section_student.operation.connect(self.set_section_student_listview)
        self.get_all_section_student.finished.connect(self.View.SectionStudentLoadingScreen.hide)

        self.get_target_class_teacher = Get(self.Model.ClassMember.get_target_class_teacher)
        self.get_target_class_teacher.started.connect(self.View.TableClassLoadingScreen.run)
        self.get_target_class_teacher.operation.connect(self.ClassMember.set_class_teacher_list)
        self.get_target_class_teacher.finished.connect(self.View.TableClassLoadingScreen.hide)

        self.get_target_class_section = Get(self.Model.ClassMember.get_target_class_section)
        self.get_target_class_section.started.connect(self.View.TableClassLoadingScreen.run)
        self.get_target_class_section.operation.connect(self.ClassMember.set_class_section_list)
        self.get_target_class_section.finished.connect(self.View.TableClassLoadingScreen.hide)

        self.get_target_teacher_attendances = Get(self.Model.TeacherAttendance.get_all_attendances)
        self.get_target_teacher_attendances.started.connect(self.View.AttendanceLoadingScreen.run)
        self.get_target_teacher_attendances.operation.connect(self.TeacherAttendance.set_teacher_attendances_list)
        self.get_target_teacher_attendances.finished.connect(self.View.AttendanceLoadingScreen.hide)

        self.View.btn_more.clicked.connect(self.more_clicked)
        self.View.AccountContextMenu._create.connect(self.create_backup)
        self.View.AccountContextMenu._load.connect(self.load_backup)
        self.View.AccountContextMenu._change.connect(self.change_password)
        self.View.AccountContextMenu._sign_out.connect(self.View.close)
        self.View.closeEvent = self.parent_closed

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
        self.get_all_section.start()

    # *SectionStudent
    def set_section_student_listview(self, students):
        section_student_model = self.Model.ListModel(self.View.lv_section_student, students)
        self.View.lv_section_student.setModel(section_student_model)
        index = section_student_model.createIndex(0,0)
        self.View.lv_section_student.setCurrentIndex(index)
        self.View.lbl_section_students_status.setText(f'Students: {len(students)}')


    # *Teacher
    def get_model_latest_teacher(self):
        teacher_model = self.View.tv_teachers.model()
        if teacher_model.rowCount() <= 1:
            self.View.lbl_attendance_status.setText(f'Attendances: 0')
            self.View.TableTeacherLoadingScreen.hide()
            return

        self.TeacherAttendance.target_teacher_row = teacher_model.rowCount() - 2
        self.TeacherAttendance.TargetTeacher = self.Model.Teacher(*teacher_model.getRowData(self.TeacherAttendance.target_teacher_row))
        self.View.tv_teachers.selectRow(self.TeacherAttendance.target_teacher_row)
        self.set_latest_teacher_inputs()

        self.get_target_teacher_attendances.val = self.TeacherAttendance.TargetTeacher,
        self.get_target_teacher_attendances.start()

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

        self.get_target_class_teacher.val = self.ClassMember.TargetClass,
        self.get_target_class_teacher.start()
        self.set_latest_class_inputs()

    def set_latest_class_inputs(self):
        Class = self.ClassMember.TargetClass
        self.View.txt_class_code.setText(Class.Code)
        self.View.txt_class_name.setText(Class.Name)
        self.View.txt_class_start.setTime(QtCore.QTime(*Class.Start))
        self.View.txt_class_end.setTime(QtCore.QTime(*Class.End))

    # *URLS
    def get_model_latest_url(self):
        url_model = self.View.lv_url.model()
        try:
            self.BlacklistURL.target_url_row = 0
            self.BlacklistURL.TargetUrl = self.Model.Url(None, url_model.getRowData(self.BlacklistURL.target_url_row))
            index = url_model.createIndex(self.BlacklistURL.target_url_row, 0)
            self.View.lv_url.setCurrentIndex(index)
        except IndexError:
            return

        self.set_latest_url_inputs()

    def set_latest_url_inputs(self):
        Url = self.BlacklistURL.TargetUrl
        self.View.txt_url.setText(Url.Domain)
        self.View.web_viewer.setUrl(QtCore.QUrl(f'https://{Url.Domain}'))

    def resize(self, event):
        self.View.ActiveOverlay.resize_loader()
        self.View.TableSectionStudentLoadingScreen.resize_loader()
        self.View.TableTeacherLoadingScreen.resize_loader()
        self.View.TableClassLoadingScreen.resize_loader()
        self.View.SectionLoadingScreen.resize_loader()
        self.View.StudentLoadingScreen.resize_loader()
        self.View.SectionStudentLoadingScreen.resize_loader()
        self.View.TeacherLoadingScreen.resize_loader()
        self.View.AttendanceLoadingScreen.resize_loader()
        self.View.ClassLoadingScreen.resize_loader()
        self.View.ClassTeacherLoadingScreen.resize_loader()
        self.View.ClassSectionLoadingScreen.resize_loader()
        self.View.URLLoadingScreen.resize_loader()
        self.View.URLSLoadingScreen.resize_loader()
        super(QMainWindow, self.View).resizeEvent(event)

    def set_admin_status_handler(self, status):
        threading.Thread(target=self.set_admin_status, args=(status,), daemon=True).start()

    def set_admin_status(self, status):
        self.status_time = 0
        self.View.set_admin_status(status)

    def timer_event(self):
        self.start_time = self.start_time.addSecs(1)

        self.status_time += 1
        if self.status_time == 5:
            self.View.lbl_database_status.clear()

    def more_clicked(self):
        pos = self.View.btn_more.mapToGlobal(self.View.btn_more.rect().bottomLeft())
        height = GetSystemMetrics(1)
        if pos.y() > height - self.View.AccountContextMenu.height():
            pos_up = self.View.btn_more.mapToGlobal(self.View.btn_more.rect().topLeft())
            self.View.AccountContextMenu.move(pos_up.x(), pos_up.y()- self.View.AccountContextMenu.height())
        else:
            self.View.AccountContextMenu.move(pos)
        self.View.AccountContextMenu.show()

    def create_backup(self):
        default_path = os.path.expanduser('~/Documents')
        path = QFileDialog.getExistingDirectory(
                self.View, 'Save backup to', default_path)
        if path:
            self.Controller.SignInController.SignIn.show_alert('file', 'Creating backup')
            path = os.path.join(path, 'horace.sql')
            os.system(f"mysqldump --defaults-file={relative_path('Config', [''], 'admin.ini')} --databases Horace --tables users --where=\"Privilege<>'Admin'\" > {path}")
            os.system(f"mysqldump --defaults-file={relative_path('Config', [''], 'admin.ini')} --databases Horace --tables sections section_students classes class_teachers class_sections attendances urls >> {path}")
            os.system(f"mysqldump --defaults-file={relative_path('Config', [''], 'admin.ini')} --databases Horace --tables security_questions --where=\"Admin<>'Admin'\" >> {path}")
            self.Controller.SignInController.SignIn.show_alert('file', 'Backup created')
            self.set_admin_status_handler("Database backup created successfully")

    def load_backup(self):
        default_path = os.path.expanduser('~/Documents')
        path = QFileDialog.getOpenFileName(
                self.View, f'Select database backup file', default_path, 'SQL (*.sql)')
        path = path[0]
        if path:
            self.Model.Database.load_backup(path)
            self.init_databases()

    def change_password(self):
        self.ChangePassword = ChangePassword(self, self.View, self.Controller.User, self.Model)
        self.ChangePassword.run()
        
    def parent_closed(self, event):
        try:
            if self.View.isVisible():
                self.View.close()
        except RuntimeError:
            pass
        self.Controller.SignInController.View.init_sign_in()
        self.Controller.SignInController.Model.init_sign_in()
        self.Controller.SignInController.init_sign_in()
        self.timer.stop()
        super(QMainWindow, self.View).closeEvent(event)