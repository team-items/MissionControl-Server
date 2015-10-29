import sys
import select
import socket
import json

from Connectable import Connectable
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer;
from Logger import Logger;

class Client(Connectable):
	controllable = True;
	midac = None;
	connectingId = None;
	conf = None

	def __init__(self, socket, size, address, port, connectingId, conf):
		self.socket = socket;
		self.messageSize = size;
		self.midac = MIDaCSerializer();
		self.address = address;
		self.port = port;
		self.connectingId = connectingId;
		self.conf = conf

	def receiveAndDecode(self):
		return self.socket.recv(self.messageSize).decode("utf-8");

	def sendAndEncode(self, msg):
		self.socket.send(msg.encode());

	def performHandshake(self):
		if not self.established:
			if self.handshakeStatus == 0:
				msg = json.loads(self.receiveAndDecode());

				if self.midac.GetMessageType(msg) == MSGType.ConnREQ:
					self.handshakeStatus = 1;

			elif self.handshakeStatus == 1:
				self.sendAndEncode(self.midac.GenerateConnACK("None", self.conf.SEGMENT_SIZE));
				self.handshakeStatus = 2;

			elif self.handshakeStatus == 2:
				#Creating test MIDaC Conn LAO here
				analog = self.midac.GenerateIntegerLAO("Analog1", 0, 1023, 30);
				analog.update(self.midac.GenerateIntegerLAO("Analog2", 0, 1023, 30));
				digital = self.midac.GenerateBoolLAO("Digital1");
				digital.update(self.midac.GenerateBoolLAO("Digital2"));
				motor = self.midac.GenerateSliderLAO("Motor1", 0, 1500);
				motor.update(self.midac.GenerateSliderLAO("Motor2", 0, 1500));
				servo = self.midac.GenerateSliderLAO("Servo1", 0, 2047);
				servo.update(self.midac.GenerateSliderLAO("Servo2", 0, 2047));
				motor.update(servo);

				LAO = self.midac.GenerateConnLAO(analog, None, digital, None, motor, None);

				self.sendAndEncode(LAO);
				self.handshakeStatus = 3;

			else:
				msg = json.loads(self.receiveAndDecode())
				if self.midac.GetMessageType(msg) == MSGType.ConnSTT:
					self.established = True;

		else:
			raise Exception("Handshake already performed");



