from Connectable import Connectable

class RS(Connectable):
	

	def __init__(self, socket, size):
		self.socket = socket;
		self.messageSize = size;


