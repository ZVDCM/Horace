import pickle
import zlib

HEADER_LENGTH = 10
FORMAT = "utf-8"

def receive_message(socket):
    try:
        message_header = socket.recv(HEADER_LENGTH)

        message_length = int(message_header.decode(FORMAT))
        message_data = socket.recv(message_length)

        while len(message_data) != message_length:
            remainder = message_length - len(message_data)
            message_data += remainder 

        return pickle.loads(zlib.decompress(message_data))
    except:
        return False