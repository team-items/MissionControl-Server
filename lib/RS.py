import json
from subprocess import Popen
import socket
import sys
import os

import NetworkUtil as NU
from Connectable import Connectable
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer;
from Logger import Logger;

server_address = 'echo_socket'

class RS(Connectable):
	rsalSock = None;
	rsalProcss = None;
	LAO = None;
	rsal = None;

	def __init__(self, conf, log):
		self.messageSize = conf.SEGMENT_SIZE;
		self.conf = conf;
		self.midac = MIDaCSerializer();
		self.log = log;

		# Make sure the socket does not already exist
		try:
		    os.unlink(server_address)
		except OSError:
		    if os.path.exists(server_address):
		        raise

		# Create a UDS socket
		self.rsalSock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.rsalSock.bind(server_address)


	def handleInput(self):
		return self.multiReceive(self.rsal);

	def handleOutput(self, msg):
		self.rsal.sendall(msg.encode());

	def multiReceive(self, connection):
		finished = False;
		jsonMsg = None;

		counter = 0;
		msg = connection.recv(self.conf.SEGMENT_SIZE).decode("utf-8");
		msg = msg.strip(' ')
		if not msg:
			return False;
		while not finished:
			try:
				counter += 1;
				jsonMsg = json.loads(msg);
				finished = True;
			except ValueError:
				if counter > 10:
					return False;
				msg1 = connection.recv(self.conf.SEGMENT_SIZE).decode("utf-8");
				msg = msg+msg1;

				if not msg1:
					return False;
		return jsonMsg;

	def connectRSAL(self):
		status = 0;
		self.rsalSock.listen(1)

		self.rsalProcss = Popen(['./RSAL/RSAL'])

		connection, client_address = self.rsalSock.accept()


		msg = self.multiReceive(connection);
		if self.midac.GetMessageType(msg) == MSGType.ConnB and status == 0:
			status = 1;

		if status == 1:
			connection.sendall(self.midac.GenerateConnACK_B().encode());
			status = 2;

		msg = self.multiReceive(connection);
		if self.midac.GetMessageType(msg) == MSGType.ConnLAO and status == 2:
			self.LAO = msg;
			status = 3;
		self.rsal = connection;
