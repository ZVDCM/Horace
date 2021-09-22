import threading
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QEvent, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
import mss
import win32ui
from Teachers.Misc.Functions.window_capture import convert_bytearray_to_QPixmap, convert_bytearray_to_pil_image, window_capture
import socket
import pickle
import zlib
import math
import pywintypes

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

    def __init__(self, Meeting, Class, Model, View, Controller):
        self.Meeting = Meeting
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.last_frame = bytearray()
        self.connect_signals()
        self.init_host()

    def connect_signals(self):
        self.SetFrame = Frame()
        self.SetFrame.operation.connect(self.View.set_frame)
        
        self.View.page.resizeEvent = self.screen_resized
        
    def init_host(self):
        self.host = socket.socket(type=socket.SOCK_DGRAM)
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        address = (self.Class.HostAddress, self.HOST_PORT)
        self.host.bind(address)
        self.init_stream()

    def init_stream(self):
        self.stream_thread = threading.Thread(target=self.handler, daemon=True, name="StreamHandler")
        self.stream_thread.start()

    def handler(self):
        while self.View.isVisible() and self.Meeting.is_connected:
            if self.Meeting.is_frozen:
                return
            try:
                self.last_frame = window_capture()
            except (win32ui.error, pywintypes.error, mss.exception.ScreenShotError):
                pass
            self.display_frame(self.last_frame)
            broadcast_thread = threading.Thread(target=self.broadcast_frame, args=(self.last_frame,), daemon=True, name="BroadcastThread")
            broadcast_thread.start()
        self.View.disconnect_screen()

    def display_frame(self, frame):
        frame = convert_bytearray_to_QPixmap(frame)
        self.SetFrame.frame = frame

        if self.Meeting.is_disconnected:
            self.SetFrame.finished.connect(self.View.disconnect_screen)
        else:
            try:
                self.SetFrame.finished.disconnect(self.View.disconnect_screen)
            except TypeError:
                pass

        self.SetFrame.start()

    def broadcast_frame(self, frame):
        if not self.View.isVisible():
            return
            
        pil_img = convert_bytearray_to_pil_image(frame)
        pil_img = zlib.compress(pickle.dumps(
            pil_img, pickle.HIGHEST_PROTOCOL), 9)
        packets = str(math.ceil(len(pil_img)/self.BUFFER)).encode(self.FORMAT)
        self.host.sendto(packets, self.BROADCAST_ADDR)

        while pil_img and self.View.isVisible():
            bytes_sent = self.host.sendto(
                pil_img[:self.BUFFER], self.BROADCAST_ADDR)
            pil_img = pil_img[bytes_sent:]

    def screen_resized(self, event):
        if self.Meeting.is_frozen:
            frame = convert_bytearray_to_QPixmap(self.last_frame)
            frame = frame.scaled(
                    self.View.page.width(), self.View.page.height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.View.screen.setPixmap(frame)
        self.View.Overlay.parent_resized(None)