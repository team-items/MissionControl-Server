#First Party Libraries
import json

#Own Libraries
from mclib import *

#Third Party Libraries
from termcolor import colored

class MissionControl():
	CONFIGPATH = "config.conf";
	PORT = 62626;
	SAMPLERATE = 0.01;

	#Setup functions 
	def setUp(self, configs):
		try:
			settings = json.loads(configs);

			if("Server" in settings.keys()):
				serversettings = settings["Server"];
				serverkeys = serversettings.keys();

				if("Port" in serverkeys):
					self.PORT = serversettings["Port"];
				else:
					printWarning("Missing Port in Config File, using 62626");
				
				if("Samplerate" in serverkeys):
					self.SAMPLERATE = serversettings["Samplerate"];
				else:
					printWarning("Missing Samplerate in Config File, using 0.01s");
			else:
				printError("Invalid Configfile.");
				printWarning("Using default values only.");
		except ValueError as e:
			printError("Invalid Configfile.");
			printWarning("Using default values only.");
		

	#Constructor
	def __init__(self):
		try:
			configfile = open(self.CONFIGPATH, 'r');
			self.setUp(configfile.read());
		except IOError as e:
			printError("No config file found.");
			printWarning("Proceeding with default values");



	#Running Functions


MissionControl();