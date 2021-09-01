from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(640, 480)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.show()
        self.setMouseTracking(True)
        self.widget.setMouseTracking(True)
        self.rightClick = False

    def mousePressEvent(self, event):
        super(App, self).mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            self.rdragx = event.x()
            self.rdragy = event.y()
            self.currentx = self.width()
            self.currenty = self.height()
            self.rightClick = True

    def mouseMoveEvent(self, event):
        super(App, self).mouseMoveEvent(event)

        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        width5 = width + 5
        widthm5 = width - 5
        height5 = height + 5
        heightm5 = height - 5

        posMouse = event.pos()
        posMouseX = event.x()
        posMouseY = event.y()

        if posMouseX >= widthm5 and posMouseX <= width5:
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
        elif posMouseX >= -5 and posMouseX <= 5:
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
        elif posMouseY >= heightm5 and posMouseY <= height5:
            QApplication.setOverrideCursor(Qt.SizeVerCursor)
        elif posMouseY >= -5 and posMouseY <= 5:
            QApplication.setOverrideCursor(Qt.SizeVerCursor)
        else:
            QApplication.restoreOverrideCursor()

        if self.rightClick == True:
            x = max(self.widget.minimumWidth(),
                    self.currentx + event.x() - self.rdragx)
            y = max(self.widget.minimumHeight(),
                    self.currenty + event.y() - self.rdragy)
            self.resize(x, y)

    def mouseReleaseEvent(self, event):
        super(App, self).mouseReleaseEvent(event)
        self.rightClick = False


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
