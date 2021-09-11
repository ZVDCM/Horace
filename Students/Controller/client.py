import threading
import time
import socket
import queue
from PyQt5.QtCore import QThread, pyqtSignal
from Students.Misc.Functions.messages import *


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
        self.Controller = Client.Controller

    def run(self):
        while True:
            message = receive_message(self.client_socket)

            if not message:
                break
            if message['type'] == 'cmd':
                if message['data'] == 'connect':
                    self.Client.end_loading.start()
                    self.Client.set_message(
                        'name', self.Controller.User.Username)
                    self.Client.send()

            elif message['type'] == 'msg':
                print(message['data'])

        self.quit()

class Client:

    PORT = 43200
    messages = queue.Queue()

    def __init__(self, Class, Model, View, Controller):
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.connect_signals()
        self.init_connection()

    def connect_signals(self):
        self.start_loading = Operation()
        self.start_loading.operation.connect(self.View.LoadingScreen.run)

        self.end_loading = Operation()
        self.end_loading.operation.connect(self.View.LoadingScreen.hide)

    def init_connection(self):
        self.client = socket.socket()
        address = (self.Class.HostAddress, self.PORT)
        self.connect_handler = Connect(self.client, address)
        self.connect_handler.started.connect(self.View.LoadingScreen.run)
        self.connect_handler.finished.connect(self.start)
        self.connect_handler.start()

    def start(self):
        self.set_message('section', self.Class.Code)
        self.send()

        self.Receive = Receive(self)
        self.Receive.finished.connect(self.init_connection)
        self.Receive.start()

    def send(self):
        message = self.messages.get()
        send_message(message, self.client)

    def set_message(self, type, message):
        message = serialize_message(normalize_message(type, message))
        self.messages.put(message)
