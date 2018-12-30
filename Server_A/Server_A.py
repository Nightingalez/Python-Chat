# Importing libraries
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

serverHost = ''
serverPort = 33000
bufferSize = 1024
addr = (serverHost, serverPort)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

# Receives connection and asks the client to input their username
def incomingConnections():

    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Please enter your username", "utf8"))

        addresses[client] = client_address
        Thread(target=handleClient, args=(client,)).start()

# Takes in the client's socket as an argument
def handleClient(client):
    name = client.recv(bufferSize).decode("utf8")
    greeting = 'Welcome to the chat server %s' % name
    client.send(bytes(greeting, "utf8"))
    msg = "%s connected" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

# Disconnects the users
    while True:
        msg = client.recv(bufferSize)
        if msg != bytes("/quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("/quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s disconnected" % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


server.listen(5)
print("Server is running")
print("Waiting for a client to connect")
ACCEPT_THREAD = Thread(target=incomingConnections())
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
server.close()



