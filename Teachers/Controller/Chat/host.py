from PyQt5 import QtCore
from Teachers.Misc.Widgets.message_targets import MessageTarget
from Teachers.Misc.Functions.window_capture import convert_pil_image_to_QPixmap
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
from datetime import date, datetime, time


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

class SetTime(QThread):
    operation = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.time = None

    def run(self):
        self.operation.emit(self.time)
        self.quit()

class Host:

    PORT = 43200
    messages = {}
    inputs = []
    outputs = []
    clients_name = {}
    clients_socket = {}
    time = {}
    start_time = QtCore.QTime(0, 0, 0)

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
        self.View.ChatInput.txt_message.returnPressed.connect(
            self.send_message)
        self.View.ChatInput.btn_send.clicked.connect(self.send_message)
        self.View.ChatInput.btn_close_reply.clicked.connect(self.hide_reply)
        self.View.ChatInput.btn_file.clicked.connect(self.get_file)
        self.View.Overlay.reconnect.connect(self.reconnect)
        self.View.Overlay.disconnect.connect(self.disconnect)
        self.View.Overlay.btn_freeze.clicked.connect(self.freeze)
        self.View.btn_send_many.clicked.connect(self.init_message_target)
        self.View.closeEvent = self.meeting_closed

        self.MessageReceived = MessageReceived()
        self.MessageReceived.operation.connect(self.display_message_received)

        self.FileMessageReceived = FileMessageReceived()
        self.FileMessageReceived.operation.connect(
            self.display_file_message_received)

        self.AddStudentItem = StudentItem()
        self.AddStudentItem.operation.connect(self.add_student_item)

        self.AddStudentItem = StudentItem()
        self.AddStudentItem.operation.connect(self.add_student_item)

        self.RemoveStudentItem = StudentItem()
        self.RemoveStudentItem.operation.connect(self.View.remove_student_item)

        self.SetStudentFrame = SetStudentFrame()
        self.SetStudentFrame.operation.connect(self.View.set_student_frame)

        self.SetTime = SetTime()
        self.SetTime.operation.connect(self.View.set_timer)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(1000)

    def init_host(self):
        self.host = socket.socket()
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = (self.Class.HostAddress, self.PORT)
        self.host.bind(address)
        self.host.listen()
        self.inputs.append(self.host)

        class_start = self.now()
        self.time['Teacher'] = {'Start' : class_start}

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

                    self.add_student_list(message['sender'])

                    self.AddStudentItem.name = message['sender']
                    self.AddStudentItem.start()

                    time_joined = self.now()
                    try:
                        self.time[message['sender']]['log'].append(('Joined', time_joined))
                        self.time[message['sender']]['logged'] += 1
                    except KeyError:
                        self.time[message['sender']] = {'logged': 1, 'log': [('Joined', time_joined)]}

                    message = normalize_message(
                        'time', self.start_time, target=message['sender'])
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

        except FromDifferentClass:
            self.exceptional(readable)

        except NotMessage:
            time_left = self.now()
            self.time[self.clients_name[readable]]['log'].append(('Left', time_left))
            self.time[self.clients_name[readable]]['logged'] += 1
            self.exceptional(readable)

    def client_writable(self, message, writable):
        if writable._closed:
            return
        message = serialize_message(message)
        send_message(message, writable)

    def add_student_list(self, name):
        student_model = self.View.lv_student.model()
        student_model.insertRows(student_model.rowCount()-1, 1, name)

    def exceptional(self, exceptional):
        self.inputs.remove(exceptional)
        if exceptional in self.outputs:
            self.outputs.remove(exceptional)
        if exceptional in self.clients_name.keys():
            self.RemoveStudentItem.name = self.clients_name[exceptional]
            self.RemoveStudentItem.start()
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
        text = self.View.ChatInput.txt_message.text()
        if is_blank(text):
            return
        message = normalize_message('msg', text)
        if self.View.ChatInput.w_reply.isVisible():
            for target in self.View.ChatInput.targets:
                message['target'] = target
                self.set_message(message)

            targets = self.View.ChatInput.targets[0]
            if len(self.View.ChatInput.targets) == 2:
                targets = " and ".join(self.View.ChatInput.targets)
            elif len(self.View.ChatInput.targets) == 3:
                last_targets = self.View.ChatInput.targets.pop()
                targets = ", ".join(
                    self.View.ChatInput.targets) + f", and {last_targets}"
            elif len(self.View.ChatInput.targets) > 3:
                first_three_targets = self.View.ChatInput.targets[:3]
                targets = ", ".join(
                    first_three_targets) + f", and {len(self.View.ChatInput.targets[2:])} others"
            self.View.display_replied_message_sent(targets, text)
            self.View.ChatInput.hide_targets()
        else:
            self.set_message(message)
            self.View.display_message_sent(text)

    def display_message_received(self, text, sender):
        message_received = _MessageReceived(self.View, text, sender)
        message_received.operation.connect(self.target_sender_message)
        self.View.verticalLayout_10.insertWidget(
            self.View.verticalLayout_10.count()-1, message_received)
        self.View.ChatInput.hide_targets()

    def target_sender_message(self, sender):
        self.View.ChatInput.w_reply.show()
        self.View.ChatInput.add_student(sender)
        student_model = self.View.lv_student.model()
        target_row = student_model.findRow(sender)
        index = student_model.createIndex(target_row, 0)
        self.View.lv_student.setCurrentIndex(index)

    def hide_reply(self):
        self.View.ChatInput.hide_targets()

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
            if self.View.ChatInput.w_reply.isVisible():
                for target in self.View.ChatInput.targets:
                    message['target'] = target
                    self.set_message(message)

                targets = self.View.ChatInput.targets.pop()
                if len(self.View.ChatInput.targets) == 2:
                    targets = " and ".join(self.View.ChatInput.targets)
                elif len(self.View.ChatInput.targets) == 3:
                    last_targets = self.View.ChatInput.targets.pop()
                    targets = ", ".join(
                        self.View.ChatInput.targets) + f", and {last_targets}"
                elif len(self.View.ChatInput.targets) > 3:
                    first_three_targets = self.View.ChatInput.targets[:3]
                    targets = ", ".join(
                        first_three_targets) + f", and {len(self.View.ChatInput.targets[2:])} others"
                self.display_replied_file_message_sent(targets, filename, file)
                self.View.ChatInput.hide_targets()
            else:
                self.set_message(message)
                self.display_file_message_sent(filename, file)

    def display_file_message_sent(self, filename, data):
        file_message_sent = FileMessageSent(self.View, filename, data)
        file_message_sent.operation.connect(self.download_file)
        self.View.verticalLayout_10.insertWidget(
            self.View.verticalLayout_10.count()-1, file_message_sent)

    def display_replied_file_message_sent(self, target, filename, data):
        file_message_sent = RepliedFileMessageSent(
            self.View, target, filename, data)
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
        file_message_received = _FileMessageReceived(
            self.View, sender, filename, data)
        file_message_received.download.connect(self.download_file)
        file_message_received.reply.connect(self.target_sender_message)
        self.View.verticalLayout_10.insertWidget(
            self.View.verticalLayout_10.count()-1, file_message_received)

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

    def init_message_target(self):
        self.MessageTarget = MessageTarget(self)
        target_student_model = self.Model.ListModel(self.MessageTarget.lv_target_student, [
                                                    self.View.lv_student.model().getRowData(i.row()) for i in self.View.lv_student.selectedIndexes()])
        self.MessageTarget.set_model(target_student_model)
        self.MessageTarget.txt_message.returnPressed.connect(
            self.target_send_message)
        self.MessageTarget.btn_send.clicked.connect(self.target_send_message)
        self.MessageTarget.btn_file.clicked.connect(self.target_get_file)
        self.MessageTarget.run()

    def target_send_message(self):
        text = self.MessageTarget.txt_message.text()
        if is_blank(text):
            return

        message = normalize_message('msg', text)

        for target in self.MessageTarget.targets:
            message['target'] = target
            self.set_message(message)

        self.MessageTarget.close()

    def target_get_file(self):
        response = QFileDialog.getOpenFileName(
            parent=self.MessageTarget,
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
            for target in self.MessageTarget.targets:
                message['target'] = target
                self.set_message(message)

        self.MessageTarget.close()

    def meeting_closed(self, event):
        class_end = self.now()
        self.time['Teacher']['End'] = class_end

        for student_name, student_info in list(self.time.items())[1:]:
            if 2 % student_info['logged'] != 0:
                self.time[student_name]['log'].append(('Left', class_end))
        
        attendance_thread = threading.Thread(target=self.record_attendance, daemon=True, name="AttendanceThread")
        attendance_thread.start()

    def record_attendance(self):
        attendance = "".join(("Class Meeting Summary\n",
                      f"Total Number of Students,{len(list(self.time.items())[1:])}\n",
                      f"Teacher,{self.Controller.User.Username}\n",
                      f"Class Name,{self.Class.Name}\n",
                      f"Scheduled Start,{self.Class.Start}\n",
                      f"Scheduled End,{self.Class.End}\n",
                      f"Class Start,\"{self.time['Teacher']['Start']}\"\n",
                      f"Class End,\"{self.time['Teacher']['End']}\"\n",
                      f"\nUsername,Join Time,Leave Time\n",
        ))

        del self.time['Teacher']
        for student_name, student_info in self.time.items():
            student_row = student_name
            for index, timelog in enumerate(student_info['log']):
                if timelog[0] == 'Left':
                    student_row += ",%s\n" % timelog[1]
                else:
                    student_row += ",%s" % timelog[1]
            attendance += student_row + "\n"

        data = bytearray(attendance.encode('utf-8'))
        with open("%s-%s.csv" % (self.Class.Code, date.today().strftime("%B %d, %Y")), 'wb') as file:
            file.write(data)

    def timer_event(self):
        self.start_time = self.start_time.addSecs(1)
        self.SetTime.time = self.start_time.toString("hh:mm:ss")
        self.SetTime.start()

    def now(self):
        now = datetime.now()
        return now.strftime("%I:%M %p")