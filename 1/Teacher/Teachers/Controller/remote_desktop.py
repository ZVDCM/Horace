from PyQt5.QtCore import QThread, pyqtSignal
from Teachers.Controller.RDC.host import Host as RDCHost

class Operation(QThread):
    operation = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        self.operation.emit()
        self.quit()

class SetStatus(QThread):
    operation = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.val = None

    def run(self):
        self.operation.emit(self.val)
        self.quit()

class RemoteDesktop:

    def __init__(self, Controller, target):
        self.View = Controller.View.RemoteDesktop
        self.Controller = Controller
        
        self.connect_signals()
        self.RDCHost = RDCHost(self, self.Controller.Meeting, self.View, self.Controller.Meeting.ChatHost, target)
        self.View.title_bar.title.setText(f'Controlling {target}')
        self.View.run()
        self.StartLoading.start()

    def connect_signals(self):
        self.StartLoading = Operation()
        self.StartLoading.operation.connect(self.View.LoadingScreen.show)

        self.EndLoading = Operation()
        self.EndLoading.operation.connect(self.View.LoadingScreen.hide)

    def set_status(self, text):
        self.View.set_control_status(text)
