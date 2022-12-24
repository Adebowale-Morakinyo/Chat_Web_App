from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from user import User

# GLOBAL VARIABLES
users = []
addresses = {}

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        try:
            client, client_address = SERVER.accept()  # wait for new connection
            user = User(client_address, client)
            users.append(user)

            print(f"{client_address} has connected.")
            Thread(target=handle_client, args=(user,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print('SERVER CRASHED')


def handle_client(user):  # Takes user object as argument.
    """Handles a single client connection."""
    addr = user.addr
    client = user.client  # client socket
    name = client.recv(BUFSIZ).decode("utf8")  # gets user's name
    user.set_name(name)

    msg = f"{name} has joined the chat!"
    broadcast(bytes(msg, "utf8"))

    while True:
        try:
            msg = client.recv(BUFSIZ)
            print(f"{name}: ", msg.decode("utf8"))

            if msg == bytes("{quit}", "utf8"):
                # client.send(bytes("{quit}", "utf8"))
                client.close()
                users.remove(user)
                broadcast(bytes(f"{name} has left the chat.", "utf8"))
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name+": ")
        except Exception as e:
            print("[EXCEPTION]", e)
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for user in users:
        sock = user.client
        sock.send(bytes(prefix, "utf8") + msg)


if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
