import sys
import select
import socket

import NetworkUtil as NU
from Client import Client 
from ConfigHandler import ConfigHandler
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer;

class ClientManager():
	clients = None;
	inputready = None;
	outputready = None;
	server = None;
	newConnectedId = 0;

	log = None;
	conf = None;
	LAO = None;

	def __init__(self, server, log, conf, LAO):
		self.clients = [];
		self.inputready = [];
		self.outputready = [];
		self.server = server;
		self.log = log;
		self.conf = conf;
		self.LAO = LAO;

	#Gets the socket descriptors of the clients, including an optional added socket descriptor
	def getClientsSockets(self, added):
		sockets = added;
		for client in self.clients:
			sockets.append(client.socket);
		return sockets;

	#get the stored client object that has the given socket descriptor 
	def getClientBySocket(self, socket):
		reqClient = None;
		for client in self.clients:
			if client.socket == socket:
				reqClient = client;

		return reqClient;

	def getHandshakeSockets(self):
		handshaking = [];
		for client in self.clients:
			if not client.established:
				handshaking.append(client);
		return handshaking;

	def update(self):
		self.inputready, self.outputready, excepts = select.select(self.getClientsSockets([self.server]), self.getClientsSockets([]), []);

	def handleConnect(self):
		client, address = self.server.accept();
		client.setblocking(0);

		self.clients.append(Client(client, self.conf.SEGMENT_SIZE, address[0], address[1], self.newConnectedId, self.conf, self.LAO));

		self.log.logAndPrintMessage("Client "+`self.newConnectedId`+" ("+address[0]+":"+`address[1]`+") connected");
		self.newConnectedId+=1;

	def handleHandshake(self):
		for client in self.getHandshakeSockets():
			if (client.socket in self.inputready and (client.handshakeStatus == 0 or client.handshakeStatus == 3 )) or (client.socket in self.outputready and (client.handshakeStatus == 1 or client.handshakeStatus == 2)):
				client.performHandshake();
				if client.established:
					self.log.logAndPrintSuccess("Handshake with Client "+`client.connectingId`+" successful!");
			if client.socket in self.inputready:
				self.inputready.remove(client.socket);
			if client.socket in self.outputready:
				self.outputready.remove(client.socket);

	def handleInput(self):
		control = None;
		for sock in self.inputready:
			if sock == self.server:
				self.handleConnect();
			else:
				try:
					data = NU.multiReceive(sock, self.conf.SEGMENT_SIZE);
					if data:
						#Only the longest lasting connected can send
						if self.clients.index(self.getClientBySocket(sock)) == 0:
							print(data);
							control = json.dumps(data);
					else:
						self.inputready.remove(sock);
						self.outputready.remove(sock);
						client = self.getClientBySocket(sock);
						self.log.logAndPrintWarning("Client "+`client.connectingId`+" ("+client.address+":"+`client.port`+") disconnected!");
						self.clients.remove(client);
				except socket.error:
					self.log.logAndPrintWarning("Socket Error");
		return control;


	def handleOutput(self, msg):
		for sock in self.outputready:
			sock.send(msg);




