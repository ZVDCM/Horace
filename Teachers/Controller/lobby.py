class Lobby:

    def __init__(self, Controller):
        self.Model = Controller.Model
        self.View = Controller.View.Lobby
        self.Controller = Controller

        self.connect_signals()

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
