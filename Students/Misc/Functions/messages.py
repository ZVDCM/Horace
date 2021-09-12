import pickle
import zlib

HEADER_LENGTH = 10
FORMAT = "utf-8"


def serialize_message(message):
    data = zlib.compress(pickle.dumps(message, pickle.HIGHEST_PROTOCOL), 9)
    return f"{len(data):<{HEADER_LENGTH}}".encode(FORMAT) + data


def normalize_message(type, message, target=None, sender=None):

    message = {
        "type": type,
        "data": message,
        "target": target,
        "sender": sender,
    }

    return message


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            raise Exception

        message_length = int(message_header.decode(FORMAT))
        message_data = client_socket.recv(message_length)

        while message_length != len(message_data):
            remainder = message_length - len(message_data)
            message_data += client_socket.recv(remainder)

        return pickle.loads(zlib.decompress(message_data))

    except:
        return False


def send_message(message, client_socket):
    client_socket.send(message)
