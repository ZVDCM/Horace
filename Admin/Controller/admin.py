class Admin:

    def __init__(self, Controller):
        self.Model = Controller.Model.Admin
        self.View = Controller.View.Admin
        self.Controller = Controller 


        self.connect_signals()
        self.View.run()

    def connect_signals(self):
        pass
