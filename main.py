#First Party Libraries
import json
import sys
import select
import socket
import base64
import time

#Own Libraries
import Debug

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

	clientStatusList = [];

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
					Debug.warning("Missing Port in Config File, using 62626");
				
				if("Samplerate" in serverkeys):
					self.SAMPLERATE = serversettings["Samplerate"];
				else:
					Debug.warning("Missing Samplerate in Config File, using 0.01s");
			else:
				Debug.error("Invalid Configfile.");
				Debug.warning("Using default values only.");
		except ValueError as e:
			Debug.error("Invalid Configfile.");
			Debug.warning("Using default values only.");
		
	def printStartupConfig(self):
		Debug.info("Config used: "+`self.CONFIGPATH`);
		Debug.info("Port used: "+`self.PORT`);
		Debug.info("Samplerate used: "+`self.SAMPLERATE`);


	def setUpServer(self):
		try:
			self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
			self.SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
			self.SERVER.bind((self.HOST, self.PORT));
			self.SERVER.listen(self.BACKLOG);
			Debug.success("Socket set up");
		except socket.error:
			if self.SERVER:
				self.SERVER.close();
			Debug.error("Could not open socket: "+sys.exc_info()[1]);
			sys.exit(1);

		self.INPUT = [self.SERVER];
		self.OUTPUT = [];

		Debug.success("Finished setting up Server");

	#Constructor
	def __init__(self):
		try:
			configfile = open(self.CONFIGPATH, 'r');
			self.setUpConfig(configfile.read());
		except IOError as e:
			Debug.error("No config file found.");
			Debug.warning("Proceeding with default values");

		self.printStartupConfig();
		Debug.info("Setting up server");
		self.setUpServer();



	#Running Functions

	def handleConnectReq(self):
		client, address = self.SERVER.accept();
		client.setblocking(0);
		self.INPUT.append(client);
		self.OUTPUT.append(client);
		self.clientStatusList.append(0);
		Debug.info("New Client connected");

	def requestOkay(self, msg):
		return True;

	def run(self):
		running = True;
		Debug.success("Server up and running");
		blocked = False;

		while running:
			inputready, outputready, exceptready = select.select(self.INPUT, self.OUTPUT, []);

			for sock in inputready:
				clientIndex = self.INPUT.index(sock)-1;
				if sock == self.SERVER:
					self.handleConnectReq();
				else:
					try:
						data = sock.recv(self.SIZE);
						if data:
							indat = data.decode("utf-8");
							if(indat[:1] == "{"):
								msg = json.loads(indat);
								if("ConnREQ" in msg and self.clientStatusList[clientIndex] == 0):
									if(self.requestOkay(msg)):
										self.clientStatusList[clientIndex] = 1;
										Debug.warning("Client "+`clientIndex`+": Handshake Request");
									else:
										self.clientStatusList[clientIndex] = -1;
										Debug.warning("Requesting Client ("+`clientIndex`+") does not fulfill requested standards");
								if("ConnSTT" in msg and self.clientStatusList[clientIndex] == 3):
									self.clientStatusList[clientIndex] = 4;
									Debug.warning("Client "+`clientIndex`+": Handshake succeeded")
								if("Control" in msg and self.clientStatusList[clientIndex] == 4):
									Debug.info("Received Control Command from "+`clientIndex`);

						else:
							sock.close();
							Debug.warning("Client "+`clientIndex`+": Connection closed");
							if sock in self.OUTPUT:
								self.OUTPUT.remove(sock);
							self.clientStatusList.pop(self.INPUT.index(sock)-1);
							self.INPUT.remove(sock);
							blocked = True;
					except(socket.error):
						Debug.error("Error while receiving data");

			if not blocked:
				for sock in outputready:
					if sock != self.SERVER:
						clientIndex = self.OUTPUT.index(sock);
						if(self.clientStatusList[clientIndex] == 1):
							sock.send('{ "ConnACK" : { "ChosenCrypto" : "None" } }'.encode());
							self.clientStatusList[clientIndex] = 2;
						elif(self.clientStatusList[clientIndex] == 2):
							sock.send('{ "ConnLAO" : {  "Information" : {   "SomeFloatNumber" : {    "DataType" : "Float",    "MinBound" : -1023.9999999,    "MaxBound" : 1023.9999999,    "Graph"  : 20   },   "SomeIntegerNumber" : {    "DataType" : "Integer",    "MinBound" : 0,    "MaxBound" : 1023   },   "SomeStatusString" : {    "DataType" : "String",    "MinLength" : 0,    "MaxLength" : 200   }   } }}'.encode())
							self.clientStatusList[clientIndex] = 3;
						elif(self.clientStatusList[clientIndex] == 4):
							sock.send('New Values!!');

			time.sleep(self.SAMPLERATE);
			blocked = False;


mc = MissionControl();
mc.run();
