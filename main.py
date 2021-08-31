import SignIn.Controller.controller as SignIn
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    SignInController = SignIn.Controller()
    sys.exit(app.exec_())

# TestTest!1
# self.View.run_loading_screen
# self.View.stop_loading_screen
# self.Controller.init_register_admin
# self.Controller.View.init_register_admin
# self.Model.register_admin
# self.View.txt_repeat_password.text()
# self.Model.register_admin_qna
# self.View.question_and_answer