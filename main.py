#First Party Libraries
import json
import sys
import select
import socket
import base64
import time
import __future__
import Queue

#Own Libraries
from Logger import Logger

#Third Party Libraries

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

	DATA = Queue.Queue();
	log = Logger('logfile.log');

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
					self.log.printWarning("Missing Port in Config File, using 62626");
				
				if("Samplerate" in serverkeys):
					self.SAMPLERATE = serversettings["Samplerate"];
				else:
					self.log.printWarning("Missing Samplerate in Config File, using 0.01s");
			else:
				self.log.printError("Invalid Configfile.");
				self.log.printWarning("Using default values only.");
		except ValueError as e:
			self.log.printError("Invalid Configfile.");
			self.log.printWarning("Using default values only.");
		
	def printStartupConfig(self):
		self.log.printMessage("Config used: "+`self.CONFIGPATH`);
		self.log.printMessage("Port used: "+`self.PORT`);
		self.log.printMessage("Samplerate used: "+`self.SAMPLERATE`);


	def setUpServer(self):
		try:
			self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
			self.SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
			self.SERVER.bind((self.HOST, self.PORT));
			self.SERVER.listen(self.BACKLOG);
			self.log.printSuccess("Socket set up");
		except socket.error:
			if self.SERVER:
				self.SERVER.close();
			self.log.printError("Could not open socket: "+sys.exc_info()[1]);
			sys.exit(1);

		self.INPUT = [self.SERVER];
		self.OUTPUT = [];

		self.log.printSuccess("Finished setting up Server");

	#Constructor
	def __init__(self):
		try:
			configfile = open(self.CONFIGPATH, 'r');
			self.setUpConfig(configfile.read());
		except IOError as e:
			self.log.printError("No config file found.");
			self.log.printWarning("Proceeding with default values");

		self.printStartupConfig();
		self.log.printMessage("Setting up server");
		self.setUpServer();



	#Running Functions
	def getData(self):
		lastData = None;
		while(not self.DATA.empty()):
			lastData = self.DATA.get();

		return lastData;


	def handleConnectReq(self):
		client, address = self.SERVER.accept();
		client.setblocking(0);
		self.INPUT.append(client);
		self.OUTPUT.append(client);
		self.clientStatusList.append(0);
		self.log.printMessage("New Client connected");

	def requestOkay(self, msg):
		return True;

	def run(self):
		running = True;
		self.log.printSuccess("Server up and running");
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
										self.log.printWarning("Client "+`clientIndex`+": Handshake Request");
									else:
										self.clientStatusList[clientIndex] = -1;
										self.log.printWarning("Requesting Client ("+`clientIndex`+") does not fulfill requested standards");
								if("ConnSTT" in msg and self.clientStatusList[clientIndex] == 3):
									self.clientStatusList[clientIndex] = 4;
									self.log.printWarning("Client "+`clientIndex`+": Handshake succeeded")
								if("Control" in msg and self.clientStatusList[clientIndex] == 4):
									self.log.printMessage("Received Control Command from "+`clientIndex`);

						else:
							sock.close();
							self.log.printWarning("Client "+`clientIndex`+": Connection closed");
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
							returningData = self.getData();
							if(returningData == None):
								sock.send('No new data'.encode());
							else:
								sock.send(returningData.encode());


			time.sleep(self.SAMPLERATE);
			blocked = False;


mc = MissionControl();
mc.run();
