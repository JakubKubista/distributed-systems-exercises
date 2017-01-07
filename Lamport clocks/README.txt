Author: Jakub Kubista
Course: Distributed Systems
Project: Big Exercises 1
Name: Lamport clocks

Basically a server thread who listen on its port a client thread sends  randomly 
messages to other known servers

The global variable CLOCK does not need any lock, cause as i read on the internet, 
reading or replacing a single global variable is thread-safe

ive got some troubles sending/receiving the data from the socket - that stuff must
be en/decoded with utf8

As I said in the specs "The actual contents of the messages are irrelevant" i don't send
any other information.



Run:
python3 program.py config.txt 1