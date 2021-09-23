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
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
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
        while self.Client.View.isVisible():
            try:
                self.Client.client.connect(self.address)
                break
            except:
                print('Connecting')
                time.sleep(2)
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

    def run(self):
        while True:
            message = receive_message(self.client_socket)

            if not message:
                break

            if message['type'] == 'cmd':
                if message['data'] == 'reconnect':
                    self.Client.Meeting.is_connected = True
                    self.Client.Meeting.is_disconnected = False
                    self.Client.Meeting.is_frozen = False
                    self.StreamClient.start()

                elif message['data'] == 'disconnect':
                    self.Client.Meeting.is_connected = False
                    self.Client.Meeting.is_disconnected = True
                    self.StreamClient.stop()

                elif message['data'] == 'frozen':
                    self.Client.Meeting.is_frozen = True
                    self.StreamClient.stop()

                elif message['data'] == 'thawed':
                    self.Client.Meeting.is_frozen = False
                    self.StreamClient.start()

                elif message['data'] == 'shutdown':
                    print(message['data'])
                    # subprocess.call('shutdown /s /f /t 0',
                    #                     creationflags=self.DETACHED_PROCESS)
                elif message['data'] == 'restart':
                    print(message['data'])
                    # subprocess.call('shutdown /r /f /t 0',
                    #                     creationflags=self.DETACHED_PROCESS)
                elif message['data'] == 'lock':
                    print(message['data'])
                    # subprocess.call('rundll32.exe user32.dll,LockWorkStation',
                    #                     creationflags=self.DETACHED_PROCESS)
                elif message['data'] == 'start control':
                    self.RDCClient = RDCClient(self.Client.Class, self.Client.View)

                    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
                    message = normalize_message('res', (width, height))
                    self.Client.send(message)

                elif message['data'] == 'end control':
                    self.RDCClient.stop()

            elif message['type'] == 'frame':
                self.StreamClient.last_frame = message['data']
                frame = convert_pil_image_to_QPixmap(self.StreamClient.last_frame)
                self.StreamClient.SetFrame.frame = frame
                self.StreamClient.SetFrame.start()

            # elif message['type'] == 'mouse':
            #     print(message)
                # mouse = MouseController()
                # if message['data'][0] == 'move':
                #     mouse.position = message['data'][1]
                # elif message['data'][0] == 'pressed':
                #     if message['data'][1] == 'left':
                #         mouse.press(Button.left)
                #     if message['data'][1] == 'middle':
                #         mouse.press(Button.middle)
                #     if message['data'][1] == 'right':
                #         mouse.press(Button.right)
                # elif message['data'][0] == 'released':
                #     if message['data'][1] == 'left':
                #         mouse.release(Button.left)
                #     if message['data'][1] == 'middle':
                #         mouse.release(Button.middle)
                #     if message['data'][1] == 'right':
                #         mouse.release(Button.right)
                # elif message['data'][0] == 'scroll':
                #     if message['data'][1] == 'up':
                #         mouse.scroll(0, 1)
                #     if message['data'][1] == 'down':
                #         mouse.scroll(0, -1)

            # elif message['type'] == 'keyboard':
                # print(message['data'])
                # keyboard = KeyboardController()
                # if "pressed" == message['data'][0]:
                #     keyboard.press(message['data'][1])
                # if "released" == message['data'][0]:
                #     keyboard.release(message['data'][1])

            elif message['type'] == 'time':
                self.Client.EndLoading.start()
                self.Client.start_time = message['data']
                self.Client.SetTime.time = message['data'].toString("hh:mm:ss")
                self.Client.SetTime.start()
                self.Client.ShowLabel.start()

                self.StreamClient = StreamClient(
                    self.Client.Meeting, self.Client.Class, self.Client.Model, self.Client.View, self.Client.Controller)

            elif message['type'] == 'msg':
                self.Client.IncrementBadge.start()
                self.Client.MessageReceived.message = message['data']
                self.Client.MessageReceived.sender = message['sender']
                self.Client.MessageReceived.start()

            elif message['type'] == 'fls':
                self.Client.IncrementBadge.start()
                self.Client.FileMessageReceived.sender = message['sender']
                self.Client.FileMessageReceived.filename = message['data']
                self.Client.FileMessageReceived.data = message['file']
                self.Client.FileMessageReceived.start()

        self.quit()


class SetTime(QThread):
    operation = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.time = None

    def run(self):
        self.operation.emit(self.time)
        self.quit()


class Client:

    PORT = 43200
    start_time = QtCore.QTime(0, 0, 0)

    def __init__(self, Meeting, Class, Model, View, Controller):
        self.Meeting = Meeting
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.Sender = Controller.User.Username
        self.connect_signals()
        self.init_client()

    def connect_signals(self):
        self.View.closeEvent = self.meeting_closed

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

        self.Timer = QtCore.QTimer()
        self.Timer.timeout.connect(self.timer_event)
        self.Timer.start(1000)

        self.IncrementBadge = Operation()
        self.IncrementBadge.operation.connect(self.View.BadgeOverlay.increment)

    def init_client(self):
        self.client = socket.socket()
        address = (self.Class.HostAddress, self.PORT)
        self.connect_handler = Connect(self, address)
        self.connect_handler.started.connect(self.View.LoadingScreen.run)
        self.connect_handler.finished.connect(self.start)
        self.connect_handler.start()

    def start(self):
        message = normalize_message('section', self.Class.Code)
        self.send(message)

        self.Receive = Receive(self)
        self.Receive.finished.connect(self.init_client)
        self.Receive.start()

        send_screenshot_thread = threading.Thread(
            target=self.send_screenshot, daemon=True, name='ChatScreenshotThread')
        send_screenshot_thread.start()

    def send_screenshot(self):
        while self.View.isVisible():
            sct = screenshot()
            message = normalize_message('frame', sct)
            self.send(message)
            time.sleep(2)

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
                print('file exceeds 125mb limit')
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
            with open(path, 'wb') as file:
                file.write(data)

    def timer_event(self):
        self.start_time = self.start_time.addSecs(1)
        self.SetTime.time = self.start_time.toString("hh:mm:ss")
        self.SetTime.start()

    def meeting_closed(self, event):
        self.client.close()
