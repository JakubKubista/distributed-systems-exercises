# coding: utf-8

# Chase_cat is a file represents cats Catty and Jazzy which works like clients for two servers Listy and Mouse.
# Program is started by Cordy and we can use this class for as many searching cat as we need, if we implement them in Cordy.


import socket
import sys
from threading import Thread
import random
from time import sleep

#  Function for read one line from file as listy_location.txt and port_number.txt.

def readOneLineFile(name):
    text = ""
    try:
        with open(name) as f:
                text = f.read()
        f.close()  
    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return text

#  	Class for chase cat has basicly 3 parts as constructor, connection for mouse and conncetion for listy cat.

class ConnectSearchingCat(Thread):

#  	Constructor connect searching cat to chosen ukko node, which was chosen by cordy.

    def __init__(self, port, command, name):
        Thread.__init__(self)
        self.port = int(port)
        self.found = 0		    #  If was mouse found by this cat.
        self.got = 0		    #  If was mouse got by this cat.
        self.command = command  #  What should cat do.
        self.host = socket.gethostname()  #  Which ukko node mouse connected.
        self.name = name
		
#  	Starting client by start method.

    def run(self):

#  If is client started and mouse wasn't catch then in this method will cat try accomplish requests from Cordy as catch or attack mouse.
	
        if(self.got == 0):
            mouseSocket = socket.socket()
            try:
                mouseSocket.connect((self.host,self.port))				
                if (self.command == "S"):				# If cat is successfully connected and searching the mouse. 
                    print (self.name + ' tried: ' + self.host.rstrip('\n') + ' - Mouse')	# Report about where mouse is.
                    self.found = 1
                    message = (self.name + ": -")		# Cat send her name to the mouse, because we want to know who found her.
                    mouseSocket.send(message.encode())
    
                if (self.command == "A"):				# If cat is successfully connected and attacking on the mouse.                     
                    message = (self.name + ": MEOW")		# Message for the mouse about attacking.
                    mouseSocket.send(message.encode())
                    sleep(6)		# The attack on the mouse takes 6 seconds.
                    data = mouseSocket.recv(1024).decode()
                    print (data) 
                    self.got = 1
                mouseSocket.close()

            except socket.error as e:
                print (self.name + ' tried: ' + self.host.rstrip('\n'))		# We want to know which ukko node we already tried.

#  If is client started and mouse wasn't catch, then in this method will cat connect to Listy and send report about situation, like if was mouse caught or got.
				
        if(self.found == 1 or self.got == 1):
            listySocket = socket.socket()
            listyNodeNumber = str(readOneLineFile("listy_location.txt")).rstrip('\n')
            listyNode = (listyNodeNumber + ".hpc.cs.helsinki.fi")		# Connect to Listy ukko node from file with listy location.
            try:
                listySocket.connect((listyNode,self.port))
                if(self.found == 1 and self.got == 0):			# Mouse was found. 
                    message = ("F " + self.host.rstrip('\n') + " "  + self.name)	# Send F message to Listy. 
                    listySocket.send(message.encode())

                if(self.got == 1):								# Mouse was got. 
                    message = ("G " + self.host.rstrip('\n') + " " + self.name)		# Send G message to Listy. 
                    listySocket.send(message.encode())
                listySocket.close()

            except socket.error as e:
                print (self.name + ' - cannot connect to Listy')            


#  Main method to create and start client also known as Chase cat. Init also calling a method with return port number in header, command and name of cat.
	
def Main(command,name):
    chaseCat = ConnectSearchingCat(readOneLineFile("port_number.txt"),command,name) 
    chaseCat.start()

#  User 2,3 fields from sys.argv array, becouse were used python3  -u - --opt -> more in cordy.py
	
if __name__ == "__main__": Main(sys.argv[2], sys.argv[3])
