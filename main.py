import sys;
import select;
import socket;
import time;
from subprocess import Popen

#Own Libraries
from Logger import Logger
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer;
from ClientManager import ClientManager;
from ConfigHandler import ConfigHandler;
from RS import RS;

server = None;

print("MissionControl Server (MIDaC V1)\n");

log = Logger("eventlog.log");
conf = ConfigHandler("config.conf", log);

log.logAndPrintMessage("Setting up server");

try:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
	server.bind((conf.HOST, conf.PORT));
	server.listen(conf.BACKLOG);
except socket.error:
	if server:
		server.close();
	log.logAndPrintError("Could not open socket: "+`sys.exc_info()[1]`);
	sys.exit();

log.logAndPrintSuccess("Server running!");

rsal = RS(conf, log);
rsal.connectRSAL(server);
log.logAndPrintSuccess("RSAL Connected!");

clients = ClientManager(server, log, conf, rsal.LAO);
log.logAndPrintSuccess("Client Manager started!");

running = True;
while running:
	try:
		clients.update();
		clients.handleHandshake();

		data = rsal.handleInput();
		if data != None:
			clients.handleOutput(data);

		control = clients.handleInput();
		if control != None:
			rsal.handleOutput(control);
		time.sleep(conf.SAMPLERATE);
	except KeyboardInterrupt:
		server.close();
		log.logAndPrintWarning("Server manually stopped");
		sys.exit();
		rsal.rsalProcss.terminate();
