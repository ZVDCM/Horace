from Teachers.Misc.Functions.window_capture import convert_pil_image_to_QPixmap
from PIL import Image
from PyQt5.QtGui import QPixmap
from Teachers.Misc.Widgets.student_item import StudentItem as _StudentItem
from Teachers.Misc.Widgets.file_message_sent import FileMessageSent
from Teachers.Misc.Widgets.file_message_received import FileMessageReceived as _FileMessageReceived
from Teachers.Misc.Widgets.replied_file_message_sent import RepliedFileMessageSent
import os
from PyQt5.QtWidgets import QFileDialog
from Teachers.Misc.Functions.is_blank import is_blank
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

class StudentItem(QThread):
    operation = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.name = None

    def run(self):
        self.operation.emit(self.name)
        self.quit()

class SetStudentFrame(QThread):
    operation = pyqtSignal(str, QPixmap)

    def __init__(self):
        super().__init__()
        self.name = None
        self.frame = None

    def run(self):
        self.operation.emit(self.name, self.frame)
        self.quit()


class Host:

    PORT = 43200
    target = None
    messages = {}
    inputs = []
    outputs = []
    clients_name = {}
    clients_socket = {}

    def __init__(self, Meeting, Class, Model, View, Controller):
        self.Meeting = Meeting
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.Sender = Controller.User.Username
        self.connect_signals()
        self.init_host()

    def connect_signals(self):
        self.View.txt_message.returnPressed.connect(self.send_message)
        self.View.btn_send.clicked.connect(self.send_message)
        self.View.btn_close_reply.clicked.connect(self.hide_reply)
        self.View.btn_file.clicked.connect(self.get_file)
        self.View.Overlay.reconnect.connect(self.reconnect)
        self.View.Overlay.disconnect.connect(self.disconnect)
        self.View.Overlay.btn_freeze.clicked.connect(self.freeze)

        self.MessageReceived = MessageReceived()
        self.MessageReceived.operation.connect(self.display_message_received)

        self.FileMessageReceived = FileMessageReceived()
        self.FileMessageReceived.operation.connect(self.display_file_message_received)

        self.AddStudentItem = StudentItem()
        self.AddStudentItem.operation.connect(self.add_student_item)

        self.RemoveStudentItem = StudentItem()
        self.RemoveStudentItem.operation.connect(self.View.remove_student_item)

        self.SetStudentFrame = SetStudentFrame()
        self.SetStudentFrame.operation.connect(self.View.set_student_frame)

    def init_host(self):
        self.host = socket.socket()
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = (self.Class.HostAddress, self.PORT)
        self.host.bind(address)
        self.host.listen()
        self.inputs.append(self.host)

        self.handler_thread = threading.Thread(
            target=self.handler, daemon=True, name='ChatHandler')
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
                    self.AddStudentItem.name = message['sender']
                    self.AddStudentItem.start()
                    message = normalize_message(
                        'cmd', 'connect', target=message['sender'])
                    self.set_message(message)
                else:
                    raise FromDifferentClass

            elif message['type'] == 'msg':
                self.MessageReceived.message = message['data']
                self.MessageReceived.sender = message['sender']
                self.MessageReceived.start()

            elif message['type'] == 'fls':
                self.FileMessageReceived.sender = message['sender']
                self.FileMessageReceived.filename = message['data']
                self.FileMessageReceived.data = message['file']
                self.FileMessageReceived.start()

            elif message['type'] == 'frame':
                frame = convert_pil_image_to_QPixmap(message['data'])
                self.SetStudentFrame.name = message['sender']
                self.SetStudentFrame.frame = frame
                self.SetStudentFrame.start()

        except (NotMessage, FromDifferentClass):
            self.inputs.remove(readable)
            self.RemoveStudentItem.name = self.clients_name[readable]
            self.RemoveStudentItem.start()
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

    def set_message(self, message):
        message['sender'] = self.Sender
        if message['target']:
            self.messages[self.clients_socket[message['target']]].put(message)
        else:
            for client in self.messages.keys():
                self.messages[client].put(message)

    def send_message(self):
        text = self.View.txt_message.text()
        if is_blank(text):
            return
        message = normalize_message('msg', text)
        if self.View.w_reply.isVisible():
            target = self.View.lbl_reply.text().removeprefix('Replying to ')
            message['target'] = target
        self.set_message(message)
        if self.View.w_reply.isVisible():
            self.View.display_replied_message_sent(target, text)
            self.View.w_reply.hide()
        else:
            self.View.display_message_sent(text)

    def display_message_received(self, text, sender):
        message_received = _MessageReceived(self.View, text, sender)
        message_received.operation.connect(self.target_sender_message)
        self.View.verticalLayout_10.insertWidget(
            self.View.verticalLayout_10.count()-1, message_received)
        self.View.w_reply.hide()

    def target_sender_message(self, sender):
        self.target = sender
        self.View.lbl_reply.setText(f"Replying to {sender}")
        self.View.w_reply.show()

    def hide_reply(self):
        self.target = None
        self.View.w_reply.hide()

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
                print('file too large')
                return

            with open(response[0], "rb") as file:
                file = bytearray(file.read())

            message = normalize_message("fls", filename, file=file)
            if self.View.w_reply.isVisible():
                target = self.View.lbl_reply.text().removeprefix('Replying to ')
                message['target'] = target
            self.set_message(message)
            if self.View.w_reply.isVisible():
                self.display_replied_file_message_sent(target, filename, file)
                self.View.w_reply.hide()
            else:
                self.display_file_message_sent(filename, file)

    def display_file_message_sent(self, filename, data):
        file_message_sent = FileMessageSent(self.View, filename, data)
        file_message_sent.operation.connect(self.download_file)
        self.View.verticalLayout_10.insertWidget(
            self.View.verticalLayout_10.count()-1, file_message_sent)

    def display_replied_file_message_sent(self, target, filename, data):
        file_message_sent = RepliedFileMessageSent(self.View, target, filename, data)
        file_message_sent.operation.connect(self.download_file)
        self.View.verticalLayout_10.insertWidget(
            self.View.verticalLayout_10.count()-1, file_message_sent)

    def download_file(self, data, filename):
        path = os.path.join(os.path.expanduser('~/Documents'), filename)
        ext = filename.split('.')[-1]
        path = QFileDialog.getSaveFileName(
            self.View, 'Save File', path, ext)[0]
        with open(path, 'wb') as file:
            file.write(data)

    def display_file_message_received(self, sender, filename, data):
        file_message_received = _FileMessageReceived(self.View, sender, filename, data)
        file_message_received.download.connect(self.download_file)
        file_message_received.reply.connect(self.target_sender_message)
        self.View.verticalLayout_10.insertWidget(self.View.verticalLayout_10.count()-1, file_message_received)
    
    def add_student_item(self, name):
        student_item = _StudentItem(self.View, name)
        student_item.operation.connect(self.student_item_clicked)
        student_item.setObjectName(name)
        self.View.flow_layout.addWidget(student_item)

    def student_item_clicked(self, name):
        print(name)

    def reconnect(self):
        self.Meeting.is_connected = True
        self.Meeting.is_disconnected = False
        self.Meeting.is_frozen = False

        self.Meeting.StreamHost.init_stream()
        message = normalize_message('cmd', 'reconnect')
        self.set_message(message)

    def disconnect(self):
        self.Meeting.is_connected = False
        self.Meeting.is_disconnected = True
        message = normalize_message('cmd', 'disconnect')
        self.set_message(message)

    def freeze(self):
        if self.Meeting.is_frozen:
            self.Meeting.is_frozen = False
            message = normalize_message('cmd', 'thawed')
        else:
            self.Meeting.is_frozen = True
            message = normalize_message('cmd', 'frozen')
        self.set_message(message)
