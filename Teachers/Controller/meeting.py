class Meeting:

    def __init__(self, Controller, Class):
        self.Model = Controller.Model.Meeting
        self.View = Controller.View.Meeting
        self.Controller = Controller
        self.Class = Class

        self.connect_signals()

        if not self.View.isVisible():
            self.View.run()

    def connect_signals(self):
        pass