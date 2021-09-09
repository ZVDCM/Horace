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

class Lobby:

    def __init__(self, Controller):
        self.Model = Controller.Model.Lobby
        self.View = Controller.View.Lobby
        self.Controller = Controller

        self.connect_signals()
        self.get_classes()

        self.View.run()

    def connect_signals(self):
        self.get_all_class = Get(self.Model.get_all_class)
        self.get_all_class.started.connect(self.View.ClassLoadingScreen.run)
        self.get_all_class.operation.connect(self.set_classes)
        self.get_all_class.finished.connect(self.View.ClassLoadingScreen.hide)

    def get_classes(self):
        self.get_all_class.val = self.Controller.User,
        self.get_all_class.finished.connect(self.set_classes_operation)
        self.get_all_class.start()
    
    def set_classes_operation(self):
        for index in range(self.View.flow_layout.count()):
            target_class_item = self.View.flow_layout.itemAt(index).widget()
            target_class_item.operation.connect(self.class_item_clicked)

    def set_classes(self, classes):
        for _class in classes:
            self.View.add_class_item(_class)

    def class_item_clicked(self, Class):
        Class.HostAddress = self.get_local_ip()
        self.Controller.Model.init_meeting()
        self.Controller.View.init_meeting()
        self.Controller.init_meeting(Class)