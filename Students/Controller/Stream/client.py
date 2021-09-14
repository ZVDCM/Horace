
import time
from Students.Misc.Functions.window_capture import convert_pil_image_to_QPixmap
import pickle
import zlib
from PyQt5.QtGui import QPixmap 

from PyQt5.QtCore import QThread, pyqtSignal
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


class Client:
    MAX_DGRAM = 2**16
    BUFFER = MAX_DGRAM - 64

    CLIENT = socket.gethostbyname(socket.gethostname())
    PORT = 43205
    CLIENT_ADDR = (CLIENT, PORT)

    FORMAT = 'utf-8'

    frames = queue.Queue()
    last_frame = None

    def __init__(self, Class, Model, View, Controller):
        self.Class = Class
        self.Model = Model
        self.View = View
        self.Controller = Controller
        self.connect_signals()
        self.init_client()

    def connect_signals(self):
        self.set_frame = Frame()
        self.set_frame.operation.connect(self.View.set_frame)

    def init_client(self):
        self.client = socket.socket(type=socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client.bind(self.CLIENT_ADDR)
        self.start()

    def start(self):
        receiving_thread = threading.Thread(
            target=self.receive, daemon=True, name="StreamReceiveThread")
        receiving_thread.start()

        display_thread = threading.Thread(
            target=self.display, daemon=True, name="StreamDisplayThread")
        display_thread.start()

    def receive(self):
        while True:
            data, _ = self.client.recvfrom(self.MAX_DGRAM)
            if len(data) < 100:
                packets = int(data.decode(self.FORMAT))
                buffer = b""
                for _ in range(packets):
                    data, _ = self.client.recvfrom(self.MAX_DGRAM)
                    buffer += data

                self.frames.put(buffer)

    def display(self):
        while True:
            frame = self.frames.get()
            try:
                frame = pickle.loads(zlib.decompress(frame))
                self.last_frame = convert_pil_image_to_QPixmap(frame)
                self.set_frame.frame = self.last_frame
                self.set_frame.start()
                time.sleep(0.025)
            except zlib.error:
                continue