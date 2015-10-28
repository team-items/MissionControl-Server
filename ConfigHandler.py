from Logger import Logger
import json

class ConfigHandler():
	CONFIGPATH = "config.conf";
	PORT = 62626;
	SAMPLERATE = 0.01;
	HOST = 'localhost';
	BACKLOG = 20;
	SEGMENT_SIZE = 2048;

	log = None;

	def __init__(self, path, log):
		self.log = log;

		if path != "":
			self.CONFIGPATH = path;
		else:
			self.log.logAndPrintWarning("No configpath, using default")
		config = json.loads(open(self.CONFIGPATH, 'r').read());
		
		if "Server" in config:
			config = config["Server"];
			if "Port" in config:
				self.PORT = config["Port"];
			else:
				self.log.logAndPrintWarning("No port in configfile, using default");
			
			if "Samplerate" in config:
				self.SAMPLERATE = config["Samplerate"];
			else:
				self.log.logAndPrintWarning("No samplerate in configfile, using default");

			if "Host" in config:
				self.HOST = config["Host"];
			else:
				self.log.logAndPrintWarning("No host in configfile, using default");

			if "Backlog" in config:
				self.BACKLOG = config["Backlog"];
			else:
				self.log.logAndPrintWarning("No backlog in configfile, using default");

			if "Segment_Size" in config:
				self.SEGMENT_SIZE = config["Segment_Size"];
			else:
				self.log.logAndPrintWarning("No segment size in configfile, using default");

		else:
			self.log.logAndPrintError("Invalid config file, using default values");

		self.log.logAndPrintMessage("Running config: \nCONFIGPATH "+self.CONFIGPATH+
			"\nPORT "+`self.PORT`+"\nSAMPLERATE "+`self.SAMPLERATE`+"\nHOST "+self.HOST+
			"\nBACKLOG "+`self.BACKLOG`+"\nSEGMENT_SIZE "+`self.SEGMENT_SIZE`)


