class BlacklistURL:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.connect_signals()

    def connect_signals(self):
        # Add
        self.View.btn_init_add_url.clicked.connect(self.View.disable_url_buttons)
        self.View.btn_init_add_url.clicked.connect(self.View.enable_url_inputs)
        self.View.btn_init_add_url.clicked.connect(self.View.w_url_btn.show)

        # Edit
        
        # Cancel
        self.View.btn_cancel_url.clicked.connect(self.View.w_url_btn.hide)
        self.View.btn_cancel_url.clicked.connect(self.View.disable_url_inputs)
        self.View.btn_cancel_url.clicked.connect(self.View.enable_url_buttons)