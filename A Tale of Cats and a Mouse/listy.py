# coding: utf-8

# Listy cat is a Thread class which works like a listening server for Catty and Jazzy.

import socket
from threading import Thread
import random
  
#  Function for read one line from file as listy_location.txt and port_number.txt.
  
def readFile(fileName):
    text = ""
    try:
        with open(fileName) as f:
                text = f.read()
        f.close()  
    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return text

#  Procedure for write last received message from chase cats to cmsg.txt file as last line.

def writeFile(text):
    try:
        with open("cmsg.txt","r+b") as f:
            f.read()
            f.write(bytes(text, 'UTF-8')) #  Example: F/G ukkoXXX catname
        f.close()  
    except IOError:
        raise Exception('IO exeption - Unreadable file')

#  Function for printing and formating incoming data for write to cmsg.txt and also returning type of message.

def saveData(data):
    print ("Saving report: (" + str(data) + ")")
    writeFile(str(data) + "\n")
    data = data.split(' ')
    return data[0]

	
class ConnectListy(Thread):

#  	Constructor connect Listy to chosen ukko node from files and start listening here. Init has also essential secure as exeption.

    def __init__(self, port):
        Thread.__init__(self)
        self.port = int(port)
        self.mySocket = socket.socket()
        node = str(readFile("listy_location.txt")).rstrip('\n')	# rstrip was needed, because sometimes was there empty last line sometimes not
        host = (node + ".hpc.cs.helsinki.fi")
        try:
            self.mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# try if it's empty socket 
            self.mySocket.bind((host,self.port))
            self.mySocket.listen(2)
            print ("Listy location: ('" + str(host) +"', " + str(self.port) +")")

        except socket.error as msg:
            self.mySocket.close()
            self.mySocket = None
            print(msg)
            print ("Listy cannot connect to ukko node")
			
#  Server is listening until message G arrives.
#  If it's started and Catty or Jazzy try to connect then it create connection and call save method.

    def run(self):
        command = ""
        while True and command!="G":	# If was mouse cought close connections.
            conn, addr = self.mySocket.accept()
            data = conn.recv(1024).decode()
            if not data:
                break
            command = saveData(data)
            conn.close()

#  Main method to create and start server also known as Listy cat. 
#  Init also calling a method with return port number in header.
		
def Main():
    Listy = ConnectListy(readFile("port_number.txt")) 
    Listy.start()


if __name__ == "__main__": Main()
