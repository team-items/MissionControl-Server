# MissionControl-Server
Server implementation of MIDaC, designed to transmit sensor values from (currently) the KIPR Link to client devices supporting the MIDaC Protocol. 

###Installation on KIPR Link:
* Add the missing parts of the Python 2.7.2 stdlib into <code>/usr/lib/python2.7/</code>
* Copy the MissionControl-Server directory anywhere you want it on your link
* Go into the MissionControl-Server directory and run <code>gcc -o RSAL/RSAL RSAL/RSAL.c -lkovan</code> to compile the native parts
* Start the server with <code>./main.py</code>
