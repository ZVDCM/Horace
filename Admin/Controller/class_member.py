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


class ClassMember:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.target_class_row = None
        self.TargetClass = None

        self.connect_signals()

    def connect_signals(self):
        self.View.tv_class.clicked.connect(self.table_class_clicked)
        self.View.btn_init_add_class.clicked.connect(self.init_add_class)
        self.View.btn_init_edit_class.clicked.connect(self.init_edit_class)
        self.View.btn_add_edit_class.clicked.connect(self.init_add_edit_class)
        self.View.btn_cancel_class.clicked.connect(self.cancel_class)

    # Operations
    def GetAllClass(self):
        handler = Get(self.Model.get_all_class)
        handler.started.connect(self.View.TableClassLoadingScreen.run)
        handler.operation.connect(self.set_class_table)
        handler.finished.connect(self.View.TableClassLoadingScreen.hide)
        return handler

    def AddClass(self):
        handler = Operation(self.Model.create_class)
        handler.started.connect(self.View.ClassLoadingScreen.run)
        handler.error.connect(self.class_error)
        handler.finished.connect(self.View.ClassLoadingScreen.hide)
        handler.finished.connect(self.View.btn_cancel_class.click)
        return handler 

    # Table
    def table_class_clicked(self, index):
        row = index.row()
        class_model = self.View.tv_class.model()
        if row == class_model.rowCount() - 1:
            return

        self.set_target_class(self.Model.Class(
            *class_model.getRowData(row)))

    def set_class_table(self, classes):
        class_model = self.Model.TableModel(
            self.View.tv_class, classes, self.Model.Class.get_headers())
        self.View.tv_class.setModel(class_model)
        self.View.tv_class.horizontalHeader().setMinimumSectionSize(150)

    def set_target_class(self, Class):
        self.TargetClass = Class
        self.select_target_class_row()

    def select_target_class_row(self):
        class_model = self.View.tv_class.model()
        self.target_class_row = class_model.findRow(
            self.TargetClass.Code)
        self.View.tv_class.selectRow(self.target_class_row)
        self.View.tv_class.setFocus(True)
        self.set_class_inputs()

    def set_class_inputs(self):
        self.View.txt_class_code.setText(self.TargetClass.Code)
        self.View.txt_class_name.setText(self.TargetClass.Name)
        self.View.txt_class_start.setTime(
            QtCore.QTime(*self.TargetClass.Start))
        self.View.txt_class_end.setTime(QtCore.QTime(*self.TargetClass.End))

    def select_latest_class(self, _class):
        class_model = self.View.tv_class.model()
        self.set_target_class(self.Model.Class(
            *class_model.getRowData(class_model.findRow(_class))))

    # Buttons
    def init_add_class(self):
        self.View.clear_class_inputs()
        self.View.disable_class_buttons()
        self.View.enable_class_inputs()
        self.View.set_class('Add')

    def init_edit_class(self):
        self.View.disable_class_buttons()
        self.View.enable_class_inputs()
        self.View.set_class('Edit')

    def cancel_class(self):
        self.select_target_class_row()
        self.View.enable_class_buttons()
        self.View.disable_class_inputs()
        self.View.set_class('Read')

    def init_add_edit_class(self):
        if self.View.class_state == "Add":
            self.add_class()
        elif self.View.class_state == "Edit":
            self.edit_class()

    # Class Error
    def class_error(self, error):
        if error == 'exists':
            self.View.run_popup(f'Class exists')

    # Class Add
    def add_class(self):
        code = self.View.txt_class_code.text()
        name = self.View.txt_class_name.text()
        start = self.View.txt_class_start.time()
        start = ":".join([str(start.hour()), str(start.minute()), str(start.second())])
        end = self.View.txt_class_end.time()
        end = ":".join([str(end.hour()), str(end.minute()), str(end.second())])

        if is_blank(code) or is_blank(name):
            self.View.run_popup(f'Class fields must be filled')
            return

        self.get_all_class_handler = self.GetAllClass()
        self.add_class_handler = self.AddClass()

        self.add_class_handler.val = code, name, start, end
        self.add_class_handler.operation.connect(self.get_all_class_handler.start)

        self.get_all_class_handler.finished.connect(lambda: self.select_latest_class(code))
        self.add_class_handler.start()

    # Class Edit
    def edit_class(self):
        code = self.View.txt_class_code.text()
        name = self.View.txt_class_name.text()
        start = self.View.txt_class_start.time()
        end = self.View.txt_class_end.time()
        
        if is_blank(code) or is_blank(name):
            self.View.run_popup(f'Class fields must be filled')
            return
