# Importing the default Python GUI (Graphical User Interface) tool,
# the sockets as well as the two networking flags: AF_NET and SOCK_STREAM

import _tkinter  # default Python GUI building tool
from socket import socket  # TCP (Transmission Control Protocol)
# sockets for networking
from socket import AF_INET  # importing the first networking flag
from socket import SOCK_STREAM  # importing the second networking flag
from threading import Thread  # importing threads


# defining the two main methods: receive and send for messages

def receive_message(messsage_list=None):
    while True:
        try:
            message = client_socket.recv(buffer_size).decode("utf8")  # utf8 is a
            # unicode variable made for encoding words
            # by allocating one to four 8 bit bytes
            messsage_list.insert(_tkinter.END, message)
        except OSError:  # handling a Python built-in exception
            #  meant for when the user decides to leave the chat
            break  # break statement for ending this while-based infinite loop


def send_message(event=None, my_mesage=None):  # one of the arguments here is event because
    # it is passed by binders
    #  (i.e. tools that combine files together)
    message = my_mesage.get()  # getter method for the user to receive the message
    my_message.set(" ")  # setter method for a clear input field in the chat
    client_socket.send(bytes(message, "utf8"))  # command meant to send messages
    # to the server

    if message == "{quit}":
        client_socket.close()  # exit message which will close the socket
        top.quit()  # quitting the GUI application


def exit(event=None):
    my_message.set("{quit}")  # setting the input field to the quit message
    send_message()  # calling the send_message function in order to send messages to the server


# defining the top-level widget

top = _tkinter.Tk()  # variable used in the exit method
top.title("User")  # variable used in the exit method

messages_count = _tkinter.Frame(top)  # frame containing all the lists with messages
my_message = _tkinter.StringVar()  # string variable for the current message to be sent
my_message.set("Start chatting here.")  # setting up the string variable from above to a default
# on screen  expression
scroll = _tkinter.Scrollbar(messages_count)  # enabling the user to scroll down
# to previously-texted messages in the chat

message_list = _tkinter.Listbox(messages_count, height=20, width=50, yscrollcommand=scroll.set)
scroll.pack(side=_tkinter.RIGHT, fill=_tkinter.Y)
message_list.pack(side=_tkinter.LEFT, fill=_tkinter.BOTH)
message_list.pack()
messages_count.pack()

input_field = _tkinter.Entry(top, textvariable=my_message)
input_field.bind("Return", send_message)
input_field.pack()
send_button = _tkinter.Button(top, text="Send message", command=send_message)
send_button.pack()
top.protocol("Close window", exit)  # call to exit method
# when the user wants to quit the app

# The following lines of code will connect
# the client to the server

Host = input('Enter host name: ')
Port = input('Enter port code: ')
if not Port:
    Port = 33000
else:
    Port = int(Port)

buffer_size = 1024
address = (Host, Port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(address)

receive_thread = Thread(target=receive_message)
receive_thread.start()
_tkinter.mainloop()  # Starts up the GUI
