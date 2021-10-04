from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt

class ListModel(QAbstractListModel):

    def __init__(self, parent, data):
        super().__init__(parent=parent)
        self.parent = parent

        self.data = []
        self.default_size = 0
        if len(data) != 0:
            self.default_size = len(data)
            for datum in data:
                self.data.insert(len(self.data)-1, datum)

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            value = self.data[row]

            return value

    def flags(self, index):
        return Qt.ItemIsEnabled

    def getRowData(self, index):
        if index < self.default_size:
            return None
        return self.data[index]

    def findRow(self, text):
        for index, datum in enumerate(self.data):
            if datum == text:
                return index

    def getData(self):
        return self.data

    def insertRows(self, position, rows, value, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.data.insert(position, value)

        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.data.remove(self.data[position])

        self.endRemoveRows()
        return True

    def editRow(self, position, value):
        self.data[position] = value