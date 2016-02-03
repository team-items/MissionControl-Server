# MissionControl-Server
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/team-items/MissionControl-Server/blob/master/LICENSE)

Server implementation of MIDaC, designed to transmit sensor values from (currently) the KIPR Link to client devices supporting the MIDaC Protocol. 

###Installation on KIPR Link:
* Add the missing parts of the Python 2.7.2 stdlib into <code>/usr/lib/python2.7/</code>
* Copy the MissionControl-Server directory anywhere you want it on your link and switch into the directory
* Go into the MC2ML directory. Run <code>python MC2ML_Parser.py controller_files/KiprLink.xml</code> to generate a CONTROLLER.c file
* Copy the CONTROLLER.c file into the RSAL directory
* Go back into the MissionControl-Server directory and run <code>gcc -o RSAL/RSAL RSAL/RSAL.c -lkovan</code> to compile the native parts
* Start the server with <code>./main.py</code> (you might need to change the files permissions to execute)
