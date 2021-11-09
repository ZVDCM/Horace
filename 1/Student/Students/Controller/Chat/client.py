from PyQt5 import QtCore
from win32api import GetSystemMetrics
from Students.Misc.Functions.window_capture import convert_pil_image_to_QPixmap, screenshot
from Students.Misc.Widgets.file_message_sent import FileMessageSent
from Students.Controller.Stream.client import Client as StreamClient
from PyQt5.QtWidgets import QFileDialog
from Students.Misc.Functions.is_blank import is_blank
from Students.Misc.Widgets.teacher_file_message_received import FileMessageReceived as _FileMessageReceived
from PyQt5.QtCore import QThread, pyqtSignal
from Students.Misc.Functions.messages import *
from Students.Controller.RDC.client import Client as RDCClient
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from PyQt5.QtGui import QPixmap
from Students.Misc.Widgets.pop_up import Popup
from Students.Misc.Functions.relative_path import relative_path
import os
import time
import socket
import platform
import threading
import subprocess


class MessageReceived(QThread):
    operation = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.message = None
        self.sender = None

    def run(self):
        self.operation.emit(self.message, self.sender)
        self.quit()


class FileMessageReceived(QThread):
    operation = pyqtSignal(str, str, bytearray)

    def __init__(self):
        super().__init__()
        self.sender = None
        self.filename = None
        self.data = None

    def run(self):
        self.operation.emit(self.sender, self.filename, self.data)
        self.quit()


class Operation(QThread):
    operation = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        self.operation.emit()
        self.quit()


class Connect(QThread):

    def __init__(self, Client, address):
        super().__init__()
        self.Client = Client
        self.address = address

    def run(self):
        counter = 0
        try:
            while self.Client.View.isVisible():
                try:
                    self.Client.client.connect(self.address)
                    break
                except (OSError, TypeError):
                    counter += 1
                    self.Client.set_meeting_status_handler(
                        'Connecting' + '.' * (counter % 4))
                    time.sleep(0.5)
        except RuntimeError:
            pass
        self.quit()


class Receive(QThread):
    HOST_PATH = os.path.join(os.environ['SystemRoot'], 'SysNative' if platform.architecture()[
                             0] == '32bit' else 'System32', "drivers", "etc", "hosts")
    REDIRECT = "127.0.0.1"
    DETACHED_PROCESS = 0x00000008

    def __init__(self, Client):
        super().__init__()
        self.Client = Client
        self.client_socket = Client.client
        self.blacklisted_sites = []

    def run(self):
        try:
            while self.Client.View.isVisible():
                message = receive_message(self.client_socket)

                if not message:
                    break

                if message['type'] == 'permission':
                    time.sleep(5)
                    break

                elif message['type'] == 'frame':
                    self.StreamClient.last_frame = message['data']
                    frame = convert_pil_image_to_QPixmap(
                        self.StreamClient.last_frame)
                    self.StreamClient.SetFrame.frame = frame
                    self.StreamClient.SetFrame.start()

                elif message['type'] == 'cmd':
                    if message['data'] == 'reconnect':
                        self.Client.Meeting.is_connected = True
                        self.Client.Meeting.is_disconnected = False
                        self.Client.Meeting.is_frozen = False
                        self.StreamClient.start()

                        self.Client.set_meeting_status_handler(
                            f"Teacher {self.Client.ClassTeacher.Teacher} reconnected the screen")

                    elif message['data'] == 'disconnect':
                        self.Client.Meeting.is_connected = False
                        self.Client.Meeting.is_disconnected = True
                        self.StreamClient.stop()
                        self.StreamClient.frames.put('disconnect')

                        if self.Client.Meeting.is_frozen:
                            self.StreamClient.DisconnectScreen.start()

                        self.Client.set_meeting_status_handler(
                            f"Teacher {self.Client.ClassTeacher.Teacher} disconnected the screen")

                    elif message['data'] == 'frozen':
                        self.Client.Meeting.is_frozen = True
                        self.StreamClient.stop()
                        self.StreamClient.frames.put('frozen')
                        self.Client.set_meeting_status_handler(
                            f"Teacher {self.Client.ClassTeacher.Teacher} froze the screen")

                    elif message['data'] == 'thawed':
                        self.Client.Meeting.is_frozen = False
                        self.StreamClient.start()
                        self.Client.set_meeting_status_handler(
                            f"Teacher {self.Client.ClassTeacher.Teacher} thawed the screen")

                    elif message['data'] == 'shutdown':
                        subprocess.call('shutdown /s /f /t 0',
                                            creationflags=self.DETACHED_PROCESS)
                    elif message['data'] == 'restart':
                        subprocess.call('shutdown /r /f /t 0',
                                            creationflags=self.DETACHED_PROCESS)
                    elif message['data'] == 'lock':
                        subprocess.call('rundll32.exe user32.dll,LockWorkStation',
                                            creationflags=self.DETACHED_PROCESS)
                    elif message['data'] == 'start control':
                        self.RDCClient = RDCClient(
                            self.Client.ClassTeacher, self.Client.View)

                        width, height = GetSystemMetrics(0), GetSystemMetrics(1)
                        message = normalize_message('res', (width, height))
                        self.Client.send(message)
                        self.Client.set_meeting_status_handler(
                            f"Teacher {self.Client.ClassTeacher.Teacher} started remote desktop control")

                    elif message['data'] == 'end control':
                        self.RDCClient.stop()
                        self.Client.set_meeting_status_handler(
                            f"Teacher {self.Client.ClassTeacher.Teacher} ended remote desktop control")

                elif message['type'] == 'mouse':
                    mouse = MouseController()
                    if message['data'][0] == 'move':
                        mouse.position = message['data'][1]
                    elif message['data'][0] == 'pressed':
                        if message['data'][1] == 'left':
                            mouse.press(Button.left)
                        if message['data'][1] == 'middle':
                            mouse.press(Button.middle)
                        if message['data'][1] == 'right':
                            mouse.press(Button.right)
                    elif message['data'][0] == 'released':
                        if message['data'][1] == 'left':
                            mouse.release(Button.left)
                        if message['data'][1] == 'middle':
                            mouse.release(Button.middle)
                        if message['data'][1] == 'right':
                            mouse.release(Button.right)
                    elif message['data'][0] == 'scroll':
                        if message['data'][1] == 'up':
                            mouse.scroll(0, 1)
                        if message['data'][1] == 'down':
                            mouse.scroll(0, -1)

                elif message['type'] == 'keyboard':
                    keyboard = KeyboardController()
                    if "pressed" == message['data'][0]:
                        keyboard.press(message['data'][1])
                    if "released" == message['data'][0]:
                        keyboard.release(message['data'][1])

                elif message['type'] == 'time':
                    self.Client.EndLoading.start()
                    self.Client.start_time = message['data']
                    self.Client.SetTime.time = message['data'].toString("hh:mm:ss")
                    self.Client.SetTime.start()
                    self.Client.ShowLabel.start()
                    self.Client.InitScreenshot.start()

                    self.StreamClient = StreamClient(self.client_socket,
                        self.Client.Meeting, self.Client.ClassTeacher, self.Client.Model, self.Client.View, self.Client.Controller)
                    self.Client.set_meeting_status_handler(
                        f"Joined {self.Client.Class.Name}")

                elif message['type'] == 'msg':
                    self.Client.IncrementBadge.start()
                    self.Client.MessageReceived.message = message['data']
                    self.Client.MessageReceived.sender = message['sender']
                    self.Client.MessageReceived.start()
                    self.Client.set_meeting_status_handler(
                        f"Teacher {self.Client.ClassTeacher.Teacher} sent a message")

                elif message['type'] == 'fls':
                    self.Client.IncrementBadge.start()
                    self.Client.FileMessageReceived.sender = message['sender']
                    self.Client.FileMessageReceived.filename = message['data']
                    self.Client.FileMessageReceived.data = message['file']
                    self.Client.FileMessageReceived.start()
                    self.Client.set_meeting_status_handler(
                        f"Teacher {self.Client.ClassTeacher.Teacher} sent a file")

                elif message['type'] == 'url':
                    if self.blacklisted_sites:
                        if len(message['data']) > len(self.blacklisted_sites):
                            self.Client.set_meeting_status_handler(
                                f"Teacher {self.Client.ClassTeacher.Teacher} blacklisted {message['data'][-1]}")
                        else:
                            self.Client.set_meeting_status_handler(
                                f"Teacher {self.Client.ClassTeacher.Teacher} whitelisted {self.blacklisted_sites[-1]}")

                    self.blacklisted_sites = message['data']

                    open(self.HOST_PATH, 'w').close()
                    with open(self.HOST_PATH, 'r+') as hostfile:
                        hosts_content = hostfile.read()
                        for site in self.blacklisted_sites:
                            if site not in hosts_content:
                                hostfile.write(self.REDIRECT +
                                                '\t' + site + '\r\n')
                    subprocess.call('taskkill /f /im chrome.exe',
                                            creationflags=self.DETACHED_PROCESS)
                    subprocess.call('taskkill /f /im iexplore.exe',
                                            creationflags=self.DETACHED_PROCESS)
                    subprocess.call('taskkill /f /im msedge.exe',
                                            creationflags=self.DETACHED_PROCESS)

                elif message['type'] == 'student':
                    new_list_students = message['data']
                    try:
                        old_list_students = self.Client.View.lv_student.model().data

                        if len(new_list_students) > len(old_list_students):
                            self.Client.set_meeting_status_handler(
                                f"{new_list_students[0]} joined the class")
                        else:
                            if len(new_list_students) != 1 or len(new_list_students) == len(old_list_students):
                                self.Client.set_meeting_status_handler(
                                    f"{old_list_students[-1]} left the class")
                    except AttributeError:
                        pass

                    self.Client.SetStudentList.val = new_list_students
                    self.Client.SetStudentList.start()

                elif message['type'] == 'popup':
                    self.Client.set_meeting_status_handler(
                        f'Teacher {self.Client.ClassTeacher.Teacher} sent a popup')
                    message, icon = message['data']
                    if icon == 'Question':
                        self.Client.View.Popup.lbl_icon.setPixmap(QPixmap(relative_path(
                        'Students', ['Misc', 'Resources'], 'question.png')))
                    elif icon == 'Warning':
                        self.Client.View.Popup.lbl_icon.setPixmap(QPixmap(relative_path(
                        'Students', ['Misc', 'Resources'], 'warning.png')))
                    elif icon == 'Critical':
                        self.Client.View.Popup.lbl_icon.setPixmap(QPixmap(relative_path(
                        'Students', ['Misc', 'Resources'], 'critical.png')))
                    else:
                        self.Client.View.Popup.lbl_icon.setPixmap(QPixmap(relative_path(
                        'Students', ['Misc', 'Resources'], 'information.png')))
                    self.Client.View.Popup.lbl_message.setText(message)
                    self.Client.View.Popup.run()
        except RuntimeError:
            pass

        self.quit()


class Screenshot(QThread):
    operation = pyqtSignal()

    def __init__(self, Client):
        super().__init__()
        self.Client = Client
        self.View = Client.View
        self.client_socket = Client.client

    def run(self):
        try:
            while self.View.isVisible() and not self.client_socket._closed:
                try:
                    sct = screenshot()
                except OSError:
                    continue
                message = normalize_message('frame', sct)
                self.Client.send(message)
                time.sleep(2)
        except RuntimeError:
            pass
        self.quit()


class SetTime(QThread):
    operation = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.time = None

    def run(self):
        self.operation.emit(self.time)
        self.quit()


class SetStudentList(QThread):
    operation = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.val = None

    def run(self):
        self.operation.emit(self.val)
        self.quit()


# class Popup(QThread):

#     def __init__(self, fn):
#         super().__init__()
#         self.fn = fn
#         self.val = ()

#     def run(self):
#         self.fn(*self.val)


class SetMeetingStatus(QtCore.QThread):
    operation = QtCore.pyqtSignal(str)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        try:
            self.fn(self.val)
        except RuntimeError:
            pass
        self.quit()


class Client:

    PORT = 43200

    def __init__(self, Meeting, Class, ClassTeacher, Model, View, Controller):
        self.Meeting = Meeting
        self.Class = Class
        self.ClassTeacher = ClassTeacher
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.Sender = Controller.User.Username

        self.start_time = QtCore.QTime(0, 0, 0)
        self.status_time = 0

        self.connect_signals()
        self.init_client()

    def connect_signals(self):
        self.View.closeEvent = self.meeting_closed
        self.View.btn_leave.clicked.connect(self.View.close)

        self.StartLoading = Operation()
        self.StartLoading.operation.connect(self.View.LoadingScreen.run)

        self.EndLoading = Operation()
        self.EndLoading.operation.connect(self.View.LoadingScreen.hide)

        self.MessageReceived = MessageReceived()
        self.MessageReceived.operation.connect(
            self.View.display_message_received)

        self.FileMessageReceived = FileMessageReceived()
        self.FileMessageReceived.operation.connect(
            self.display_file_message_received)

        self.View.txt_message.returnPressed.connect(self.send_message)
        self.View.btn_send.clicked.connect(self.send_message)

        self.View.btn_file.clicked.connect(self.get_file)

        self.ShowLabel = Operation()
        self.ShowLabel.operation.connect(self.View.lbl_timer.show)

        self.SetTime = SetTime()
        self.SetTime.operation.connect(self.View.set_timer)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000)

        self.IncrementBadge = Operation()
        self.IncrementBadge.operation.connect(self.View.BadgeOverlay.increment)

        self.SetStudentList = SetStudentList()
        self.SetStudentList.operation.connect(self.set_student_list)

        self.View.btn_search_student.clicked.connect(self.search)
        self.View.txt_search_student.returnPressed.connect(self.search)
        self.View.lv_student.hideEvent = self.reset_list_target

    def init_client(self):
        self.client = socket.socket()
        address = (self.ClassTeacher.HostAddress, self.PORT)
        self.Connect = Connect(self, address)
        self.Connect.started.connect(self.View.LoadingScreen.run)
        self.Connect.started.connect(
            lambda: self.set_meeting_status_handler('Connecting'))
        self.Connect.finished.connect(self.start)
        self.Connect.start()
        self.InitScreenshot = Screenshot(self)

    def start(self):
        message = normalize_message('section', self.ClassTeacher.Code)
        self.send(message)

        self.Receive = Receive(self)
        self.Receive.finished.connect(self.init_client)
        self.Receive.start()

    def send(self, message):
        try:
            message['sender'] = self.Sender
            message = serialize_message(message)
            send_message(message, self.client)
        except OSError:
            return

    def send_message(self):
        text = self.View.txt_message.text()
        if is_blank(text):
            return
        message = normalize_message('msg', text)
        self.send(message)
        self.View.display_message_sent(text)

    def get_file(self):
        response = QFileDialog.getOpenFileName(
            parent=self.View,
            caption="Select a file",
            directory=os.path.expanduser('~/Documents'),
        )

        if response[0]:
            filename = response[0].split("/")[-1]
            size = os.path.getsize(response[0])

            if size > 131_072_000:
                self.View.run_popup(f'File must be lower than 125mb in size')
                return

            with open(response[0], "rb") as file:
                file = bytearray(file.read())

            message = normalize_message("fls", filename, file=file)
            self.send(message)
            self.display_file_message_sent(filename, file)

    def display_file_message_sent(self, filename, data):
        file_message_sent = FileMessageSent(self.View, filename, data)
        file_message_sent.operation.connect(self.download_file)
        self.View.verticalLayout_6.insertWidget(
            self.View.verticalLayout_6.count()-1, file_message_sent)

    def display_file_message_received(self, sender, filename, data):
        file_message_received = _FileMessageReceived(
            self.View, sender, filename, data)
        file_message_received.operation.connect(self.download_file)
        self.View.verticalLayout_6.insertWidget(
            self.View.verticalLayout_6.count()-1, file_message_received)

    def download_file(self, data, filename):
        path = os.path.join(os.path.expanduser('~/Documents'), filename)
        ext = filename.split('.')[-1]
        path = QFileDialog.getSaveFileName(
            self.View, 'Save File', path, ext)[0]
        if path:
            self.Controller.SignInController.SignIn.View.show_alert('file', 'Downloading file...')
            with open(path, 'wb') as file:
                file.write(data)
            self.Controller.SignInController.SignIn.View.show_alert('file', 'File downloaded')

    def timer_event(self):
        self.start_time = self.start_time.addSecs(1)
        self.SetTime.time = self.start_time.toString("hh:mm:ss")
        self.SetTime.start()

        self.status_time += 1
        if self.status_time == 5:
            self.View.lbl_meeting_status.clear()

    def meeting_closed(self, event):
        self.client.close()

        try:
            if self.Controller.View.Lobby.isVisible():
                self.Controller.Lobby.enable_classes()
                if self.View.isVisible():
                    self.View.close()
        except RuntimeError:
            self.Controller.SignInController.View.init_sign_in()
            self.Controller.SignInController.Model.init_sign_in()
            self.Controller.SignInController.init_sign_in()
        
        if self.Connect.isRunning():
            self.Connect.terminate()
        self.timer.stop()

    def set_student_list(self, students):
        student_model = self.Model.ListModel(self.View.lv_student, students)
        self.View.lv_student.setModel(student_model)

    def set_meeting_status_handler(self, status):
        self.status_time = 0
        threading.Thread(target=self.View.set_meeting_status, args=(status,), daemon=True).start()

    def search(self):
        target_student = self.View.txt_search_student.text()
        student_model = self.View.lv_student.model()
        students = student_model.data
        target_indices = []
        for index, student in enumerate(students):
            if target_student in student:
                target_indices.append(index)
            self.View.lv_student.setRowHidden(index, True)

        for target_index in target_indices:
            self.View.lv_student.setRowHidden(target_index, False)

        self.View.txt_search_student.clear()

    def reset_list_target(self, event):
        self.View.txt_search_student.clear()
        student_model = self.View.lv_student.model()
        students = student_model.data
        for index, student in enumerate(students):
            self.View.lv_student.setRowHidden(index, False)