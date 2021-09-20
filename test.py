from PyQt5.QtCore import Qt, QRect, QPoint, QEvent
from PyQt5.QtWidgets import (QLabel, QMainWindow, QApplication, QSizePolicy,
                             QVBoxLayout, QWidget, QHBoxLayout, QPushButton)
from enum import Enum


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.createCostumTitleBar()

        self.setContentsMargins(0, 0, 0, 0)

        self.central = QWidget()
        self.central.setStyleSheet("background-color: #f8ecdf")

        self.centralLayout = QVBoxLayout()
        self.central.setLayout(self.centralLayout)
        self.centralLayout.addWidget(
            self.costumsystemmenu, alignment=Qt.AlignTop)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self.central)

        # Set the minimum size to avoid window being resized too small.

        self.setMinimumSize(300, 400)
        self.minheight = self.minimumHeight()
        self.minwidth = self.minimumWidth()

        self.resize(300, 400)

        # make sure your minium size have the same aspect ratio as the step.
        self.stepY = 4
        self.stepX = 3

        # install the event filter on this window.
        self.installEventFilter(self)
        self.grabarea.installEventFilter(self)

        self.cursorpos = CursorPos.DEFAULT
        self.iswindowpress = False

    def createCostumTitleBar(self):
        self.costumsystemmenu = QWidget()
        self.costumsystemmenu.setStyleSheet("background-color: #ccc")
        self.costumsystemmenu.setContentsMargins(0, 0, 0, 0)
        self.costumsystemmenu.setMinimumHeight(30)

        self.grabarea = QLabel("")
        self.grabarea.setStyleSheet("background-color: #ccc")
        self.grabarea.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)

        titlebarlayout = QHBoxLayout()
        titlebarlayout.setContentsMargins(11, 11, 11, 11)
        titlebarlayout.setSpacing(0)

        self.closeButton = QPushButton("X")
        self.closeButton.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.closeButton.clicked.connect(self.close)

        self.costumsystemmenu.setLayout(titlebarlayout)
        titlebarlayout.addWidget(self.grabarea)
        titlebarlayout.addWidget(self.closeButton, alignment=Qt.AlignRight)

        self.istitlebarpress = False

    def eventFilter(self, object, event):
        # The eventFilter() function must return true if the event
        # should be filtered, (i.e. stopped); otherwise it must return false.
        # https://doc.qt.io/qt-5/qobject.html#eventFilter

        # check if the object is the mainwindow.
        if object == self:

            if event.type() == QEvent.HoverMove:
                if not self.iswindowpress:
                    self.setCursorShape(event)
                return True

            elif event.type() == QEvent.MouseButtonPress:
                self.iswindowpress = True
                # Get the position of the cursor and map to the global coordinate of the widget.
                self.globalpos = self.mapToGlobal(event.pos())
                self.origingeometry = self.geometry()

                return True

            elif event.type() == QEvent.MouseButtonRelease:
                self.iswindowpress = False
                return True

            elif event.type() == QEvent.MouseMove:
                if self.cursorpos != CursorPos.DEFAULT and self.iswindowpress:
                    self.resizing(self.globalpos, event,
                                  self.origingeometry, self.cursorpos)

                return True

            else:
                return False

        elif object == self.grabarea:
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton and self.iswindowpress == False:
                    self.oldpos = event.globalPos()
                    self.oldwindowpos = self.pos()
                    self.istitlebarpress = True

                return True
            elif event.type() == QEvent.MouseButtonRelease:
                self.istitlebarpress = False
                return True
            elif event.type() == QEvent.MouseMove:
                if (self.istitlebarpress):
                    distance = event.globalPos()-self.oldpos
                    newwindowpos = self.oldwindowpos + distance
                    self.move(newwindowpos)
                return True
            else:
                return False
        else:
            return False

    # Change the cursor shape when the cursor is over different part of the window.
    def setCursorShape(self, event, handlersize=11):
        rect = self.rect()
        topLeft = rect.topLeft()
        topRight = rect.topRight()
        bottomLeft = rect.bottomLeft()
        bottomRight = rect.bottomRight()

        # get the position of the cursor
        pos = event.pos()

        # make the resize handle include some space outside the window,
        # can avoid user move too fast and loss the handle.
        # top handle
        if pos in QRect(QPoint(topLeft.x()+handlersize, topLeft.y()-2*handlersize),
                        QPoint(topRight.x()-handlersize, topRight.y()+handlersize)):
            self.setCursor(Qt.SizeVerCursor)
            self.cursorpos = CursorPos.TOP

        # bottom handle
        elif pos in QRect(QPoint(bottomLeft.x()+handlersize, bottomLeft.y()-handlersize),
                          QPoint(bottomRight.x()-handlersize, bottomRight.y()+2*handlersize)):
            self.setCursor(Qt.SizeVerCursor)
            self.cursorpos = CursorPos.BOTTOM

        # right handle
        elif pos in QRect(QPoint(topRight.x()-handlersize, topRight.y()+handlersize),
                          QPoint(bottomRight.x()+2*handlersize, bottomRight.y()-handlersize)):
            self.setCursor(Qt.SizeHorCursor)
            self.cursorpos = CursorPos.RIGHT

        # left handle
        elif pos in QRect(QPoint(topLeft.x()-2*handlersize, topLeft.y()+handlersize),
                          QPoint(bottomLeft.x()+handlersize, bottomLeft.y()-handlersize)):
            self.setCursor(Qt.SizeHorCursor)
            self.cursorpos = CursorPos.LEFT

        # topRight handle
        elif pos in QRect(QPoint(topRight.x()-handlersize, topRight.y()-2*handlersize),
                          QPoint(topRight.x()+2*handlersize, topRight.y()+handlersize)):
            self.setCursor(Qt.SizeBDiagCursor)
            self.cursorpos = CursorPos.TOPRIGHT

        # topLeft handle
        elif pos in QRect(QPoint(topLeft.x()-2*handlersize, topLeft.y()-2*handlersize),
                          QPoint(topLeft.x()+handlersize, topLeft.y()+handlersize)):
            self.setCursor(Qt.SizeFDiagCursor)
            self.cursorpos = CursorPos.TOPLEFT

        # bottomRight handle
        elif pos in QRect(QPoint(bottomRight.x()-handlersize, bottomRight.y()-handlersize),
                          QPoint(bottomRight.x()+2*handlersize, bottomRight.y()+2*handlersize)):
            self.setCursor(Qt.SizeFDiagCursor)
            self.cursorpos = CursorPos.BOTTOMRIGHT

        # bottomLeft handle
        elif pos in QRect(QPoint(bottomLeft.x()-2*handlersize, bottomLeft.y()-handlersize),
                          QPoint(bottomLeft.x()+handlersize, bottomLeft.y()+2*handlersize)):
            self.setCursor(Qt.SizeBDiagCursor)
            self.cursorpos = CursorPos.BOTTOMLEFT

        # Default is the arrow cursor.
        else:
            self.setCursor(Qt.ArrowCursor)
            self.cursorpos = CursorPos.DEFAULT

    def resizing(self, originpos, event, geo, cursorpos):
        newpos = self.mapToGlobal(event.pos())

        # find the distance between new and old cursor position.
        dist = newpos - originpos

        # calculate the steps to grow or srink.
        if cursorpos in [CursorPos.TOP, CursorPos.BOTTOM,
                         CursorPos.TOPRIGHT,
                         CursorPos.BOTTOMLEFT, CursorPos.BOTTOMRIGHT]:
            steps = dist.y()//self.stepY
        elif cursorpos in [CursorPos.LEFT, CursorPos.TOPLEFT, CursorPos.RIGHT]:
            steps = dist.x()//self.stepX

        # if the distance moved is too stort, grow or srink by 1 step.
        if steps == 0:
            steps = -1 if dist.y() < 0 or dist.x() < 0 else 1

        oldwidth = geo.width()
        oldheight = geo.height()

        oldX = geo.x()
        oldY = geo.y()

        if cursorpos in [CursorPos.TOP, CursorPos.TOPRIGHT]:

            width = oldwidth - steps * self.stepX
            height = oldheight - steps * self.stepY

            newX = oldX
            newY = oldY + (steps * self.stepY)

            # check if the new size is within the size limit.
            if height >= self.minheight and width >= self.minwidth:
                self.setGeometry(newX, newY, width, height)

        elif cursorpos in [CursorPos.BOTTOM, CursorPos.RIGHT, CursorPos.BOTTOMRIGHT]:

            width = oldwidth + steps * self.stepX
            height = oldheight + steps * self.stepY

            self.resize(width, height)

        elif cursorpos in [CursorPos.LEFT, CursorPos.BOTTOMLEFT]:

            width = oldwidth - steps * self.stepX
            height = oldheight - steps * self.stepY

            newX = oldX + steps * self.stepX
            newY = oldY

            # check if the new size is within the size limit.
            if height >= self.minheight and width >= self.minwidth:
                self.setGeometry(newX, newY, width, height)

        elif cursorpos == CursorPos.TOPLEFT:

            width = oldwidth - steps * self.stepX
            height = oldheight - steps * self.stepY

            newX = oldX + steps * self.stepX
            newY = oldY + steps * self.stepY

            # check if the new size is within the size limit.
            if height >= self.minheight and width >= self.minwidth:
                self.setGeometry(newX, newY, width, height)

        else:
            pass

# cursor position
class CursorPos(Enum):
    TOP = 1
    BOTTOM = 2
    RIGHT = 3
    LEFT = 4
    TOPRIGHT = 5
    TOPLEFT = 6
    BOTTOMRIGHT = 7
    BOTTOMLEFT = 8
    DEFAULT = 9


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())