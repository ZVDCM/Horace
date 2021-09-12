import threading
import time
import socket
import queue
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
                if message['data'] == 'connect':
                    self.Client.EndLoading.start()
                    self.Client.send('name', self.Client.Sender)

            elif message['type'] == 'msg':
                self.Client.MessageReceived.message = message['data']
                self.Client.MessageReceived.sender = message['sender']
                self.Client.MessageReceived.start()

        self.quit()

class Client:

    PORT = 43200

    def __init__(self, Class, Model, View, Controller):
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.Sender = Controller.User.Username
        self.connect_signals()
        self.init_connection()

    def connect_signals(self):
        self.StartLoading = Operation()
        self.StartLoading.operation.connect(self.View.LoadingScreen.run)

        self.EndLoading = Operation()
        self.EndLoading.operation.connect(self.View.LoadingScreen.hide)

        self.MessageReceived = MessageReceived()
        self.MessageReceived.operation.connect(self.View.display_message_received)

        self.View.txt_message.returnPressed.connect(self.send_message)

    def init_connection(self):
        self.client = socket.socket()
        address = (self.Class.HostAddress, self.PORT)
        self.connect_handler = Connect(self.client, address)
        self.connect_handler.started.connect(self.View.LoadingScreen.run)
        self.connect_handler.finished.connect(self.start)
        self.connect_handler.start()

    def start(self):
        self.send('section', self.Class.Code)

        self.Receive = Receive(self)
        self.Receive.finished.connect(self.init_connection)
        self.Receive.start()

    def send(self, type, message):
        message = serialize_message(normalize_message(type, message, sender=self.Sender))
        send_message(message, self.client)

    def send_message(self):
        text = self.View.txt_message.text()
        self.send('msg', text)
        self.View.display_message_sent(text)