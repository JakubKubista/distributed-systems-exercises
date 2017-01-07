# coding: utf-8

# Cordy is a file represents class Cordy cat, which coordinate cats Catty and Jazzy.
# This Class could be upgrade to more dynamic version, if we want add searching cats in future.
# In this file is a little problem about sending commands to chase_cat.py, which wasn't fixed and is commented below.

import random
from time import sleep
import subprocess
import os

#  Function for read one line from file as listy_location.txt.
#  This ukko node in listy_location.txt is base node for Jazzy and Catty, before they leave to find mouse.

def readOneLineFile(fileName):
    text = ""
    try:
        with open(fileName) as f:
                text = f.read()
        f.close()  
    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return text

# Procedure, which prepare CMSG file for reports from chase cats.
# It's called at the beginning of program and clear the CMSG file. 
    
def prepareCMSGFile():
    try:
        with open("cmsg.txt","r+b") as f:
            f.truncate()
        f.close()  
    except IOError:
        raise Exception('IO exeption - Unreadable file')

#  Function read last line from CMSG file and use it as instruction for chase cats.

def readCMSGFile():
    text = ""
    try:
        with open("cmsg.txt","r") as f:
            for line in (line for line in f if line.rstrip('\n')):
                text = line
        f.close()  

    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return text

    
#  Function is called from readNodeFile and return two random addresess.
#  Each of addresess contains different ukko node than other address.
#  It should be okay without loop, but sometimes were same nodes without loop.

def choseRandomAddresses(nodes):
    firstAddress,secondAddress=("","")
    while(firstAddress==secondAddress):
        random.shuffle(nodes)
        firstNode = str(nodes[0]).rstrip('\n')
        secondNode = str(nodes[1]).rstrip('\n')
        firstAddress = (firstNode + ".hpc.cs.helsinki.fi")
        secondAddress = (secondNode + ".hpc.cs.helsinki.fi")
    return (firstAddress,secondAddress)
    
#  Function read file of ukko nodes and add them into array nodes. 
#  Then calling choseRandomAddresses function and returning addresess.

def readNodeFile():
    nodes = []
    firstAddress,secondAddress = "",""
    secondAddress = ""
    try:
        with open("ukkonodes.txt") as f:
            for line in f:
                nodes.append(line)
        firstAddress, secondAddress = (choseRandomAddresses(nodes))
        f.close()  

    except IOError:
        raise Exception('IO exeption - Unreadable file')
    return (firstAddress,secondAddress)

#  Here is solution for avoid already visited nodes.

"""
def narrowNodes(nodes,lastCatty,lastJazzy):
    print(str(nodes))
    for node in nodes:
        if(node == lastCatty):
            nodes.remove(node)
    for node in nodes:
        if(node == lastJazzy):
            nodes.remove(node)
    print(str(nodes))
    return nodes   
    # nodes = narrowNodes(nodes,firstCatNode,secondCatNode)
"""

#  First step in the tale, in which we connect file of chase cats to other network.
#  They are send by random node to find the mouse.

def randomCoordinate(catName, catNode):

    #Caught error - python: can't open file 'S': [Errno 2] No such file or directory
    #Found a few fix for this error like:
    # https://github.com/ansible/ansible/issues/15457
    # http://serverfault.com/questions/161117/cron-job-errno-2-no-such-file-or-directory

    
    catCommand = ("ssh " + catNode + " python3  -u - --opt S " + catName + "  < chase_cat.py")
    subprocess.Popen([catCommand], shell = True)  
    return 1;
    # I tried many other solutions, e.g.:    
    # 1. solution
    #prog = subprocess.Popen(["ssh", catNode, 'python3 chase_cat.py S ' + catName], stderr=subprocess.PIPE)
    #errdata = prog.communicate()[1]
    
    # 2. solution
    #client = SSHClient()   # from paramiko import SSHClient
    #client.load_system_host_keys()
    #client.connect(catNode) 
    #stdin, stdout, stderr = client.exec_command('python3 chase_cat.py S ' + catName)
    
    # 3. solution
    #s = pxssh.pxssh()   # from pexpect import pxssh
    #s.login (catNode)
    #catCommand = ("python3 S " + catName + "  < chase_cat.py")
    #subprocess.Popen([catCommand], shell = True)

    
#  Second step in the tale, in which we connect file of chase cat to other network.
#  She is send by node, where was mouse found by other cat.

def secondCoordinate(attack, lastCommand, catName, catBool):
    if((attack == 0) and (str(lastCommand[0])=="F") and (str(lastCommand[2]).rstrip('\n') != catName) and (catBool == 0)): 
        print("secondCoordinate sleep 12")
        sleep(12) # Jazzy and Catty need 12 seconds to search one node.
        mouseAddress = (lastCommand[1] + ".hpc.cs.helsinki.fi")  # Know ukko node from CMSG file. 
        catCommand = ("ssh " + mouseAddress + " python3  -u - --opt S "+ catName + "  < chase_cat.py")
        subprocess.Popen([catCommand], shell = True)
        catBool = 1 # Which cat is the second one.
        attack = 1 # After this step is possible to start attack.

    return catBool,attack
    
#  Third step in the tale, in which we connect file of chase cat to other network.
#  In this moment both cats found mouse and one of them is able to attack mouse. 
#  Basicly the second one in CMSG file.

def attackAllowed(attack, lastCommand, catName):
    if((attack == 1) and (str(lastCommand[2]).rstrip('\n') != catName)): 
        mouseAddress = (lastCommand[1] + ".hpc.cs.helsinki.fi") 
        catCommand = ("ssh " + mouseAddress + " python3  -u - --opt A "+ catName + "  < chase_cat.py")
        subprocess.Popen([catCommand], shell = True)
        attack = 2 # After this step attack finished.
    return attack

#  Only for sure, that G was written into the CMSG file.

def assuranceOfEnd(attack,lastCommand,catName):
    if((str(lastCommand[0])=="G") and (str(lastCommand[2]).rstrip('\n') == catName)): 
        print("THE END OF TALE - mouse caught by " + catName)  
        attack = 3 # After this step loop over.
    return attack

#  Class for cordy has simple logic:
#       To find mouse we have 3 steps for each cat. 
#       1. randomCoordinate: Random choice of ukko nodes by readNodeFile() and send cats to these nodes at the same time.
#       2. secondCoordinate: One of cat found mouse and Cordy send second cat to this node.  
#       3. attackAllowed: Both cats found the mouse and one of them is going to attack.
#       4. assuranceOfEnd: Secure, that we have complete report of tale.   
     
#  It's also possible to create another class above, in which we will call these steps and have solution for more searching cats.
class ConnectCordy():

    def __init__(self):
        self.attack = 0 # progress of tale..0 = start, 3 = end 
        self.catty = 0 # if catty found the mouse - important to know who is who
        self.jazzy = 0

    def coordinateToMouse(self):
        prepareCMSGFile() # delete prevously tale
        listyNode = readOneLineFile("listy_location.txt")
        firstCatNode,secondCatNode = (listyNode,listyNode) # starting positions
        cattyString, jazzyString = "Catty","Jazzy"
        lastCommand = ["","",""] # if will be problems with CMSG File

        while self.attack != 3:
            lastCommand = readCMSGFile().split(' ')
            firstCatNode,secondCatNode = readNodeFile()
            randomCatty, randomJazzy = (0,0)
#           1. Step 
            if((self.attack == 0) and (str(lastCommand[0])!="F")):
                sleep(12)        #   Jazzy and Catty need 12 seconds to search one node.
                randomCatty = randomCoordinate(cattyString, firstCatNode)
            if((self.attack == 0) and (str(lastCommand[0])!="F")):
                randomJazzy = randomCoordinate(jazzyString, secondCatNode)
            if((randomCatty == 1) and (randomJazzy == 1)):
                print("")
                
#           2. Step 
            self.catty, self.attack = secondCoordinate(self.attack,lastCommand,cattyString, self.catty)
            self.jazzy, self.attack = secondCoordinate(self.attack,lastCommand,jazzyString, self.jazzy)

#           3. Step 
            self.attack = attackAllowed(self.attack,lastCommand,jazzyString)
            self.attack = attackAllowed(self.attack,lastCommand,cattyString)

#           4. Step 
            self.attack = assuranceOfEnd(self.attack,lastCommand,cattyString)
            self.attack = assuranceOfEnd(self.attack,lastCommand,jazzyString)
            
#  Main method contain only command of creat and run Cordy

def Main():
    Cordy = ConnectCordy().coordinateToMouse() 

if __name__ == "__main__": Main()
