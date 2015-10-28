import sys
import select
import socket

from Client import Client 
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer;

class ClientManager():
	clients = None;
	inputready = None;
	outputready = None;
	server = None;
	newConnectedId = 0;

	log = None;

	def __init__(self, server, log):
		self.clients = [];
		self.inputready = [];
		self.outputready = [];
		self.server = server;
		self.log = log;

	def getClientsSockets(self, added):
		sockets = added;
		for client in self.clients:
			sockets.append(client.socket);
		return sockets;

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

		self.clients.append(Client(client, 2048, address[0], address[1], self.newConnectedId));

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
		for sock in self.inputready:
			if sock == self.server:
				self.handleConnect();
			else:
				try:
					data = sock.recv(2048);
					if data:
						#add controlling function here
						print(data.decode("utf-8"));
					else:
						self.inputready.remove(sock);
						self.outputready.remove(sock);
						client = self.getClientBySocket(sock);
						self.log.logAndPrintWarning("Client "+`client.connectingId`+" ("+client.address+":"+`client.port`+") disconnected!");
						self.clients.remove(client);
				except socket.error:
					self.log.logAndPrintWarning("Socket Error");


	def handleOutput(self):
		for sock in self.outputready:
			sock.send("{'Data':{'Analog1':500, 'Analog2':510, 'Digital1': 'true', 'Digital2': 'false'}}");




