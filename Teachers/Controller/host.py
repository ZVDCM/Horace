import socket
import select
import queue
from PyQt5.QtCore import QThread
from Teachers.Misc.Functions.messages import receive_message

class ChatHandler(QThread):

    messages = queue.Queue()
    
    def __init__(self, inputs, outputs):
        super().__init__(objectName="ChatHandler")
        self.host = inputs[0]
        self.inputs = inputs
        self.outputs = outputs

    def __str__(self):
        return str(self.isRunning())

    def run(self):
        while self.inputs:
            readables, writables, exceptionals = select.select(self.inputs, self.outputs, self.inputs)
            
            for readable in readables:
                if not self.host_readable(readable):
                    self.client_readable(readable)
            
            for writable in writables:
                pass

            for exceptional in exceptionals:
                pass

        self.quit()

    def host_readable(self, readable):
        if readable is not self.host:
            return False

        client_socket, client_address = readable.accept()
        self.inputs.append[client_socket]

        return True

    def client_readable(self, readable):
        message = receive_message(readable)

        if not message:
            return

        print(message)


class Host:

    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 43200
    ADDR = (HOST, PORT)

    threads = {}

    def __init__(self, Class):
        self.Class = Class
        self.init_host(Class)

    def init_host(self, Class):
        self.host = socket.socket()
        self.host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host.bind(self.ADDR)
        self.host.listen()

        inputs = [self.host]
        outputs = []

        self.ChatHandler = ChatHandler(inputs, outputs)
        self.ChatHandler.finished.connect(lambda: self.remove_thread(self.ChatHandler.objectName()))
        self.threads[self.ChatHandler.objectName()] = self.ChatHandler

        self.ChatHandler.start()

    def remove_thread(self, key):
        del self.threads[key]

    def list_threads(self):
        for name, thread in self.threads.items():
            print(name, thread)