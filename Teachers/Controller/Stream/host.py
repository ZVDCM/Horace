import threading
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from Teachers.Misc.Functions.window_capture import convert_bytearray_to_QPixmap, window_capture, resize_img
import socket
import pickle
import zlib
import math

class Operation(QThread):
    operation = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        self.operation.emit()
        self.quit()

class Frame(QThread):
    operation = pyqtSignal(QtGui.QPixmap)

    def __init__(self):
        super().__init__()
        self.frame = None

    def run(self):
        self.operation.emit(self.frame)
        self.quit()
        
class Host:
    MAX_DGRAM = 2**16
    BUFFER = MAX_DGRAM - 64
    HOST_PORT = 43201

    BROADCAST = "255.255.255.255"
    BROADCAST_PORT = 43205
    BROADCAST_ADDR = (BROADCAST, BROADCAST_PORT)

    FORMAT = 'utf-8'

    last_frame = bytearray()

    def __init__(self, Class, Model, View, Controller):
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.connect_signals()
        self.init_host()

    def connect_signals(self):
        self.set_frame = Frame()
        self.set_frame.operation.connect(self.View.set_frame)

    def init_host(self):
        self.host = socket.socket(type=socket.SOCK_DGRAM)
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        address = (self.Class.HostAddress, self.HOST_PORT)
        self.host.bind(address)

        self.stream_thread = threading.Thread(target=self.handler, daemon=True, name="StreamHandler")
        self.stream_thread.start()

    def handler(self):
        while True:
            self.last_frame = window_capture()
            self.display_frame(self.last_frame)
            broadcast_thread = threading.Thread(target=self.broadcast_frame, args=(self.last_frame,), daemon=True, name="BroadcastThread")
            broadcast_thread.start()

    def display_frame(self, frame):
        frame = convert_bytearray_to_QPixmap(frame)
        self.set_frame.frame = frame
        self.set_frame.start()

    def broadcast_frame(self, frame):
        resized_img = resize_img(frame)
        resized_img = zlib.compress(pickle.dumps(
            resized_img, pickle.HIGHEST_PROTOCOL), 9)
        packets = str(math.ceil(len(resized_img)/self.BUFFER)).encode(self.FORMAT)
        self.host.sendto(packets, self.BROADCAST_ADDR)

        while resized_img:
            bytes_sent = self.host.sendto(
                resized_img[:self.BUFFER], self.BROADCAST_ADDR)
            resized_img = resized_img[bytes_sent:]