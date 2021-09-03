from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel


class TableModel(QAbstractTableModel):

    def __init__(self, parent, data, headers):
        super().__init__(parent=parent)
        self.parent = parent
        self.headers = headers

        self.data = [["NULL" for i in range(len(self.headers))]]
        if len(data) != 0:
            for index, datum in enumerate(data):
                self.data.insert(len(self.data)-1, datum.get_values())

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.data[0])

    def findRow(self, text, pos):
        indices = []
        for index, user in enumerate(self.data):
            if text in user and user.index(text) == pos:
                indices.append(index)
        return indices

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.data[row][column]

            if type(value) is bytes:
                return "BLOB"

            self.dataChanged.emit(index, index)
            return str(value)

    def getData(self):
        return self.data

    def getRowData(self, row):
        return self.data[row]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:

                if section < len(self.headers):
                    return self.headers[section]
            else:
                if section == len(self.data) - 1:
                    return '⁕'
                return str(section)

    def insertRow(self, new_user, parent=QModelIndex()):
        first = len(self.data)-1
        self.beginInsertRows(parent, first, first)
        self.data.insert(first, new_user)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self.data[position]
            self.data.remove(value)

        self.endRemoveRows()
        return True
