from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtCore import Qt

class TableView(QTableView):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.verticalHeader().setMinimumSectionSize(40)
        self.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setSelectionMode(
            QAbstractItemView.SingleSelection)
        self.setWordWrap(False)