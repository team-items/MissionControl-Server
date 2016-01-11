import sys
import select
import socket
import json

import NetworkUtil as NU
from Connectable import Connectable
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer 
from Logger import Logger 

#Class for storing client information and handle specific operations
class Client(Connectable):
	controllable = True 
	midac = None 
	connectingId = None 
	conf = None
	LAO = None 
	isWebsocket = False 
	log = None 

	def __init__(self, socket, size, address, port, connectingId, conf, LAO, log):
		self.socket = socket 
		self.messageSize = size 
		self.midac = MIDaCSerializer() 
		self.address = address 
		self.port = port 
		self.connectingId = connectingId 
		self.conf = conf 
		self.LAO = LAO 
		self.log = log 
		self.isWebsocket = False

	#receives message and performs
	def receiveAndDecode(self):
		try:
			if self.isWebsocket:
				decodedMsg = NU.decode(self.socket.recv(self.messageSize))
				if decodedMsg == None:
					self.log.logAndPrintError("Error decoding message, maybe wrong format?") 
				else:
					return decodedMsg 
			else:
				return self.socket.recv(self.messageSize).decode("utf-8") 
		except socket.error:
			self.log.logAndPrintError("Connection reset by peer, if reocurring restart server") 
			return False

	#performs utf-8 encoding on msg and sends it or uses the webscoket send function
	def sendAndEncode(self, msg):
		if self.isWebsocket:
			if not NU.sendData(self.socket, msg):
				return False
			else:
				return True
		else:
			self.socket.send(msg.encode("utf-8")) 

	#perform handshake
	def performHandshake(self):
		if not self.established:
			#receive connreq or perform websocket handshake if client is connecting over websockets
			if self.handshakeStatus == 0:
				inputMSG = self.receiveAndDecode() 
				if not inputMSG:
					self.socket.close()

				if inputMSG[:3] == "GET":
					handshake = NU.create_handshake(inputMSG)
					self.sendAndEncode(handshake)
					self.isWebsocket = True 
				else:
					try:
						msg = json.loads(inputMSG) 

						if self.midac.GetMessageType(msg) == MSGType.ConnREQ:
							self.handshakeStatus = 1 
					except ValueError:
						self.log.logAndPrintError("Error while parsing input") 

			#send connack to client
			elif self.handshakeStatus == 1:
				self.sendAndEncode(self.midac.GenerateConnACK("None", self.conf.SEGMENT_SIZE)) 
				self.handshakeStatus = 2 

			#send connlao to client
			elif self.handshakeStatus == 2:
				self.sendAndEncode(self.LAO) 
				self.handshakeStatus = 3 

			#receive connstt and set status to established
			else:
				inputMSG = self.receiveAndDecode() 
				if not inputMSG:
					self.socket.close() 
				try:
					msg = json.loads(inputMSG) 
					if self.midac.GetMessageType(msg) == MSGType.ConnSTT:
						self.established = True 
				except ValueError:
					self.established = False 

		else:
			raise Exception("Handshake already performed") 



