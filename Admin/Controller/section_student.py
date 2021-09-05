from Admin.Misc.Widgets.data_table import DataTable
from PyQt5.QtWidgets import QDialog
from Admin.Misc.Functions.is_blank import is_blank
from PyQt5 import QtCore


class GetTargetSectionStudent(QtCore.QThread):
    operation = QtCore.pyqtSignal(object)

    def __init__(self, SectionStudents):
        super().__init__()
        self.SectionStudents = SectionStudents
        self.value = ()

    def run(self):
        SectionStudents = self.SectionStudents(*self.value)
        self.operation.emit(SectionStudents)
        self.quit()


class GetTargetStudentSection(QtCore.QThread):
    operation = QtCore.pyqtSignal(object, object)

    def __init__(self, StudentSection, SectionStudents):
        super().__init__()
        self.StudentSection = StudentSection
        self.SectionStudents = SectionStudents
        self.value = ()

    def run(self):
        StudentSection = self.StudentSection(*self.value)
        SectionStudents = self.SectionStudents(StudentSection)
        self.operation.emit(StudentSection, SectionStudents)
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


class Operation(QtCore.QThread):
    operation = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = ()

    def run(self):
        successful = self.fn(*self.val)
        if successful:
            self.operation.emit()
        else:
            self.error.emit()
        self.quit()


class SectionStudent:

    def __init__(self, Model, View, Admin):
        self.Model = Model
        self.View = View
        self.Admin = Admin

        self.target_section_row = None
        self.TargetSection = None
        self.target_student_row = None
        self.TargetStudent = None
        self.target_section_student_row = None
        self.TargetSectionStudent = None

        self.connect_signals()

    def connect_signals(self):
        self.section_signals()
        self.section_operations()
        self.student_signals()
        self.student_operations()
        self.sectionstudent_signals()
        self.sectionstudent_operations()
    
    # SectionStudent
    def sectionstudent_signals(self):
        self.View.lv_section_student.clicked.connect(self.list_sectionstudent_clicked)

    def sectionstudent_operations(self):
        pass

    def list_sectionstudent_clicked(self, index):
        row = index.row()
        self.set_target_section_student(self.Model.SectionStudent(None, self.View.txt_section_name.text(), self.View.lv_section_student.model().getRowData(row)))
        student_model = self.View.tv_students.model()
        self.set_target_student(self.Model.Student(*student_model.getRowData(student_model.findRow(self.TargetSectionStudent.Student))))

    # Section
    def section_signals(self):
        self.View.tv_sections.clicked.connect(self.table_section_clicked)

    def section_operations(self):
        self.GetTargetSectionStudent = GetTargetSectionStudent(
            self.Model.get_all_section_student)
        self.GetTargetSectionStudent.started.connect(
            self.View.TableSectionStudentLoadingScreen.run)
        self.GetTargetSectionStudent.started.connect(
            self.View.SectionStudentLoadingScreen.run)
        self.GetTargetSectionStudent.operation.connect(
            self.get_target_section_student)
        self.GetTargetSectionStudent.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        self.GetTargetSectionStudent.finished.connect(
            self.View.SectionStudentLoadingScreen.hide)

    def table_section_clicked(self, index):
        row = index.row()
        section_model = self.View.tv_sections.model()
        if row == section_model.rowCount() - 1:
            return

        self.set_target_section(self.Model.Section(
            *section_model.getRowData(row)))
        self.GetTargetSectionStudent.value = self.TargetSection,
        self.GetTargetSectionStudent.start()

    def get_target_section_student(self, sectionstudents):
        target_section_student = sectionstudents[-1]
        student_model = self.View.tv_students.model()
        target_student = self.Model.Student(
            *student_model.getRowData(student_model.findRow(target_section_student.Student)))

        self.set_section_student_list(sectionstudents)
        self.set_target_section_student(target_section_student)
        self.set_target_student(target_student)

    def set_target_section(self, Section):
        self.TargetSection = Section
        self.select_target_section_row()

    def select_target_section_row(self):
        section_model = self.View.tv_sections.model()
        self.target_section_row = section_model.findRow(
            self.TargetSection.Name)
        self.set_section_inputs()

    def set_section_inputs(self):
        self.View.tv_sections.selectRow(self.target_section_row)
        self.View.txt_section_name.setText(self.TargetSection.Name)

    # Student
    def student_signals(self):
        self.View.tv_students.clicked.connect(self.table_student_clicked)

    def student_operations(self):
        self.GetTargetStudentSection = GetTargetStudentSection(
            self.Model.get_student_section, self.Model.get_all_section_student)
        self.GetTargetStudentSection.started.connect(
            self.View.TableSectionStudentLoadingScreen.run)
        self.GetTargetStudentSection.started.connect(
            self.View.SectionStudentLoadingScreen.run)
        self.GetTargetStudentSection.operation.connect(
            self.get_target_student_section)
        self.GetTargetStudentSection.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        self.GetTargetStudentSection.finished.connect(
            self.View.SectionStudentLoadingScreen.hide)

    def table_student_clicked(self, index):
        row = index.row()
        student_model = self.View.tv_students.model()
        if row == student_model.rowCount() - 1:
            return

        self.set_target_student(self.Model.Student(
            *student_model.getRowData(row)))
        self.GetTargetStudentSection.value = self.TargetStudent,
        self.GetTargetStudentSection.start()

    def get_target_student_section(self, Section, sectionstudents):
        for sectionstudent in sectionstudents:
            if sectionstudent.Student == self.TargetStudent.Username:
                target_section_student = sectionstudent
                break
        self.set_target_section(Section)
        self.set_section_student_list(sectionstudents)
        self.set_target_section_student(target_section_student)

    def set_target_student(self, Student):
        self.TargetStudent = Student
        self.select_target_student_row()

    def select_target_student_row(self):
        student_model = self.View.tv_students.model()
        self.target_student_row = student_model.findRow(
            self.TargetStudent.Username)
        self.View.tv_students.selectRow(self.target_student_row)
        self.set_student_inputs()

    def set_student_inputs(self):
        self.View.txt_student_username.setText(self.TargetStudent.Username)
        self.View.txt_student_password.setText(
            str(self.TargetStudent.Salt + self.TargetStudent.Hash))
        self.View.txt_student_password.setCursorPosition(0)

    # SectionStudent
    def set_target_section_student(self, SectionStudent):
        self.TargetSectionStudent = SectionStudent
        self.select_target_section_student_row()

    def select_target_section_student_row(self):
        section_student_model = self.View.lv_section_student.model()
        self.target_section_student_row = section_student_model.createIndex(
            section_student_model.findRow(self.TargetSectionStudent.Student), 0)
        self.View.lv_section_student.setCurrentIndex(
            self.target_section_student_row)

    def set_section_student_list(self, sectionstudents):
        section_student_model = self.Model.ListModel(
            self.View.lv_section_student, sectionstudents)
        self.View.lv_section_student.setModel(section_student_model)
