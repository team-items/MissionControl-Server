#First Party Libraries
import json

#Own Libraries
from mclib import *

#Third Party Libraries
from termcolor import colored

class MissionControl():
	CONFIGPATH = "config.conf";
	PORT = 62626;

	#Setup functions 
	def setUp(self, configs):
		settings = json.loads(configs);

		if("Server" in settings.keys()):
			if("Port" in settings["Server"].keys()):
				self.PORT = settings["Server"]["Port"];
			else:
				printWarning("Missing Port in Config File, using 62626");
		else:
			printWarning("Invalid Configfile. Using default values only.");
		
		

	#Constructor
	def __init__(self):
		try:
			configfile = open(self.CONFIGPATH, 'r');
			self.setUp(configfile.read());
		except:
			printError("No config file found.");
			printWarning("proceeding with default values");


	#Running Functions


MissionControl();