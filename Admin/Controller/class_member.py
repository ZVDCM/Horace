class ClassMember:

    def __init__(self, Model, View, Contoller):
        self.Model = Model
        self.View = View
        self.Contoller = Contoller

        self.target_class_row = None
        self.TargetClass = None

        self.connect_signals()

    def connect_signals(self):
        pass
    
    # Table
    def set_class_table(self, classes):
        class_model = self.Model.TableModel(
            self.View.tv_class, classes, self.Model.Class.get_headers())
        self.View.tv_class.setModel(class_model)
        self.View.tv_class.horizontalHeader().setMinimumSectionSize(150)