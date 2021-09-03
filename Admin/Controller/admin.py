from Admin.Controller.section_student import SectionStudent
from Admin.Controller.teacher_attendance import TeacherAttendance
from Admin.Controller.class_member import ClassMember
from Admin.Controller.blacklist_url import BlacklistURL


class Admin:

    def __init__(self, Controller):
        self.Model = Controller.Model
        self.View = Controller.View.Admin
        self.Controller = Controller

        self.connect_signals()
        self.SectionStudent = SectionStudent(
            self.Model.SectionStudent, self.View, self.Controller)
        self.StudentSection = TeacherAttendance(
            self.Model, self.View, self.Controller)
        self.StudentSection = ClassMember(
            self.Model, self.View, self.Controller)
        self.StudentSection = BlacklistURL(
            self.Model, self.View, self.Controller)
        self.View.run()

    def connect_signals(self):
        for side_nav in self.View.side_navs:
            side_nav.operation.connect(self.change_page)

    def change_page(self, index):
        for side_nav in self.View.side_navs:
            if side_nav.is_active:
                side_nav.deactivate()
                break
        self.View.side_navs[index].activate()
        self.View.sw_all.setCurrentIndex(index)

    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)
