from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receiveMessage():
    while True:
        try:
            message = c_socket.recv(buffersize).decode("utf8")
            message_list.insert(tkinter.END, message)
        except OSError:  # Client has left the chat.
            break


def sendMessage(event=None):
    message = my_message.get()
    my_message.set("")
    c_socket.send(bytes(message, "utf8"))
    if message == "{quit}":
        c_socket.close()
        top.quit()


def onExit(event=None):
    my_message.set("{quit}")
    sendMessage()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_message = tkinter.StringVar()
my_message.set("Type your message here: ")
scrollbar = tkinter.Scrollbar(messages_frame)

message_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
message_list.pack()

messages_frame.pack()

chat_box = tkinter.Entry(top, textvariable=my_message)
chat_box.bind("<Return>", sendMessage)
chat_box.pack()

top.protocol("WM_DELETE_WINDOW", onExit)

host = input('Enter host: ')
port = input('Enter port: ')

if not port:
    port = 33000
else:
    port = int(port)

buffersize = 1024
addr = (host, port)
c_socket = socket(AF_INET, SOCK_STREAM)
c_socket.connect(addr)

receive_thread = Thread(target=receiveMessage)
receive_thread.start()
tkinter.mainloop()