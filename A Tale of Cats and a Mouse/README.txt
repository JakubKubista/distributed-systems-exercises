Author: Jakub Kubista
Course: Distributed Systems
Project: Big Exercises 2
Name: A Tale of Cats and a Mouse


Run:
1. Open three linux terminals.    
2. Get to username@melkki.cs.helsinki.fi in each of them.    
3. Steps in terminal 1:              
   a) Get to ukkoXXX.hpc.cs.helsinki.fi where XXX is random ukko node from file ukkonodes.txt
   b) Start mouse.py as: python3 mouse.py
4. Steps in terminal 2:               
   a) Get to ukko027.hpc.cs.helsinki.fi 
   b) Start listy.py as: python3 listy.py   
5. Steps in terminal 3:               
   a) Get to ukko027.hpc.cs.helsinki.fi 
   b) Start cordy.py as: python3 cordy.py 


Addition notes:
I started with implementation localy, but there were so many things different between local implementation and real simulation like this.
So I had of course a lot of problems with that mostly with cordy and mouse. At first I started with cordy like with client threat. And I made
chase_cat like a server and also client. I did it almost complete, so I took a lot of time and after that I read the text at first right, that
I don't need sending any messages, ony leave a command. Conclusion: think about app from high level, not only like about local app and read tasks thrice.