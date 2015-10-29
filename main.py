import sys;
import select;
import socket;
import time;

#Own Libraries
from Logger import Logger
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer;
from ClientManager import ClientManager;
from ConfigHandler import ConfigHandler;

server = None;

print("MissionControl Server (MIDaC V2)\n");

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

clients = ClientManager(server, log, conf);

running = True;
while running:
	try:
		clients.update();
		clients.handleHandshake();
		clients.handleInput();
		clients.handleOutput();
		time.sleep(conf.SAMPLERATE);
	except KeyboardInterrupt:
		server.close();
		log.logAndPrintWarning("Server manually stopped");
		sys.exit();
