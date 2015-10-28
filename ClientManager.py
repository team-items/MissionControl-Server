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

		clients.append(Client(client, 2048));

		self.log.logAndPrintMessage("New client ("+address+") connected")

	def handleHandshake(self):
		for client in self.getHandshakeSockets():
			if client.socket in self.inputready and client.socket in self.outputready:
				client.performHandshake();
				self.inputready.remove(client.socket);
				self.outputready.remove(client.socket);

	def handleInput(self):
		for sock in self.inputready:
			if sock == self.server:
				self.handleConnect();
			else:
				data = sock.recv(2048);
				if data:
					print(data.decode("utf-8"));
				else:
					self.inputready.remove(sock);
					self.outputready.remove(sock);
					self.clients.remove(self.getClientBySocket(sock));


	def handleOutput(self):
		for sock in self.outputready:
			sock.send("asdf");




