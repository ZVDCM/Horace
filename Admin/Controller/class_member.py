class ClassMember:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.connect_signals()

    def connect_signals(self):
        self.View.btn_init_class_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_class, 1)
        )

        self.View.btn_back_class_bulk.clicked.connect(
            lambda: self.change_table_bulk(self.View.sw_class, 0)
        )
        
        # Add
        self.View.btn_init_add_class.clicked.connect(self.View.disable_class_buttons)
        self.View.btn_init_add_class.clicked.connect(self.View.enable_class_inputs)
        self.View.btn_init_add_class.clicked.connect(self.View.w_class_btn.show)

        # Edit
        
        # Cancel
        self.View.btn_cancel_class.clicked.connect(self.View.w_class_btn.hide)
        self.View.btn_cancel_class.clicked.connect(self.View.disable_class_inputs)
        self.View.btn_cancel_class.clicked.connect(self.View.enable_class_buttons)

    def change_table_bulk(self, target, index):
        target.setCurrentIndex(index)