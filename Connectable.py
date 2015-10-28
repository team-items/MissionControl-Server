class Connectable():
	socket = None;
	handshakeStatus = 0;
	established = False;
	messageSize = None;

	def __init__(self, socket, size):
		self.socket = socket;
		self.messageSize = size;

