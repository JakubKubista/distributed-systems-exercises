# coding: utf-8

# Mouse is a Thread class which works like a listening server for Catty and Jazzy.

import socket
from threading import Thread
import random
from time import sleep
import os 

#  Function for read one line from file as port_number.txt.  
  
def readPortFile():
    port = ""
    try:
        with open("port_number.txt") as f:
                port = f.read()
        f.close()  
    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return port
    
#  Function read file of ukko nodes and return one random ukko node.

def readNodeFile():
    nodes = []
    node = ""
    try:
        with open("ukkonodes.txt") as f:
            for line in f:
                nodes.append(line)
        random.shuffle(nodes)   # I Wasn't use random.choice(nodes), becouse this solution is faster - no loop.
        node = str(nodes[0]).rstrip('\n')
        f.close()    

    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return node

#  Class which represents mouse and her actions

class ConnectMouse(Thread):

#  	Constructor connect Mouse to .
#  	As you can see,I tried to connect mouse by choiced ukko node
#   But it was never ending loop with badly closed connections 
#  	After that mouse start listening here and waiting for cats. Init has also essential secure as exeption.

    def __init__(self, port):
        Thread.__init__(self)
        self.port = int(port)
        self.mySocket = socket.socket()
        self.wasted = 0         # True if was mouse attacked.
        
        #node = readNodeFile()   # Random ukko node.
        #host = (node + ".hpc.cs.helsinki.fi")
        #command = ("ssh " + host + " python  -u - --opt < mouse.py")
        #os.system(command)

        host = "0.0.0.0" #  host will be listening for everything on this ukko node
        node = socket.gethostname() # Function returns host where mouse actually is.
        host = (node + ".hpc.cs.helsinki.fi")
        try:
            self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.mySocket.bind((host,self.port))
            self.mySocket.listen(2)
            print ("Mouse location: ('" + node +".hpc.cs.helsinki.fi', " + str(self.port) +")")

        except socket.error as msg:
            self.mySocket.close()
            self.mySocket = None
            print(msg)
            
#  Server is listening until mouse won't be attacked by cats.
#  If it's started and Catty or Jazzy try to connect then it create connection.
#  Then mouse will wait for message from one of chase cats.
#  In the first case message contains only name of cat, so now mouse can identify who found her.
#  In the second case it is MEOW message and mouse is under attack.
#  In the second case, she have to answer by OUCH message and end listening for cats.
    def run(self):
        while True and self.wasted!=1:
            conn, addr = self.mySocket.accept()
            data = conn.recv(1024).decode()
            text = data.split(' ')
            if not data:
                break

            if(text[1]=="-"):
                print (str(text[0]) + " found me")

            if(text[1]=="MEOW"):
                print (str(data))
                data = ("Mouse: OUCH")
                sleep(8)		# The attacking cat will wait 8 seconds for the OUCH message.
                conn.send(data.encode()) 
                self.wasted=1   # Attacked 
                conn.close()

#  Main method to create and start server also known as Mouse.
#  Init also calling a method with return port number in header.			

def Main():
    mouse = ConnectMouse(readPortFile()) 
    mouse.start()


if __name__ == "__main__": Main()
