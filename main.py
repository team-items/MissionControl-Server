#!/usr/bin/env python

import sys;
import socket;
import time;

#Own Libraries
from lib import *

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

rsal = RS(conf, log)
rsal.connect()

log.logAndPrintSuccess("RSAL Connected!");

log.logAndPrintSuccess("Server running!");

clients = ClientManager(server, log, conf, rsal.LAO);
log.logAndPrintSuccess("Client Manager started!");

running = True;
while running:
	try:
		clients.update();
		clients.handleHandshake();
		
		control = clients.handleInput();
		if control != None:
			rsal.handleOutput(control);

		data = rsal.handleInput();
		if data != None:
			clients.handleOutput(data);

		time.sleep(conf.SAMPLERATE);
	except KeyboardInterrupt:
		server.close();
		log.logAndPrintWarning("Server manually stopped");
		sys.exit();
		rsal.rsalProcss.terminate();
	except:
		server.close() 
		rsal.rsalProcss.terminate() 
		log.logAndPrintError("Unexpected Exception. Server stopped") 
		sys.exit() 

