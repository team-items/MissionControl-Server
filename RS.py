import socket
import sys
import select
import json
from subprocess import Popen

from Connectable import Connectable
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer;
from Logger import Logger;

class RS(Connectable):
	rsalSock = None;
	rsalProcss = None;
	LAO = None;

	def __init__(self, conf, log):
		#dont forget to set self.socket
		self.messageSize = conf.SEGMENT_SIZE;
		self.conf = conf;
		self.midac = MIDaCSerializer();
		self.log = log;

	def handleInput(self):
		inp, out, exc = select.select([self.rsalSock],[self.rsalSock],[]);
		if len(inp) == 1:
			return inp[0].recv(self.conf.SEGMENT_SIZE).decode("utf-8");
		return None;

	def handleOutput(self, msg):
		print("handling output");
		inp, out, exc = select.select([self.rsalSock],[self.rsalSock],[]);
		if len(out) == 1:
			out[0].send(msg.encode())

	def connectRSAL(self, server):
		status = 0;
		outputs = []
		inputs = []

		inputs.append(server)

		self.rsalProcss = Popen(['./RSAL'])

		while status < 3:
			inputready, outputready, excepts = select.select(inputs, outputs, []);

			for socket in inputready:
				if socket == server and self.rsalSock == None:
					client, address = server.accept();
					client.setblocking(0);
					inputs.append(client);
					outputs.append(client);
					self.rsalSock = client;
				else:
					msg = socket.recv(self.conf.SEGMENT_SIZE).decode("utf-8");
					msg = json.loads(msg);

					if socket == self.rsalSock:
						if self.midac.GetMessageType(msg) == MSGType.ConnB and status == 0:
							status = 1;
						if self.midac.GetMessageType(msg) == MSGType.ConnLAO and status == 2:
							self.LAO = msg;
							status = 3;

			for socket in outputready:
				if socket == self.rsalSock and status == 1:
					socket.send(self.midac.GenerateConnACK_B().encode());
					status = 2;
