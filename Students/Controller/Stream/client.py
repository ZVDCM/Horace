from PyQt5 import QtCore
from Students.Misc.Functions.window_capture import convert_pil_image_to_QPixmap
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import pickle
import zlib
import queue
import socket
import threading


class Frame(QThread):
    operation = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        self.frame = None

    def run(self):
        self.operation.emit(self.frame)
        self.quit()


class Operation(QThread):
    operation = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        self.operation.emit()
        self.quit()


class Client:
    MAX_DGRAM = 2**16
    BUFFER = MAX_DGRAM - 64

    CLIENT = socket.gethostbyname(socket.gethostname())
    PORT = 43205
    CLIENT_ADDR = (CLIENT, PORT)

    FORMAT = 'utf-8'

    def __init__(self, chat_socket, Meeting, ClassTeacher, Model, View, Controller):
        self.chat_socket = chat_socket
        self.Meeting = Meeting
        self.ClassTeacher = ClassTeacher
        self.Model = Model
        self.View = View
        self.Controller = Controller
        
        self.frames = queue.Queue()
        self.last_frame = None

        self.connect_signals()
        self.start()

    def connect_signals(self):
        self.SetFrame = Frame()
        self.SetFrame.operation.connect(self.View.set_frame)

        self.DisconnectScreen = Operation()
        self.DisconnectScreen.operation.connect(self.View.disconnect_screen)

        self.View.widget.resizeEvent = self.screen_resized

    def init_client(self):
        self.client = socket.socket(type=socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(self.CLIENT_ADDR)

    def start(self):
        self.frames = queue.Queue()
        self.init_client()
        self.start_receiving()
        self.start_displaying()

    def stop(self):
        self.client.close()

    def start_receiving(self):
        receiving_thread = threading.Thread(
            target=self.receive, daemon=True, name="StreamReceiveThread")
        receiving_thread.start()

    def start_displaying(self):
        display_thread = threading.Thread(
            target=self.display, daemon=True, name="StreamDisplayThread")
        display_thread.start()

    def receive(self):
        while self.Meeting.is_connected and not self.Meeting.is_frozen and not self.client._closed and not self.chat_socket._closed:
            try:
                data, _ = self.client.recvfrom(self.MAX_DGRAM)
                if len(data) < 150:
                    packets = int(data.decode(self.FORMAT))
                    buffer = b""
                    for _ in range(packets):
                        data, _ = self.client.recvfrom(self.MAX_DGRAM)
                        buffer += data
                    self.frames.put(buffer)
            except OSError as e:
                return
            except UnicodeDecodeError as e:
                continue

    def display(self):
        while not self.chat_socket._closed:
            frame = self.frames.get()
            if frame == 'disconnect':
                self.DisconnectScreen.start()
                break
            elif frame == 'frozen':
                try:
                    self.set_last_frame()
                    break
                except AttributeError:
                    continue
            try:
                self.last_frame = pickle.loads(zlib.decompress(frame))
                frame = convert_pil_image_to_QPixmap(self.last_frame)
                self.SetFrame.frame = frame
                self.SetFrame.start()
            except (zlib.error, pickle.UnpicklingError):
                self.frames = queue.Queue()
                continue

    def set_last_frame(self):
        frame = convert_pil_image_to_QPixmap(self.last_frame)
        frame = frame.scaled(
                self.View.w_left.width(), self.View.w_left.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.View.screen.setPixmap(frame)

    def screen_resized(self, event):
        if self.Meeting.is_frozen:
            self.set_last_frame()
        self.View.LoadingScreen.parent_resized(None)