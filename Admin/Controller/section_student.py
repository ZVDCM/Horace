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
        self.student_signals()
        self.sectionstudent_signals()

    # *SectionStudent
    def sectionstudent_signals(self):
        self.View.lv_section_student.clicked.connect(
            self.list_sectionstudent_clicked)

    # List
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

    def list_sectionstudent_clicked(self, index):
        row = index.row()
        self.set_target_section_student(self.Model.SectionStudent(
            None, self.View.txt_section_name.text(), self.View.lv_section_student.model().getRowData(row)))
        student_model = self.View.tv_students.model()
        self.set_target_student(self.Model.Student(
            *student_model.getRowData(student_model.findRow(self.TargetSectionStudent.Student))))

    # *Section
    def section_signals(self):
        self.View.tv_sections.clicked.connect(self.table_section_clicked)
        self.View.btn_init_add_section.clicked.connect(self.init_add_section)
        self.View.btn_init_edit_section.clicked.connect(self.init_edit_section)
        self.View.btn_add_edit_section.clicked.connect(self.init_add_edit_section)
        self.View.btn_cancel_section.clicked.connect(self.cancel_section)
        self.View.btn_delete_section.clicked.connect(self.delete_section)

    # Section Operations
    def GetTargetSectionStudent(self):
        handler = GetTargetSectionStudent(
            self.Model.get_all_section_student)
        handler.operation.connect(
            self.get_target_section_student)
        return handler

    def GetAllSection(self):
        handler = Get(self.Model.get_all_section)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.operation.connect(self.set_section_table)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def AddSection(self):
        handler = Operation(self.Model.create_section)
        handler.started.connect(self.View.SectionLoadingScreen.run)
        handler.error.connect(self.section_error)
        handler.finished.connect(self.View.SectionLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_section.click)
        return handler

    def EditSection(self):
        handler = Operation(self.Model.edit_section)
        handler.started.connect(self.View.SectionLoadingScreen.run)
        handler.error.connect(self.section_error)
        handler.finished.connect(self.View.SectionLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_section.click)
        return handler

    def DeleteSection(self):
        handler = Operation(self.Model.delete_section)
        handler.started.connect(self.View.SectionLoadingScreen.run)
        handler.finished.connect(self.View.SectionLoadingScreen.hide)
        handler.finished.connect(self.View.clear_section_inputs)
        return handler

    # Table
    def table_section_clicked(self, index):
        row = index.row()
        section_model = self.View.tv_sections.model()
        if row == section_model.rowCount() - 1:
            return

        self.get_target_section_student_handler = self.GetTargetSectionStudent()
        self.set_target_section(self.Model.Section(
            *section_model.getRowData(row)))
        self.get_target_section_student_handler.value = self.TargetSection,
        self.get_target_section_student_handler.start()

    def get_target_section_student(self, sectionstudents):
        if sectionstudents != ():
            target_section_student = sectionstudents[-1]
            student_model = self.View.tv_students.model()
            target_student = self.Model.Student(
                *student_model.getRowData(student_model.findRow(target_section_student.Student)))

            self.set_section_student_list(sectionstudents)
            self.set_target_section_student(target_section_student)
            self.set_target_student(target_student)
        else:
            self.View.tv_students.clearSelection()
            self.View.clear_student_inputs()
            self.View.lv_section_student.model().removeRows(0, self.View.lv_section_student.model().rowCount())

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

    def set_section_table(self, sections):
        section_model = self.Model.TableModel(self.View.tv_sections, sections, self.Model.Section.get_headers())
        self.View.tv_sections.setModel(section_model)
        self.View.tv_sections.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_sections.setFocus(True)

    def select_latest_section(self, section):
        section_model = self.View.tv_sections.model()
        self.set_target_section(self.Model.Section(
            *section_model.getRowData(section_model.findRow(section))))

    def get_latest_target_section_student(self):
        section_model = self.View.tv_sections.model()
        self.set_target_section(self.Model.Section(
            *section_model.getRowData(section_model.rowCount() - 2)))
        self.get_target_section_student_handler.value = self.TargetSection,
        self.get_target_section_student_handler.start()

    # Buttons
    def init_add_section(self):
        self.View.clear_section_inputs()
        self.View.disable_section_buttons()
        self.View.enable_section_inputs()
        self.View.set_section('Add')

    def init_edit_section(self):
        self.View.disable_section_buttons()
        self.View.enable_section_inputs()
        self.View.set_section('Edit')

    def cancel_section(self):
        self.select_target_section_row()
        self.View.enable_section_buttons()
        self.View.disable_section_inputs()
        self.View.set_section('Read')

    def init_add_edit_section(self):
        if self.View.section_state == "Add":
            self.add_section()
        elif self.View.section_state == "Edit":
            self.edit_section()
    
    # Section Error
    def section_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'Section exists')
    
    # Section Add
    def add_section(self):
        section = self.View.txt_section_name.text()
        if is_blank(section):
            self.View.run_pop('Section fields must be filled')
            return
        
        self.get_all_section_handler = self.GetAllSection()
        self.add_section_handler = self.AddSection()

        self.add_section_handler.val = section,
        self.add_section_handler.operation.connect(self.get_all_section_handler.start)

        self.get_all_section_handler.finished.connect(lambda: self.select_latest_section(section))
        self.get_all_section_handler.finished.connect(self.View.tv_students.clearSelection)
        self.get_all_section_handler.finished.connect(self.View.clear_student_inputs)
        self.get_all_section_handler.finished.connect(lambda: self.View.lv_section_student.model().removeRows(0, self.View.lv_section_student.model().rowCount()))
        self.add_section_handler.start()

    # Section Edit
    def edit_section(self):
        section = self.View.txt_section_name.text()
        if is_blank(section):
            self.View.run_pop('Section fields must be filled')
            return

        if section == self.TargetSection.Name:
            self.View.btn_cancel_section.click()
            return

        self.get_all_section_handler = self.GetAllSection()
        self.edit_section_handler = self.EditSection()

        self.edit_section_handler.val = self.TargetSection.ID, section
        self.edit_section_handler.operation.connect(self.get_all_section_handler.start)

        self.get_all_section_handler.finished.connect(lambda: self.select_latest_section(section))
        self.edit_section_handler.start()

    # Section Delete
    def delete_section(self):
        self.get_all_section_handler = self.GetAllSection()
        self.delete_section_handler = self.DeleteSection()

        self.delete_section_handler.val = self.TargetSection,
        self.delete_section_handler.operation.connect(self.get_all_section_handler.start)

        self.get_all_section_handler.finished.connect(self.get_latest_target_section_student)
        self.delete_section_handler.start()

    # *Student
    def student_signals(self):
        self.View.tv_students.clicked.connect(self.table_student_clicked)
        self.View.btn_init_add_student.clicked.connect(self.init_add_student)
        self.View.btn_init_edit_student.clicked.connect(self.init_edit_student)
        self.View.btn_add_edit_student.clicked.connect(self.init_add_edit_student)
        self.View.btn_cancel_student.clicked.connect(self.cancel_student)
        self.View.btn_delete_student.clicked.connect(self.init_delete_student)

    # Student Operations
    def GetTargetStudentSection(self):
        handler = GetTargetStudentSection(
            self.Model.get_student_section, self.Model.get_all_section_student)
        handler.operation.connect(
            self.get_target_student_section)
        return handler

    def GetAllStudents(self):
        handler = Get(self.Model.get_all_student)
        handler.started.connect(self.View.TableSectionStudentLoadingScreen.run)
        handler.operation.connect(self.set_student_table)
        handler.finished.connect(
            self.View.TableSectionStudentLoadingScreen.hide)
        return handler

    def GetAllSectionStudents(self):
        handler = Get(self.Model.get_all_section_student)
        handler.finished.connect(self.View.SectionStudentLoadingScreen.run)
        handler.operation.connect(self.set_section_student_list)
        handler.finished.connect(self.View.SectionStudentLoadingScreen.hide)
        return handler

    def AddStudent(self):
        handler = Operation(self.Model.create_student)
        handler.started.connect(self.View.StudentLoadingScreen.run)
        handler.error.connect(self.student_error)
        handler.finished.connect(self.View.StudentLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_student.click)
        return handler

    def EditStudent(self):
        handler = Operation(self.Model.edit_student)
        handler.started.connect(self.View.StudentLoadingScreen.run)
        handler.error.connect(self.student_error)
        handler.finished.connect(self.View.StudentLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_student.click)
        return handler

    def DeleteStudent(self):
        handler = Operation(self.Model.delete_student)
        handler.started.connect(self.View.StudentLoadingScreen.run)
        handler.finished.connect(self.View.StudentLoadingScreen.hide)
        return handler

    # Table
    def table_student_clicked(self, index):
        row = index.row()
        student_model = self.View.tv_students.model()
        if row == student_model.rowCount() - 1:
            return

        self.get_target_student_section_handler = self.GetTargetStudentSection()
        self.set_target_student(self.Model.Student(
            *student_model.getRowData(row)))
        self.get_target_student_section_handler.value = self.TargetStudent,
        self.get_target_student_section_handler.start()

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

    def set_student_table(self, students):
        student_model = self.Model.TableModel(
            self.View.tv_students, students, self.Model.Student.get_headers())
        self.View.tv_students.setModel(student_model)
        self.View.tv_students.horizontalHeader().setMinimumSectionSize(150)
        self.View.tv_students.setFocus(True)

    def select_latest_student(self, username):
        student_model = self.View.tv_students.model()
        self.set_target_student(self.Model.Student(
            *student_model.getRowData(student_model.findRow(username))))

    def get_latest_section_student(self):
        section_model = self.View.lv_section_student.model()
        self.set_target_section_student(self.Model.SectionStudent(None, self.TargetSection.Name, section_model.getData()[0]))
        student_model = self.View.tv_students.model()
        self.set_target_student(self.Model.Student(*student_model.getRowData(student_model.findRow(self.TargetSectionStudent.Student))))

    # Buttons
    def init_add_student(self):
        self.View.clear_student_inputs()
        self.View.disable_student_buttons()
        self.View.enable_student_inputs()
        self.View.set_student('Add')

    def init_edit_student(self):
        self.View.disable_student_buttons()
        self.View.enable_student_inputs()
        self.View.set_student('Edit')

    def cancel_student(self):
        self.select_target_student_row()
        self.View.enable_student_buttons()
        self.View.disable_student_inputs()
        self.View.set_student('Read')

    def init_add_edit_student(self):
        if self.View.student_state == "Add":
            self.add_student()
        elif self.View.student_state == "Edit":
            self.edit_student()

    # Student Error
    def student_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'Student exists')
        elif error == "section exists":
            self.View.run_popup(f'Student already in section')

    # Student Add
    def add_student(self):
        username = self.View.txt_student_username.text()
        password = self.View.txt_student_password.text()
        if is_blank(username) or is_blank(password):
            self.View.run_pop('Student fields must be filled')
            return

        self.get_all_student_handler = self.GetAllStudents()
        self.get_all_section_student_handler = self.GetAllSectionStudents()
        self.add_student_handler = self.AddStudent()

        self.add_student_handler.val = self.TargetSection.Name, username, password
        self.add_student_handler.operation.connect(
            self.get_all_student_handler.start)
        self.get_all_student_handler.finished.connect(
            self.get_all_section_student_handler.start)
        self.get_all_student_handler.finished.connect(
            lambda: self.select_latest_student(username))

        self.get_all_section_student_handler.val = self.TargetSection,
        self.get_all_section_student_handler.finished.connect(lambda: self.set_target_section_student(
            self.Model.SectionStudent(None, self.TargetSection.Name, username)))
        self.add_student_handler.start()

    # Student Edit
    def edit_student(self):
        username = self.View.txt_student_username.text()
        password = self.View.txt_student_password.text()

        if is_blank(username) or is_blank(password):
            self.View.run_pop('Student fields must be filled')
            self.View.btn_cancel_student.click()
            return

        if username == self.TargetStudent.Username and password == str(self.TargetStudent.Salt + self.TargetStudent.Hash):
            self.View.btn_cancel_student.click()
            return

        self.get_all_student_handler = self.GetAllStudents()
        self.get_all_section_student_handler = self.GetAllSectionStudents()
        self.edit_student_handler = self.EditStudent()

        self.edit_student_handler.val = self.TargetStudent.UserID, username, self.TargetStudent.Salt, self.TargetStudent.Hash, password
        self.edit_student_handler.operation.connect(
            self.get_all_student_handler.start)

        self.get_all_section_student_handler.val = self.TargetSection,
        self.get_all_section_student_handler.finished.connect(lambda: self.set_target_section_student(
            self.Model.SectionStudent(None, self.TargetSection.Name, username)))
        self.get_all_student_handler.finished.connect(
            self.get_all_section_student_handler.start)
        self.get_all_student_handler.finished.connect(
            lambda: self.select_latest_student(username))
        self.edit_student_handler.start()

    # Student Delete
    def init_delete_student(self):
        self.get_all_student_handler = self.GetAllStudents()
        self.get_all_section_student_handler = self.GetAllSectionStudents()
        self.delete_student_handler = self.DeleteStudent()

        self.delete_student_handler.val = self.TargetStudent,
        self.delete_student_handler.operation.connect(
            self.get_all_student_handler.start)

        self.get_all_section_student_handler.val = self.TargetSection,
        self.get_all_student_handler.finished.connect(
            self.get_all_section_student_handler.start)

        self.get_all_section_student_handler.finished.connect(self.get_latest_section_student)
        self.delete_student_handler.start()