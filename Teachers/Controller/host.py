import threading
from Students.Misc.Functions.messages import *
import socket
import select
import queue
from PyQt5.QtCore import QThread


class Host:

    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 43200
    ADDR = (HOST, PORT)

    messages = queue.Queue()
    message = None
    inputs = []
    outputs = []
    clients = {}

    def __init__(self, Class):
        self.Class = Class
        self.init_host()

    def init_host(self):
        self.host = socket.socket()
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host.bind(self.ADDR)
        self.host.listen()
        self.inputs.append(self.host)

        handler_thread = threading.Thread(
            target=self.handler, daemon=True, name='ChatHandler')
        handler_thread.start()

    def handler(self):
        while self.inputs:
            readables, writables, exceptionals = select.select(
                self.inputs, self.outputs, self.inputs)

            for readable in readables:
                if not self.host_readable(readable):
                    self.client_readable(readable)

            try:
                self.message = self.messages.get_nowait()
            except queue.Empty:
                pass

            for writable in writables:
                if not self.client_writable(writable):
                    break

            for exceptional in exceptionals:
                self.exceptional(exceptional)

    def host_readable(self, readable):
        if readable is not self.host:
            return False

        client_socket, client_address = readable.accept()
        self.inputs.append(client_socket)
        self.clients[client_socket] = None

        return True

    def client_readable(self, readable):
        try:
            message = receive_message(readable)

            if not message:
                raise Exception

            if readable not in self.outputs:
                        self.outputs.append(readable)

            if message['type'] == 'section':
                if message['data'] == self.Class.Code:
                    self.set_message('cmd', 'connect')
                else:
                    raise Exception

            elif message['type'] == 'name':
                self.clients[readable] = message['data']

        except:
            self.inputs.remove(readable)
            if readable in self.outputs:
                self.outputs.remove(readable)
            if readable in self.clients.keys():
                del self.clients[readable]
            readable.close()

    def client_writable(self, writable):
        if not self.message or writable._closed:
            return False
        send_message(self.message, writable)
        self.message = None
        return True

    def exceptional(self, exceptional):
        self.inputs.remove(exceptional)
        if exceptional in self.outputs:
            self.outputs.remove(exceptional)
        if exceptional in self.clients.keys():
            del self.clients[exceptional]
        exceptional.close()

    def set_message(self, type, message):
        message = serialize_message(normalize_message(type, message))
        self.messages.put(message)
