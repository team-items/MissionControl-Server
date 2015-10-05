#First Party Libraries
import json
import sys
import select
import socket
import base64

#Own Libraries
from mclib import *

#Third Party Libraries
from termcolor import colored

class MissionControl():
	CONFIGPATH = "config.conf";
	PORT = 62626;
	SAMPLERATE = 0.01;

	HOST = 'localhost';
	BACKLOG = 10;
	SIZE = 2048;
	SERVER = None;

	INPUT = None; #list of inputs
	OUTPUT = None; #list of sockets ready for output

	#Setup functions 
	def setUpConfig(self, configs):
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
		
	def printStartupConfig(self):
		printInfo("Config used: "+`self.CONFIGPATH`);
		printInfo("Port used: "+`self.PORT`);
		printInfo("Samplerate used: "+`self.SAMPLERATE`);


	def setUpServer(self):
		try:
			self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
			self.SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
			self.SERVER.bind((self.HOST, self.PORT));
			self.SERVER.listen(self.BACKLOG);
			printSuccess("Socket set up");
		except socket.error:
			if self.SERVER:
				self.SERVER.close();
			printError("Could not open socket: "+sys.exc_info()[1]);
			sys.exit(1);

		self.INPUT = [self.SERVER];
		self.OUTPUT = [];

		printSuccess("Finished setting up Server");

	#Constructor
	def __init__(self):
		try:
			configfile = open(self.CONFIGPATH, 'r');
			self.setUpConfig(configfile.read());
		except IOError as e:
			printError("No config file found.");
			printWarning("Proceeding with default values");

		self.printStartupConfig();
		printInfo("Setting up server");
		self.setUpServer();



	#Running Functions

	def handleConnectReq():
		client, address = self.SERVER.accept();
		client.setblocking(0);
		self.INPUT.append(client);
		printInfo("New Client connected");

	def run(self):
		running = True;
		printSuccess("Server up and running");

		while running:
			inputready, outputready, exceptready = select.select(self.INPUT, self.OUTPUT, []);

			for sock in inputready:
				if sock == self.SERVER:
					handleConnectReq();
				else:
					data = sock.recv(self.SIZE);
					if data:
						print(data.decode("utf-8"))
					else:
						sock.close();
						printWarning("Connection closed");
						if sock in self.OUTPUT:
							output.remove(sock);
						self.INPUT.remove(sock);


mc = MissionControl();
mc.run();
