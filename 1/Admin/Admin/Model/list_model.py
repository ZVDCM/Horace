from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt

class ListModel(QAbstractListModel):

    def __init__(self, parent, data):
        super().__init__(parent=parent)
        self.parent = parent

        self.data = []
        data.reverse()
        if data:
            for datum in data:
                self.data.append(datum.get_display())

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            value = self.data[row]

            return value

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def getRowData(self, index):
        return self.data[index]

    def findRow(self, text):
        for index, datum in enumerate(self.data):
            if datum == text:
                return index

    def getData(self):
        return self.data

    def insertRows(self, position, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.data.insert(position, "<url>")

        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.data.remove(self.data[position])

        self.endRemoveRows()
        return True