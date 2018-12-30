"TCP network socket, using AF_INET and SOCK_STREAM flags"
from socket import AF_INET, socket, SOCK_STREAM

"Threadin libray, to utilize several CPU's at the same time"
from threading import Thread


def accept_incoming_connections():
    "Registers incoming clients and adds the them to a client address list (client_address)"
    while True:
        "Accepts a connection and returns a variable of type (conn, address)"
        "'conn' is a socket object that send an receive data"
        "'address' is the address where from the socket (conn) are bound to"
        client, address_from_client = SERVER.accept()

        "'%s:%s is used to have a string placeholder for both the conn and address"
        print("%s:%s has connected." % address_from_client)

        ".send sends the bytes value into the client variable"
        "bytes() is a method that returns an immutable integer ranging from 0-256"
        "the two parameters used in bytes() is the source (client) and -"
        "the encoding (utf8) since the source is a string"
        client.send(bytes("Greetings. Pls type your name and hit enter.", "utf8"))

        "Adds the input from the user to the address client list"
        addresses[client] = address_from_client

        "Separates the tasks to the CPU's using threading.Thread() method"
        "target= is the target which needs to be threaded"
        "args= takes the potential clients which needs to be threaded if there is several of them"
        Thread(target=client_handler, args=(client,)).start()


def client_handler(client):
    "Takes one client connection"

    "recv(BUFSIZ) recvieves data from the socket and returns it as a sring"
    "the maximum amount of data possible is defined by the BUFSIZ, which in this case is 1024"
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s. Type {quit} to exit the program.' % name
    client.send(bytes(welcome, "utf8"))
    server_status = "%s is online" % name
    broadcast(bytes(server_status, "utf8"))

    "Adds the user to a client list"
    clients[client] = name

    while True:
        server_status = client.recv(BUFSIZ)
        if server_status != bytes("{quit}", "utf8"):
            broadcast(server_status, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()

            "delets the client from the client list, when done"
            del clients[client]
            broadcast(bytes("%s left the chat room." % name, "utf8"))
            break


def broadcast(server_status, prefix=""):  # prefix is for name identification.
    "Sends message to all clients"

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + server_status)


clients = {}
addresses = {}

HOST = ''
"1024 through 49151: Registered Ports"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    "sets the possible amount of unaccpted connection, which is 5 in this case"
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()