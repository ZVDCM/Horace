import queue
import threading

from PyQt5 import QtCore
from Students.Misc.Functions.window_capture import screenshot
from Students.Misc.Widgets.file_message_sent import FileMessageSent
import os
from Students.Controller.Stream.client import Client as StreamClient
from PyQt5.QtWidgets import QFileDialog
from Students.Misc.Functions.is_blank import is_blank
from Students.Misc.Widgets.teacher_file_message_received import FileMessageReceived as _FileMessageReceived
import time
import socket
from PyQt5.QtCore import QThread, pyqtSignal
from Students.Misc.Functions.messages import *


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

    def __init__(self, client, address):
        super().__init__()
        self.client = client
        self.address = address

    def run(self):
        while True:
            try:
                self.client.connect(self.address)
                break
            except:
                print('Connecting')
                time.sleep(2)
        self.quit()


class Receive(QThread):

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
                    self.StreamClient.start_displaying()

                elif message['data'] == 'disconnect':
                    self.StreamClient.frames.put(message['data'])

                elif message['data'] == 'frozen':
                    print('frozen')

                elif message['data'] == 'thawed':
                    self.StreamClient.frames = queue.Queue()

            elif message['type'] == 'time':
                self.Client.EndLoading.start()
                self.Client.start_time = message['data']
                self.Client.SetTime.time = message['data'].toString("hh:mm:ss")
                self.Client.SetTime.start()

                self.StreamClient = StreamClient(
                    self.Client.Class, self.Client.Model, self.Client.View, self.Client.Controller)

            elif message['type'] == 'msg':
                self.Client.MessageReceived.message = message['data']
                self.Client.MessageReceived.sender = message['sender']
                self.Client.MessageReceived.start()

            elif message['type'] == 'fls':
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

    def __init__(self, Class, Model, View, Controller):
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.Sender = Controller.User.Username
        self.connect_signals()
        self.init_client()

    def connect_signals(self):
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
        self.SetTime.finished.connect(self.ShowLabel.start)

        self.Timer = QtCore.QTimer()
        self.Timer.timeout.connect(self.timer_event)
        self.Timer.start(1000)

    def init_client(self):
        self.client = socket.socket()
        address = (self.Class.HostAddress, self.PORT)
        self.connect_handler = Connect(self.client, address)
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
        while True:
            if self.client._closed:
                return
            sct = screenshot()
            message = normalize_message('frame', sct)
            self.send(message)
            time.sleep(2)

    def send(self, message):
        message['sender'] = self.Sender
        message = serialize_message(message)
        send_message(message, self.client)

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
