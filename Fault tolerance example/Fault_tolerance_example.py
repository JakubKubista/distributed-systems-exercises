# coding: utf-8

# Jakub Kubista
# Distributed Systems : Big Exercise 3
# Program Fault_tolerance_example contains 3 fault methods.
# Faults represents identifiers of errors or failures.

import sys
from time import sleep
import random
 
# Latent fault for the main program.
# TypeError: unsupported operand type(s) for +: 'int' and 'str'
# The error describe, how easily we can make latent typing error,
# which we can find after a long time in bigger project.
# Solution for these type of mistake could be strong tests or fault-tolerant programs. 
# For example check and correction of every used value.

def isNumber(args):
    result = False
    sec_args = "58*"

    try:
       result = int(args)
       if(int(args)==725): # 725 is number which show latent fault
            args = int(args) + sec_args # latent fault
    except ValueError:
       print("That's not an int.")

    return bool(result)

# The first error
# Error reference on undesired state of the part of resource.
# Error detected by the main program and handled (tolerated) by method invocation.
# Error: division by zero (basic mathematical mistake)

def calculate(args,factor):
    try:
        args = int(args) / int(factor)
        args = round(args,1)
        print("Result: " + str(args))
    except Exception as e:
        print("Error: " + str(e) )
        factor = input("Enter a new factor: ")
        calculate(args,factor)

# The second error, which is on same principal like previously, 
# but I'm introducing it for sure, that I understood to the question. 
# Maybe it is not too generaly, just like the last one - save memory
# by using less variables while developer's writing code fast,
# but the point is same.
# Error detected by the main program and handled (tolerated) by method invocation. 
# Thus, error can be handle very easily, but only in case, that
# code has been  written carefully and not only in the best option.
# TypeError: 'int' object is not subscriptable

def splitSentence(sentence):
    print("\r")
    print("Alternative method 2 - Print words from sentence")
    try:
        words = sentence.rsplit(" ")
        for words in range(1,5):
            print (words, ":", words[words])
    except:
        print("Type: ", sys.exc_info()[0])
        print("Message: ", sys.exc_info()[1])
        print("Traceback: ", sys.exc_info()[2])   

        words = sentence.rsplit(" ")        
        for i in range(1,5):
            print (i, ":", str(words[i]))

# Left unhandled failure by the main program.
# Failure occurs whenever the actual service delivered by a system deviates from its expected service.
# For example we can imagine, that knight fighting with dragon.
# Program should end, when dragon die (health = 0), but it still continue, because dragon loses his life by sums and not by units of damage.

def theFairyTale():
    print("\r")
    print("Method 3 - The Fairy Tale")
    health = 100
    i = 0
    fullHealth = health
    while not (health==0):
        dmg = random.randint(10, 20)
        health = health - dmg
        health_p = round((health/fullHealth)*100,1)
        print ("Dragon health: " + str(health_p) + "%")
        sleep(0.5)
        i = i + 1
        if (i == 10):
            print ("Dragon must be alrady dead") # min. dmg = 10, hp = 100
            break

# Methods are called one by one in Main funtion.

def Main():
    print("Methods 1 and 2 - simple division")
    args = input("Enter your input number: ")
    sentence = ("So many errors and failures in this code.")
    factor = 0
    
    if(isNumber(args) == True): # latent fault
        calculate(args,factor) # method contains handled error

    splitSentence(sentence) # method contains handled error - moreover

    theFairyTale() # method contains failure

if __name__ == "__main__": Main()