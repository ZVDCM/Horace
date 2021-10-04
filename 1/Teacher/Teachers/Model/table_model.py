from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel


class TableModel(QAbstractTableModel):

    def __init__(self, parent, data):
        super().__init__(parent=parent)
        self.parent = parent

        self.data = []
        if len(data) != 0:
            for datum in data:
                self.data.insert(len(self.data), datum)

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data[0])

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.data[row][column]

            self.dataChanged.emit(index, index)
            return str(value)
