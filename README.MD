# SupermarketQueueSimulation 
This is a python Event Based simulation implementation of a store formed by 1 queue, 4 supermarket checkouts and 3 possible types of clients:

- Client with no doubts (less use time) 
- Client with some doubts (medium use time) 
- Client with lots of doubts (long use time) 
  
If any of these entities wait for more than 15 minutes in the queue they leave.

To execute the simulation just run main.py and introduce the requested configuration parameters.
Simulation may stop on its own when no more events remain in the events list. 