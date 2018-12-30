# Importing libraries
from socket import AF_INET as AI, socket as sc, SOCK_STREAM as SS
from threading import Thread as th

clients = {}
addresses = {}

serverHost = ''
serverPort = 33000
bufferSize = 1024
addr = (serverHost, serverPort)
server = sc(AI, SS)
server.bind(addr)

# Receives connection and asks the client to input their username
def incomingConnections():

    while True:
        client, client_addresses = server.accept()
        print("Server: %s has connected." % client_addresses)
        client.send(bytes("Please enter your username", "utf8"))

        addresses[client] = client_addresses
        th(target=handleClient, args=(client,)).start()

# Takes in the client's socket as an argument
def handleClient(client):
    name = client.recv(bufferSize).decode("utf8")
    greeting = 'Welcome to the chat server %s' % name
    client.send(bytes(greeting, "utf8"))
    msg = "%s connected" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name


    while True:
        msg = client.recv(bufferSize)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s disconnected" % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


if __name__== "__main__":
    server.listen(6)
    print("Server is running")
    print("Waiting for a client to connect")
    ACCEPT_THREAD = th(target=incomingConnections())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()



