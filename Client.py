import sys
import select
import socket
import simplejson as json

from Connectable import Connectable
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer;
from Logger import Logger;

class Client(Connectable):
	controllable = True;
	midac = None;
	connectingId = None;
	conf = None
	LAO = None;

	def __init__(self, socket, size, address, port, connectingId, conf, LAO):
		self.socket = socket;
		self.messageSize = size;
		self.midac = MIDaCSerializer();
		self.address = address;
		self.port = port;
		self.connectingId = connectingId;
		self.conf = conf;
		self.LAO = LAO;

	def receiveAndDecode(self):
		return self.socket.recv(self.messageSize).decode("utf-8");

	def sendAndEncode(self, msg):
		self.socket.send(msg.encode());

	def performHandshake(self):
		if not self.established:
			if self.handshakeStatus == 0:
				inputMSG = self.receiveAndDecode();
				msg = json.loads(inputMSG);

				if self.midac.GetMessageType(msg) == MSGType.ConnREQ:
					self.handshakeStatus = 1;

			elif self.handshakeStatus == 1:
				self.sendAndEncode(self.midac.GenerateConnACK("None", self.conf.SEGMENT_SIZE));
				self.handshakeStatus = 2;

			elif self.handshakeStatus == 2:
				#Creating test MIDaC Conn LAO here

				self.sendAndEncode(json.dumps(self.LAO));
				self.handshakeStatus = 3;

			else:
				msg = json.loads(self.receiveAndDecode())
				if self.midac.GetMessageType(msg) == MSGType.ConnSTT:
					self.established = True;

		else:
			raise Exception("Handshake already performed");



