from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

#function for receiving messages
def receiveMessage():
    while True:         #we use an infinite loop so that the messages can be received at any time
        try:
            message = c_socket.recv(buffersize).decode("utf8")  #recv() stops the execution until a message is received
            message_list.insert(tkinter.END, message)   #the message is appended to message_list
        except OSError:  # Client has left the chat.
            break

#function for sending messages
def sendMessage(event=None):    #the event is passed implicitly by Tkinter
    message = my_message.get()  #my_message is the input field in the  GUI
    my_message.set("")  #input field is cleared
    c_socket.send(bytes(message, "utf8"))
    if message == "/quit":  #if the message is "/quit", the socket is closed and then the GUI is closed as well
        c_socket.close()
        top.quit()

#function that closes the GUI window
def onExit(event=None):
    my_message.set("/quit")
    sendMessage()


top = tkinter.Tk()  #defining the top level widget
top.title("Chat")   #setting the name of the GUI window

messages_frame = tkinter.Frame(top) #creating the frame for the messages
my_message = tkinter.StringVar()    #creating a string that holds the values from the input field
my_message.set("Enter message: ")
scrollbar = tkinter.Scrollbar(messages_frame)   #scroll bar to see older messages

message_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
message_list.pack()

messages_frame.pack()   #the message liost is stored in messages_frame, and then packed together with all the other GUI elements

chat_box = tkinter.Entry(top, textvariable=my_message)  #input field is created
chat_box.bind("<Return>", sendMessage)  #the return key is bound to the sendMessage function
chat_box.pack()

top.protocol("WM_DELETE_WINDOW", onExit)

host = input('Enter host: ')    #command for entering the IP address of the host
port = input('Enter port: ')    #command for entering the port

if not port:
    port = 33000    #default port value
else:
    port = int(port)    #else use the port defined by the user

buffersize = 1024
addr = (host, port)
c_socket = socket(AF_INET, SOCK_STREAM) #socket is created
c_socket.connect(addr)  #connect to socket

receive_thread = Thread(target=receiveMessage)  #start thread for receiving messages
receive_thread.start()  #start main loop for the GUI
tkinter.mainloop()  