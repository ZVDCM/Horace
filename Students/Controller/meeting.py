class Meeting:

    def __init__(self, Controller, Class):
        self.Model = Controller.Model.Meeting
        self.View = Controller.View.Meeting
        self.Controller = Controller
        self.Class = Class

        self.connect_signals()

        self.View.run()

    def connect_signals(self):
        for interactor in self.View.interactors:
            interactor.operation.connect(self.change_right_page)

        for close_button in self.View.close_buttons:
            close_button.clicked.connect(self.View.close_right)

    def change_right_page(self, index):
        if self.View.sw_right.isHidden():
            self.View.sw_right.show()
            
        for interactor in self.View.interactors:
            if interactor.is_active:
                interactor.deactivate()
                break
            
        self.View.interactors[index].activate()
        self.View.sw_right.setCurrentIndex(index)