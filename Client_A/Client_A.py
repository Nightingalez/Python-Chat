from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

'''The following functions deal with recieveng and sending messeges in the client'''

'''This function recieves the messeges'''
def msgRecieve():
    while True:
        try:
            msg = clientSocket.recv(bufferSize).decode("utf8") #Stops execution of the loop until a message is recieved
            msgList.insert(tkinter.END, msg) #A list which holds the recieved message
        except OSError:
            break

'''This function sends the messeges'''
def msgSend(event = None):
    msg = myMsg.get()
    myMsg.set("") #The place where the user writes the messege
    clientSocket.send(bytes(msg, "utf8")) #The client socket seneds the message to the server
    #This if- statement checks if /quit is written; if it is, it stops the client from sending messeges
    if msg == "/quit":
        clientSocket.close()
        top.quit()

'''This function closes the socket before the GUI gets closed'''
def scktClose(event = None):
    myMsg.set("/quit") #The input field is set to {Quit}
    msgSend() #The msgSend funciton, defined above, gets called and executed

'''GUI build'''

top = tkinter.Tk() #Defines a Tkinter Top-level Widget (the chat window)
top.title("Simple Chat") #Sets the title for the chat window

msgFrame = tkinter.Frame(top) #Groups all other widgets into a complex layout
myMsg = tkinter.StringVar() #A string which holds the username and the messages that are sent
myMsg.set("Enter message here") #Setting the username
sb = tkinter.Scrollbar(msgFrame) #Creates a scrollbar for the frame, so the user can navigate through previous messages

msgList = tkinter.Listbox(msgFrame, height = 30, width = 60, yscrollcommand = sb.set) #Defines a message list, which will hold the messeges
sb.pack(side = tkinter.RIGHT, fill = tkinter.Y) #Placement of the scrollbar
msgList.pack(side = tkinter.LEFT, fill = tkinter.BOTH) #Placement of the list
msgList.pack()
msgFrame.pack()

chatEntry = tkinter.Entry(top, textvariable = myMsg) #Messege box
chatEntry.bind("<Return>", msgSend) #Sends the message when the user presses Return/Enter
chatEntry.pack()
sendButton = tkinter.Button(top, text = "Send message", command = msgSend) #Creates a "Send message" button in case the user wants to use a button
sendButton.pack()

top.protocol("WM_DELETE_WINDOW", scktClose)

'''Connecting the client to the server'''

serverHost = input('Enter host (IP): ') #Server IP as an input
serverPort = input('Enter port: ') #Server port as an input

if not serverPort:
    serverPort = 33000 #Default value for the port
else:
    serverPort = int(serverPort)

bufferSize = 1024
addr = (serverHost, serverPort) #Server address
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(addr)

recieveThread = Thread(target = msgRecieve) #A thread object for receiving messeges
recieveThread.start() #This method changes the thread state to runnable; a run method is called on the thread object, when it gets started
tkinter.mainloop() #Executes the GUI