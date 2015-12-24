import sys
import select
import json
import socket

import NetworkUtil as NU
from Client import Client 
from ConfigHandler import ConfigHandler
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer 

#Class for managing all connected clients
class ClientManager():
	clients = None 
	inputready = None 
	outputready = None 
	server = None 
	newConnectedId = 0 

	log = None 
	conf = None 
	LAO = None 

	def __init__(self, server, log, conf, LAO):
		self.clients = [] 
		self.inputready = [] 
		self.outputready = [] 
		self.server = server 
		self.log = log 
		self.conf = conf 
		self.LAO = LAO 

	#Gets the socket descriptors of the clients, including an optional added socket descriptor
	def getClientsSockets(self, added):
		sockets = added 
		for client in self.clients:
			sockets.append(client.socket) 
		return sockets 

	#get the stored client object that has the given socket descriptor 
	def getClientBySocket(self, socket):
		reqClient = None 
		for client in self.clients:
			if client.socket == socket:
				reqClient = client 

		return reqClient 

	#get the handshaking clients
	def getHandshakeSockets(self):
		handshaking = [] 
		for client in self.clients:
			if not client.established:
				handshaking.append(client) 
		return handshaking 

	#performs select on all connected clients
	def update(self):
		self.inputready, self.outputready, excepts = select.select(self.getClientsSockets([self.server]), self.getClientsSockets([]), []) 

	#creates client object and adds it to client list. performed when client connected
	def handleConnect(self):
		client, address = self.server.accept() 
		client.setblocking(0) 

		self.clients.append(Client(client, self.conf.SEGMENT_SIZE, address[0], address[1], self.newConnectedId, self.conf, self.LAO, self.log)) 

		self.log.logAndPrintMessage("Client "+`self.newConnectedId`+" ("+address[0]+":"+`address[1]`+") connected") 
		self.newConnectedId+=1 

	#calls handshake handling function on every connected client that is in handshake mode
	def handleHandshake(self):
		for client in self.getHandshakeSockets():
			if (client.socket in self.inputready and (client.handshakeStatus == 0 or client.handshakeStatus == 3 )) or (client.socket in self.outputready and (client.handshakeStatus == 1 or client.handshakeStatus == 2)):
				try:
					client.performHandshake() 
					if client.established:
						self.log.logAndPrintSuccess("Handshake with Client "+`client.connectingId`+" successful!") 
				except:
					self.clients.remove(client)
					self.log.logAndPrintError("Unexpected exception occured during handshake!")
					self.log.logAndPrintWarning("Client "+`client.connectingId`+" ("+client.address+":"+`client.port`+") disconnected!") 
			if client.socket in self.inputready:
				self.inputready.remove(client.socket) 
			if client.socket in self.outputready:
				self.outputready.remove(client.socket) 

	#handles input from clients (also used for disconnect)	
	def handleInput(self):
		control = None 
		for sock in self.inputready:
			if sock == self.server:
				self.handleConnect() 
			else:
				try:
					client = self.getClientBySocket(sock) 
					if client.isWebsocket:
						data = client.receiveAndDecode() 
					else:
						data = NU.multiReceive(sock, self.conf.SEGMENT_SIZE) 
					if data:
						#Only the longest lasting connected can send
						if self.clients.index(self.getClientBySocket(sock)) == 0:
							try:
								control = json.dumps(data) 
							except:
								self.log.logAndPrintWarning("Unparseable client input") 
								return None
					else:
						if(sock in self.inputready):
							self.inputready.remove(sock) 
						if(sock in self.outputready):
							self.outputready.remove(sock) 
						client = self.getClientBySocket(sock) 
						self.log.logAndPrintWarning("Client "+`client.connectingId`+" ("+client.address+":"+`client.port`+") disconnected!") 
						self.clients.remove(client) 
				except socket.error:
					self.log.logAndPrintWarning("Socket Error") 
		return control 

	#sends output to connected clients
	def handleOutput(self, msg):
		for sock in self.outputready:
			try:
				client = self.getClientBySocket(sock) 

				#pad the message
				for i in range(len(msg.encode("utf8")), 2048):
					msg+=" "
				if client.isWebsocket:
					if not client.sendAndEncode(msg):
						self.clients.remove(client)
						self.log.logAndPrintWarning("Client "+`client.connectingId`+" ("+client.address+":"+`client.port`+") disconnected!") 
				else:
					sock.send(msg) 
			except socket.error:
				self.log.logAndPrintError("Broken pipe warning, if reocurring restart server") 




