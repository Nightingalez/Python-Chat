from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


# Assigning dictionaries for clients
clients = {}
addresses = {}

# host will be assigned an IP, chosen by the client
host = ''
# The default port is set to 33000
port = 33000
buffersize = 1024
addr = (host, port)
# TCP sockets are used
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)

def userConnection():

    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave!" +
                          "Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client): # Takes client socket as parameter
    name = client.recv(buffersize).decode("utf8")
    welcome = 'Welcome %s! To quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    message = "%s has joined the chat!" % name
    broadcast(bytes(message, "utf8"))
    clients[client] = name

    while True:
        message = client.recv(buffersize)
        if message != bytes("{quit}", "utf8"):
            broadcast(message, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat!" % name, "utf8"))
            break

def broadcast(message, prefix=""): # prefix is for name identification
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + message)

server.listen(5) # Listens for 6 connections at max.
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=userConnection())
ACCEPT_THREAD.start() # Starts the infinite loop.
ACCEPT_THREAD.join()
server.close()
