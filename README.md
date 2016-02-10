# MissionControl-Server
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](https://github.com/team-items/MissionControl-Server/blob/master/LICENSE)

Server implementation of MIDaC, designed to transmit sensor values from (currently) the KIPR Link to client devices supporting the MIDaC Protocol. 

###Installation on KIPR Link:
* Add the missing parts of the Python 2.7.2 stdlib into <code>/usr/lib/python2.7/</code>
* Copy the MissionControl-Server directory anywhere you want it on your link and switch into the directory
* Run <code>python MC2ML/MC2ML\_Parser.py KiprLink.xml</code> to compile and generate the specific part for the KIPR Link (if you have an adapted MC2ML file store it in the MC2ML/controller_files directory and use it's file name instead of 'KiprLink.xml')
* Start the server with <code>./main.py</code> or <code>python main.py</code> (you might need to change the files permissions to execute)

###Installation on KIPR Wallaby:
* Add the missing parts of the Python 2.7.9 stdlib into <code>/usr/lib/python2.7/</code>
* Copy the MissionControl-Server directory anywhere you want it on your link and switch into the directory
* Run <code>python MC2ML/MC2ML\_Parser.py KiprWallaby.xml</code> to compile and generate the specific part for the KIPR Wallaby (if you have an adapted MC2ML file store it in the MC2ML/controller_files directory and use it's file name instead of 'KiprWallaby.xml')
* Start the server with <code>./main.py</code> or <code>python main.py</code> (you might need to change the files permissions to execute)

**Attention:** There are currently problems if you are connected to the Wallaby via USB. We are working on that.

###Installation on testing devices with random output:
* Copy the MissionControl-Server directory anywhere you want it on your Linux or OS X device
* Run <code>python MC2ML/MC2ML\_Parser.py SpecialTesting.xml</code> 
* Start the server with <code>./main.py</code> or <code>python main.py</code> (you might need to change the files permissions to execute)