import socket
import threading
from Students.Misc.Functions.window_capture import rdc_screenshot
import zlib
import pickle
import math


class Client:
    MAX_DGRAM = 2**16
    BUFFER = MAX_DGRAM - 64
    PORT = 43203

    FORMAT = 'utf-8'

    def __init__(self, Class, View):
        self.Class = Class
        self.View = View
        self.destination = (self.Class.HostAddress, self.PORT) 
        self.client = socket.socket(type=socket.SOCK_DGRAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        handle_thread = threading.Thread(
            target=self.handle, daemon=True, name="RDCHandleThread")
        handle_thread.start()

    def stop(self):
        self.client.close()

    def handle(self):
        while self.View.isVisible() and not self.client._closed:
            self.frame = rdc_screenshot()
            send_thread = threading.Thread(
                target=self.send, daemon=True, args=(self.frame,), name="RDCSendThread")
            send_thread.start()

    def send(self, frame):
        try:
            frame = zlib.compress(pickle.dumps(frame, pickle.HIGHEST_PROTOCOL), 9)
            packets = str(math.ceil(len(frame)/(self.BUFFER))).encode(self.FORMAT)
            self.client.sendto(packets, self.destination)

            while frame:
                bytes_sent = self.client.sendto(frame[:self.BUFFER], self.destination)
                frame = frame[bytes_sent:]
        except OSError:
            return
