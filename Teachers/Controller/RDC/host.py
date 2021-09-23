from Teachers.Misc.Functions.window_capture import convert_pil_image_to_QPixmap
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from Teachers.Misc.Functions.messages import normalize_message
import zlib
import queue
import pickle
import socket
import threading

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
    PORT = 43203

    FORMAT = 'utf-8'

    def __init__(self, RDC, parent, Chat, target):
        self.RDC = RDC
        self.parent = parent
        self.parent.closeEvent = self.parent_closed
        self.parent.mouse_move.connect(self.get_mouse_pos)
        self.parent.mouse_press.connect(self.get_pressed_mouse_button)
        self.parent.mouse_release.connect(self.get_released_mouse_button)
        self.parent.mouse_wheel.connect(self.get_mouse_scroll_direction)
        self.parent.key_press.connect(self.get_pressed_key)
        self.parent.key_release.connect(self.get_released_key)
        self.Chat = Chat
        self.target = target

        self.last_frame = None
        self.frames = queue.Queue()
        self.connect_signals()
        self.parent.run()
        self.start()

    def connect_signals(self):
        self.SetFrame = Frame()
        self.SetFrame.operation.connect(self.parent.set_frame)

    def get_mouse_pos(self, coordinates):
        message = normalize_message('mouse', ['move', coordinates], target=self.target)
        self.Chat.set_message(message)

    def get_pressed_mouse_button(self, button):
        message = normalize_message('mouse', ['pressed', button], target=self.target)
        self.Chat.set_message(message)

    def get_released_mouse_button(self, button):
        message = normalize_message('mouse', ['released', button], target=self.target)
        self.Chat.set_message(message)

    def get_mouse_scroll_direction(self, direction):
        message = normalize_message('mouse', ['scroll', direction], target=self.target)
        self.Chat.set_message(message)

    def get_pressed_key(self, key):
        message = normalize_message('keyboard', ['pressed', key], target=self.target)
        self.Chat.set_message(message)

    def get_released_key(self, key):
        message = normalize_message('keyboard', ['release', key], target=self.target)
        self.Chat.set_message(message)

    def start(self):
        self.server = socket.socket(type=socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((socket.gethostbyname(socket.gethostname()), self.PORT))

        receive_thread = threading.Thread(
            target=self.receive, daemon=True, name="RDCUDPReceiveThread")
        receive_thread.start()

        display_thread = threading.Thread(
            target=self.display, daemon=True, name="RDCUDPDisplayThread")
        display_thread.start()

    def stop(self):
        self.server.close()

    def receive(self):
        while not self.server._closed:
            try:
                data, _ = self.server.recvfrom(self.MAX_DGRAM)
                if len(data) < 100:
                    packets = int(data.decode(self.FORMAT))
                    buffer = b""
                    for _ in range(packets):
                        data, _ = self.server.recvfrom(self.MAX_DGRAM)
                        buffer += data

                    self.frames.put(buffer)
            except OSError:
                self.frames.put("disconnect")
                return

    def display(self):
        while not self.server._closed:
            frame = self.frames.get()
            if self.parent.LoadingScreen.isVisible():
                self.RDC.EndLoading.start()
            if frame == 'disconnect':
                return
            try:
                frame = pickle.loads(zlib.decompress(frame))
                self.last_frame = convert_pil_image_to_QPixmap(frame)
                self.SetFrame.frame = self.last_frame
                self.SetFrame.start()
            except zlib.error:
                continue

    def parent_closed(self, event):
        self.stop()
        message = normalize_message('cmd', 'end control', target=self.target)
        self.Chat.set_message(message)
        self.Chat.View.Overlay.btn_freeze.click()