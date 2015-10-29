import time;

class Logger():
	logfile_location = None;

	OK = '\033[32m' #Success Green
	WARNING = '\033[33m' #Warning Yellow
	ERROR = '\033[31m' #Fail Red
	MESSAGE = '\033[7m' #Message Bold
	ENDC = '\033[0m'

	def __init__(self, logfile_location):
		self.logfile_location = logfile_location;
		self.clearLogfile();

	def logWithTime(self, text):
		with open(self.logfile_location, "a") as logfile:
			logfile.write(time.strftime("%x %H:%M:%S") + " " + text+"\n");

	def log(self, text):
		with open(self.logfile_location, "a") as logfile:
			logfile.write(text+"\n");

	def printWithTime(self, text):
		print(time.strftime("%x %H:%M:%S") + " " + text);

	def logWarning(self, text):
		text = "[Warning] "+text;
		self.logWithTime(text);

	def logError(self, text):
		text = "[Error]   "+text;
		self.logWithTime(text);

	def logSuccess(self, text):
		text = "[Success] "+text;
		self.logWithTime(text);

	def logMessage(self, text):
		text = "[Message] "+text;
		self.logWithTime(text);

	def printWarning(self, text):
		text = self.WARNING+"[Warning]"+self.ENDC+" "+text;
		self.printWithTime(text);

	def printError(self, text):
		text = self.ERROR+"[Error]"+self.ENDC+"   "+text;
		self.printWithTime(text);

	def printSuccess(self, text):
		text = self.OK+"[Success]"+self.ENDC+" "+text;
		self.printWithTime(text);

	def printMessage(self, text):
		text = self.MESSAGE+"[Message]"+self.ENDC+" "+text;
		self.printWithTime(text);

	def logAndPrintWarning(self, text):
		self.logWarning(text);
		self.printWarning(text);

	def logAndPrintError(self, text):
		self.logError(text);
		self.printError(text);

	def logAndPrintSuccess(self, text):
		self.logSuccess(text);
		self.printSuccess(text);

	def logAndPrintMessage(self, text):
		self.logMessage(text);
		self.printMessage(text);

	def clearLogfile(self):
		self.printWarning("Clearing logfile");
		open(self.logfile_location, 'w').close();
