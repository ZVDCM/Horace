class BlacklistURL:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.target_url_row = None
        self.TargetUrl = None

        self.connect_signals()

    def connect_signals(self):
        pass

    def set_url_list(self, urls):
        url_model = self.Model.ListModel(
            self.View.lv_url, urls)
        self.View.lv_url.setModel(url_model)