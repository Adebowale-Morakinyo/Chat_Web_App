from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
BUFSIZ = 1024
ADDR = (HOST, PORT)


class Client:
    """Handles communication with server."""

    def __init__(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.msg_list = []
        self.client_lock = Lock()  # safe memory access

        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        self.send(name)

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(BUFSIZ).decode("utf8")
                self.client_lock.acquire()
                self.msg_list.append(msg)
                self.client_lock.release()
                # print(msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(self, msg):
        """Handles sending of messages."""
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_lock.acquire()
            self.client_lock.release()
            self.client_socket.close()

    def get_messages(self):
        """Returns a list of messages(str)."""
        messages_cpy = self.msg_list[:]

        self.client_lock.acquire()
        self.msg_list = []
        self.client_lock.release()

        return messages_cpy

    def disconnect(self):
        self.send("{quit}")
