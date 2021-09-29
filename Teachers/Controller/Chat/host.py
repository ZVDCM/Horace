from PyQt5 import QtCore
from Teachers.Misc.Widgets.message_targets import MessageTarget
from Teachers.Misc.Functions.window_capture import convert_bytearray_to_pil_image, convert_pil_image_to_QPixmap
from PyQt5.QtGui import QPixmap
from Teachers.Misc.Widgets.student_item import StudentItem as _StudentItem
from Teachers.Misc.Widgets.file_message_sent import FileMessageSent
from Teachers.Misc.Widgets.file_message_received import FileMessageReceived as _FileMessageReceived
from Teachers.Misc.Widgets.replied_file_message_sent import RepliedFileMessageSent
from PyQt5.QtWidgets import QFileDialog
from Teachers.Misc.Functions.is_blank import is_blank
from Teachers.Misc.Functions.messages import *
from PyQt5.QtCore import QThread, pyqtSignal
from Teachers.Misc.Widgets.message_received import MessageReceived as _MessageReceived
from datetime import date, datetime
import os
import queue
import socket
import select
import threading


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


class Attendance(QtCore.QThread):
    operation = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = ()

    def run(self):
        res = self.fn(*self.val)
        if res == 'successful':
            self.operation.emit()
        self.quit()


class GetUrls(QtCore.QThread):
    operation = QtCore.pyqtSignal(object)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        res = self.fn()
        self.operation.emit(res)
        self.quit()


class SetMeetingStatus(QtCore.QThread):

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.val = None

    def run(self):
        self.fn(self.val)
        self.quit()


class Alert(QtCore.QThread):
    operation = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.val = ()

    def run(self):
        self.operation.emit(*self.val)
        self.quit()


class Host:

    PORT = 43200

    def __init__(self, Meeting, Class, Model, View, Controller):
        self.Meeting = Meeting
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.Sender = Controller.User.Username

        self.target = None
        self.messages = {}
        self.inputs = []
        self.outputs = []
        self.clients_name = {}
        self.clients_socket = {}
        self.time = {}

        self.start_time = QtCore.QTime(0, 0, 0)
        self.status_time = 0

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
        self.View.Overlay.btn_freeze.clicked.connect(self.init_freeze_thaw)
        self.View.btn_send_many.clicked.connect(self.init_message_target)
        self.View.closeEvent = self.meeting_closed
        self.View.lv_url.clicked.connect(self.url_list_clicked)

        self.View.btn_init_add_url.clicked.connect(self.init_add_url)
        self.View.btn_init_edit_url.clicked.connect(self.init_edit_url)
        self.View.btn_delete_url.clicked.connect(self.delete_url)
        self.View.txt_url.returnPressed.connect(self.init_add_edit_url)
        self.View.btn_add_edit_url.clicked.connect(self.init_add_edit_url)
        self.View.btn_cancel_url.clicked.connect(self.cancel_url)

        self.View.btn_search_student.clicked.connect(self.search)
        self.View.txt_search_student.returnPressed.connect(self.search)
        self.View.lv_student.hideEvent = self.reset_list_target

        self.View.btn_shutdown.clicked.connect(
            lambda: self.btn_commands_clicked('shutdown'))
        self.View.btn_restart.clicked.connect(
            lambda: self.btn_commands_clicked('restart'))
        self.View.btn_lock.clicked.connect(
            lambda: self.btn_commands_clicked('lock'))

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

        self.AddAttendance = Attendance(self.Model.create_attendance)
        self.AddAttendance.operation.connect(lambda: self.show_alert('attendance', 'Attendance Stored'))
        self.AddAttendance.operation.connect(self.Controller.Lobby.get_attendances)

        self.IncrementBadge = Operation()
        self.IncrementBadge.operation.connect(self.View.BadgeOverlay.increment)

        self.GetUrls = GetUrls(self.Model.get_blacklisted_urls)
        self.GetUrls.started.connect(self.View.LoadingScreenURL.show)
        self.GetUrls.started.connect(self.View.LoadingScreenURLList.show)
        self.GetUrls.operation.connect(self.set_url_list)
        self.GetUrls.finished.connect(self.View.LoadingScreenURL.hide)
        self.GetUrls.finished.connect(self.View.LoadingScreenURLList.hide)
        self.GetUrls.start()

        self.ShowLoadingScreen = Operation()
        self.ShowLoadingScreen.operation.connect(self.View.LoadingScreen.show)

        self.HideLoadingScreen = Operation()
        self.HideLoadingScreen.operation.connect(self.View.LoadingScreen.hide)

    def show_alert(self, type, message):
        self.ShowAlert = Alert()
        self.ShowAlert.operation.connect(self.View.show_alert)
        self.ShowAlert.val = type, message
        self.ShowAlert.start()

    def set_meeting_status_handler(self, status):
        self.status_time = 0
        self.handler = SetMeetingStatus(self.View.set_meeting_status)
        self.handler.val = status
        self.handler.start()

    def init_host(self):
        self.host = socket.socket()
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = (self.Class.HostAddress, self.PORT)
        self.host.bind(address)
        self.host.listen()
        print(self.host)
        self.inputs.append(self.host)

        class_start = self.now()
        self.time['Teacher'] = {'Start': class_start}

        handler_thread = threading.Thread(
            target=self.handler, daemon=True, name='ChatHandler')
        handler_thread.start()

        self.set_meeting_status_handler('Meeting initialized')

    def handler(self):
        while self.View.isVisible():
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

        else:
            for socket in self.inputs:
                socket.close()

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
                    target = message['sender']
                    self.clients_name[readable] = target
                    self.clients_socket[target] = readable

                    self.add_student_list(target)

                    self.AddStudentItem.name = target
                    self.AddStudentItem.start()

                    time_joined = self.now()
                    try:
                        self.time[target]['log'].append(
                            ('Joined', time_joined))
                        self.time[target]['logged'] += 1
                    except KeyError:
                        self.time[target] = {
                            'logged': 1, 'log': [('Joined', time_joined)]}

                    message = normalize_message(
                        'time', self.start_time, target=target)
                    self.set_message(message)

                    if self.Meeting.is_disconnected:
                        message = normalize_message(
                            'cmd', 'disconnect', target=target)
                        self.set_message(message)
                    elif self.Meeting.is_frozen:
                        message = normalize_message(
                            'cmd', 'frozen', target=target)
                        self.set_message(message)
                        message = normalize_message('frame', convert_bytearray_to_pil_image(
                            self.Meeting.StreamHost.last_frame), target=target)
                        self.set_message(message)

                    message = normalize_message(
                        'url', self.View.lv_url.model().data, target=target)
                    self.set_message(message)
                    message = normalize_message(
                        'student', self.View.lv_student.model().data)
                    self.set_message(message)
                    self.set_meeting_status_handler(
                        f"{target} joined the class")
                else:
                    message = normalize_message(
                        'permission', False, target=message['sender'])
                    message = serialize_message(message)
                    send_message(message, readable)
                    raise FromDifferentClass

            elif message['type'] == 'msg':
                self.IncrementBadge.start()
                self.MessageReceived.message = message['data']
                self.MessageReceived.sender = message['sender']
                self.MessageReceived.start()
                self.set_meeting_status_handler(
                    f"Received a message from {message['sender']}")

            elif message['type'] == 'fls':
                self.IncrementBadge.start()
                self.FileMessageReceived.sender = message['sender']
                self.FileMessageReceived.filename = message['data']
                self.FileMessageReceived.data = message['file']
                self.FileMessageReceived.start()
                self.set_meeting_status_handler(
                    f"Received a file from {message['sender']}")

            elif message['type'] == 'frame':
                frame = convert_pil_image_to_QPixmap(message['data'])
                self.SetStudentFrame.name = message['sender']
                self.SetStudentFrame.frame = frame
                self.SetStudentFrame.start()

            elif message['type'] == 'res':
                self.Controller.View.RemoteDesktop.target_resolution = message['data']

        except FromDifferentClass:
            self.exceptional(readable)

        except NotMessage:
            time_left = self.now()
            try:
                target = self.clients_name[readable]
                self.time[target]['log'].append(('Left', time_left))
                self.time[target]['logged'] += 1
                self.set_meeting_status_handler(f"{target} left the class")
                self.exceptional(readable)
            except KeyError:
                return

        except ConnectionAbortedError:
            return

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
            student = self.clients_name[exceptional]
            try:
                if self.Controller.View.RemoteDesktop.isVisible():
                    if student in self.Controller.View.RemoteDesktop.title_bar.title.text():
                        self.Controller.View.RemoteDesktop.title_bar.btn_close.click()
            except AttributeError:
                pass
            student_model = self.View.lv_student.model()
            row = student_model.findRow(student)
            student_model.removeRows(row, 1)
            message = normalize_message(
                'student', self.View.lv_student.model().data)
            self.set_message(message)

            self.RemoveStudentItem.name = student
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
        if path:
            self.show_alert('file', 'Downloading file...')
            with open(path, 'wb') as file:
                file.write(data)
            self.show_alert('file', 'File downloaded')

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
        student_item.ContextMenu.shutdown.connect(
            lambda: self.btn_commands_clicked('shutdown', name))
        student_item.ContextMenu.restart.connect(
            lambda: self.btn_commands_clicked('restart', name))
        student_item.ContextMenu.lock.connect(
            lambda: self.btn_commands_clicked('lock', name))
        student_item.ContextMenu.control.connect(
            lambda: self.control_desktop(name))
        student_item.setObjectName(name)
        self.View.flow_layout.addWidget(student_item)

    def student_item_clicked(self, name):
        self.target = name

    def reconnect(self):
        self.Meeting.is_connected = True
        self.Meeting.is_disconnected = False
        self.Meeting.is_frozen = False

        self.Meeting.StreamHost.init_stream()
        message = normalize_message('cmd', 'reconnect')
        self.set_message(message)
        self.set_meeting_status_handler('Screen reconnected')

    def disconnect(self):
        self.Meeting.is_connected = False
        self.Meeting.is_disconnected = True

        if self.Meeting.is_frozen:
            self.View.disconnect_screen()

        message = normalize_message('cmd', 'disconnect')
        self.set_message(message)
        self.set_meeting_status_handler('Screen disconnected')

    def init_freeze_thaw(self):
        if self.Meeting.is_frozen:
            self.thaw()
        else:
            self.freeze()

    def freeze(self):
        self.Meeting.is_frozen = True
        message = normalize_message('cmd', 'frozen')
        self.set_meeting_status_handler('Screen frozen')
        self.set_message(message)
    
    def thaw(self):
        self.Meeting.is_frozen = False
        message = normalize_message('cmd', 'thawed')
        self.Meeting.StreamHost.init_stream()
        self.set_meeting_status_handler('Screen thawed')
        self.set_message(message)

    def init_message_target(self):
        self.MessageTarget = MessageTarget(self)
        target_student_model = self.Model.ReadOnlyListModel(self.MessageTarget.lv_target_student, [
            self.View.lv_student.model().getRowData(i.row()) for i in self.View.lv_student.selectedIndexes()])
        self.MessageTarget.set_model(target_student_model)
        self.MessageTarget.txt_message.returnPressed.connect(
            self.target_send_message)
        self.MessageTarget.operation.connect(self.target_init_send_message)
        self.MessageTarget.btn_file.clicked.connect(self.target_get_file)
        self.MessageTarget.run()

    def target_init_send_message(self, is_popup):
        if is_popup:
            self.target_send_popup()
        else:
            self.target_send_message()

    def target_send_popup(self):
        text = self.MessageTarget.txt_message.text()
        if is_blank(text):
            return

        message = normalize_message(
            'popup', [text, self.MessageTarget.comboBox.currentText()])

        for target in self.MessageTarget.targets:
            message['target'] = target
            self.set_message(message)

        self.MessageTarget.close()

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

        try:
            if self.Meeting.is_frozen:
                self.View.Overlay.btn_freeze.click()
            self.Controller.View.RemoteDesktop.title_bar.btn_close.click()
        except AttributeError:
            pass

        for student_name, student_info in list(self.time.items())[1:]:
            if 2 % student_info['logged'] != 0:
                self.time[student_name]['log'].append(('Left', class_end))

        attendance_thread = threading.Thread(
            target=self.record_attendance, daemon=True, name="AttendanceThread")
        attendance_thread.start()

        if not self.Controller.View.Lobby.isVisible():
            self.Controller.SignInController.View.init_sign_in()
            self.Controller.SignInController.Model.init_sign_in()
            self.Controller.SignInController.init_sign_in()

    def record_attendance(self):
        self.show_alert('attendance', 'Storing Attendance...')
        attendance = "".join(("Class Meeting Summary\n",
                              f"Total Number of Students,{len(list(self.time.items())[1:])}\n",
                              f"Teacher,{self.Controller.User.Username}\n",
                              f"Class Name,{self.Class.Name}\n",
                              f"Scheduled Start,{self.Class.Start}\n",
                              f"Scheduled End,{self.Class.End}\n",
                              f"Class Start,{self.time['Teacher']['Start']}\n",
                              f"Class End,{self.time['Teacher']['End']}\n",
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
        self.AddAttendance.val = self.Controller.User.Username, "%s %s.csv" % (
            self.Class.Code,  date.today().strftime("%B %d, %Y")), data, datetime.today()
        # if self.Controller.View.Lobby.isVisible():
            # self.AddAttendance.operation.connect(self.Controller.Lobby.get_attendances)
        self.AddAttendance.start()

    def timer_event(self):
        self.start_time = self.start_time.addSecs(1)
        self.SetTime.time = self.start_time.toString("hh:mm:ss")
        self.SetTime.start()

        self.status_time += 1
        if self.status_time == 5:
            self.View.lbl_meeting_status.clear()

    def now(self):
        now = datetime.now()
        return now.strftime("%I:%M %p")

    def btn_commands_clicked(self, command, target=None):
        message = normalize_message('cmd', command, target=target)
        self.set_message(message)

    def control_desktop(self, name):
        self.is_controlling = True
        self.View.Overlay.btn_freeze.click()
        message = normalize_message('cmd', 'start control', target=name)
        self.set_message(message)
        self.Controller.View.init_remote_desktop(self.View)
        self.Controller.init_remote_desktop(name)
        self.ShowLoadingScreen.start()

    def set_url_list(self, urls):
        url_model = self.Model.ListModel(self.View.lv_url, urls, True)
        self.View.lv_url.setModel(url_model)

    def set_latest_url(self):
        url_model = self.View.lv_url.model()
        if url_model.rowCount() == url_model.default_size:
            return
        index = url_model.createIndex(url_model.rowCount()-1, 0)
        self.View.lv_url.setCurrentIndex(index)
        text = url_model.getRowData(url_model.rowCount()-1)
        self.View.txt_url.setText(text)

    def url_list_clicked(self, index):
        row = index.row()
        target_url = self.View.lv_url.model().getRowData(row)
        if target_url:
            self.View.txt_url.setText(target_url)

    def init_add_url(self):
        self.View.clear_url_inputs()
        self.View.disable_url_buttons()
        self.View.enable_url_inputs()
        self.View.set_url('Add')

    def init_edit_url(self):
        self.View.disable_url_buttons()
        self.View.enable_url_inputs()
        self.View.set_url('Edit')

    def cancel_url(self):
        self.View.clear_url_inputs()
        self.set_latest_url()
        self.View.enable_url_buttons()
        self.View.disable_url_inputs()
        self.View.set_url('Read')

    def init_add_edit_url(self):
        if self.View.url_state == "Add":
            self.add_url()
        elif self.View.url_state == "Edit":
            self.edit_url()

    def add_url(self):
        domain = self.View.txt_url.text()
        if is_blank(domain):
            self.View.run_popup(f'URL fields must be filled')
            return

        url_model = self.View.lv_url.model()

        index = url_model.findRow(domain)
        if index:
            self.View.run_popup(f'URL exists')
            return

        url_model.insertRows(url_model.rowCount(), 1, domain)
        index = url_model.createIndex(url_model.rowCount()-1, 0)
        self.View.lv_url.setCurrentIndex(index)
        self.cancel_url()
        message = normalize_message('url', self.View.lv_url.model().data)
        self.set_message(message)

    def edit_url(self):
        domain = self.View.txt_url.text()
        if is_blank(domain):
            self.View.run_popup(f'URL fields must be filled')
            return

        url_model = self.View.lv_url.model()
        index = url_model.findRow(domain)
        if index and index != self.View.lv_url.selectedIndexes()[0].row():
            self.View.run_popup(f'URL exists')
            return

        url_model.editRow(url_model.rowCount()-1, domain)
        self.cancel_url()
        message = normalize_message('url', self.View.lv_url.model().data)
        self.set_message(message)

    def delete_url(self):
        self.View.txt_url.clear()
        row = self.View.lv_url.selectedIndexes()[0].row()
        url_model = self.View.lv_url.model()
        url_model.removeRows(row, 1)
        self.set_latest_url()
        message = normalize_message('url', self.View.lv_url.model().data)
        self.set_message(message)

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
