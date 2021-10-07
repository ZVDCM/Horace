from PyQt5 import QtCore, QtGui, QtWidgets

class ScreenViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._photo.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#0B1A30")))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        try:
            rect = QtCore.QRectF(self._photo.pixmap().rect())
            if not rect.isNull():
                self.setSceneRect(rect)
                if self.hasPhoto():
                    unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                    self.scale(1 / unity.width(), 1 / unity.height())
                    viewrect = self.viewport().rect()
                    scenerect = self.transform().mapRect(rect)
                    factor = min(viewrect.width() / scenerect.width(),
                                viewrect.height() / scenerect.height())
                    self.scale(factor, factor)
                self.zoom = 0
        except RuntimeError:
            return

    def setFrame(self, pixmap=None):
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self.zoom += 1
            else:
                factor = 0.8
                self.zoom -= 1
            if self.zoom > 0:
                self.scale(factor, factor)
            elif self.zoom == 0:
                self.fitInView()
            else:
                self.zoom = 0

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super().mousePressEvent(event)