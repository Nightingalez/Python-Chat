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
# TCP sockets are used, indicated by the flags 'AF_INET' and 'SOCK_STREAM'
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)



def userConnection():

# Infinite while-loop that waits for incoming connections.
    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=clientMessages, args=(client,)).start()

def clientMessages(client): # Takes client socket as parameter
    # Save the user's chosen name
    name = client.recv(buffersize).decode("utf8")
    # Prints messages to all clients
    welcome = 'Welcome %s! To quit, type /quit to exit.' % name
    client.send(bytes(welcome, "utf8"))
    # User has joined
    message = "%s has joined the chatroom!" % name
    broadcast(bytes(message, "utf8"))
    clients[client] = name

    # Infinite while-loop that exits the program if "/quit"
    # is sent from the client. If not, the messages are
    # broadcast to all clients
    while True:
        message = client.recv(buffersize)
        if message != bytes("/quit", "utf8"):
            broadcast(message, name+": ")
        else:
            # Exit program and delete client entry.
            client.send(bytes("/quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chatroom!" % name, "utf8"))
            break

# This function sends 'message' to all clients
def broadcast(message, prefix=""): # prefix is for name identification
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + message)

# Main:
server.listen(5) # Listens for 5 connections at maximum.
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=userConnection())
ACCEPT_THREAD.start() # Starts the infinite loop.
ACCEPT_THREAD.join()
server.close()
