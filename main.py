import SignIn.Controller.controller as SignIn
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    SignInController = SignIn.Controller()
    sys.exit(app.exec_())

# TestTest!1
# 1136, 884
# self.parent.width()
# self.parent.height()
# self.parent.setWindowState(QtCore.Qt.WindowNoState)