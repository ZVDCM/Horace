from os import read
import threading
from Teachers.Misc.Functions.messages import *
import socket
import select
import queue
from PyQt5.QtCore import QThread, pyqtSignal
from Teachers.Misc.Widgets.message_received import MessageReceived as _MessageReceived


class NotMessage(Exception):
    pass
class FromDifferentClass(Exception):
    pass

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


class Host:

    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 43200
    ADDR = (HOST, PORT)
    target = None
    messages = {}
    inputs = []
    outputs = []
    clients_name = {}
    clients_socket = {}

    def __init__(self, Class, Model, View, Controller):
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.Sender = Controller.User.Username
        self.connect_signals()
        self.init_host()

    def connect_signals(self):
        self.View.txt_message.returnPressed.connect(self.send_message)

        self.MessageReceived = MessageReceived()
        self.MessageReceived.operation.connect(self.display_message_received)

        self.View.btn_close_reply.clicked.connect(self.hide_reply)

    def init_host(self):
        self.host = socket.socket()
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host.bind(self.ADDR)
        self.host.listen()
        self.inputs.append(self.host)

        self.handler_thread = threading.Thread(target=self.handler, daemon=True, name='ChatHandler')
        self.handler_thread.start()

    def handler(self):
        while self.inputs:
            readables, writables, exceptionals = select.select(
                self.inputs, self.outputs, self.inputs)

            for readable in readables:
                if not self.host_readable(readable):
                    self.client_readable(readable)

            for writable in writables:
                try:
                    message = self.messages[writable].get_nowait()
                except:
                    continue
                self.client_writable(message, writable)

            for exceptional in exceptionals:
                self.exceptional(exceptional)

        self.quit()

    def host_readable(self, readable):
        if readable is not self.host:
            return False

        client_socket, client_address = readable.accept()
        self.inputs.append(client_socket)
        self.messages[client_socket] = queue.Queue()

        return True

    def client_readable(self, readable):
        try:
            message = receive_message(readable)

            if not message:
                raise NotMessage

            if readable not in self.outputs:
                self.outputs.append(readable)

            if message['type'] == 'section':
                if message['data'] == self.Class.Code:
                    self.clients_name[readable] = message['sender']
                    self.clients_socket[message['sender']] = readable
                    self.set_message('cmd', 'connect', target=message['sender'])
                else:
                    raise FromDifferentClass

            elif message['type'] == 'msg':
                self.MessageReceived.message = message['data']
                self.MessageReceived.sender = message['sender']
                self.MessageReceived.start()

        except (NotMessage, FromDifferentClass):
            self.inputs.remove(readable)
            if readable in self.outputs:
                self.outputs.remove(readable)
            if readable in self.clients_name.keys():
                del self.clients_name[readable]
            if readable in self.clients_socket.keys():
                del self.clients_socket[readable]
            readable.close()

    def client_writable(self, message, writable):
        if writable._closed:
            return
        message = serialize_message(message)
        send_message(message, writable)

    def exceptional(self, exceptional):
        self.inputs.remove(exceptional)
        if exceptional in self.outputs:
            self.outputs.remove(exceptional)
        if exceptional in self.clients_name.keys():
                del self.clients_name[exceptional]
        if exceptional in self.clients_socket.keys():
            del self.clients_socket[exceptional]
        exceptional.close()

    def set_message(self, type, message, target=None):
        message = normalize_message(type, message, target=target, sender=self.Sender)
        if target:
            self.messages[self.clients_socket[target]].put(message)
        else:
            for client in self.messages.keys():
                self.messages[client].put(message)

    def send_message(self):
        text = self.View.txt_message.text()
        if self.View.w_reply.isVisible():
            target = self.View.lbl_reply.text().removeprefix('Replying to ')
            self.set_message('msg', text, target=target)
        else:
            self.set_message('msg', text)
        self.View.display_message_sent(text)

    def display_message_received(self, text, sender):
        message_received = _MessageReceived(self.View, text, sender)
        message_received.operation.connect(self.target_message)
        self.View.verticalLayout_10.insertWidget(
            self.View.verticalLayout_10.count()-1, message_received)
        self.View.w_reply.hide()

    def target_message(self, sender):
        self.target = sender
        self.View.lbl_reply.setText(f"Replying to {sender}")
        self.View.w_reply.show()

    def hide_reply(self):
        self.target = None
        self.View.w_reply.hide()