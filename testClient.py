#First Party Libraries
import sys
from sys import platform as _platform
import os
import socket
import json
import time

size = 2048

CONFIG = '{"ConnREQ" : {"HardwareType" : "Smartphone","SupportedCrypto" : ["AES128", "RSA512"],"PreferredCrypto" : "None","SupportedDT" : ["Bool", "String", "Integer", "Slider", "Button"]}}'

def get_host():
	if _platform == "linux" or _platform == "linux2":
		return os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1').read().strip();
	if _platform == "darwin":
		return os.popen('ifconfig en0 | grep "inet " | cut -d" " -f2 | cut -d" " -f1').read().strip();
	if _platform == "win32" or _platform == "win64":
		print("Platform not supported, using 'localhost' for host");


def multiReceive(client):
	finished = False;
	jsonMsg = None;
	msg = client.recv(size).decode("utf-8");

	if not msg:
		return False;
	while not finished:
		try:
			jsonMsg = json.loads(msg);

			finished = True;
		except ValueError:
			msg = msg+client.recv(size).decode("utf-8");

			if not msg:
				return False;
	return jsonMsg;

def testClient():


	host = get_host()
	port = 62626
	s = None
	crypto = None

	try: 
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.connect((host, port)) 
	except socket.error: 
		
		if s: 
		    s.close() 
		    print("Could not open socket: ", sys.exc_info()[1])
		    sys.exit(1)


	handshakeSucceeded = False
	s.send(CONFIG.encode())
	
	time.sleep(0.005)

	respStream = s.recv(size)

	if respStream:
		print(respStream.decode("utf8"))
		response = json.loads(respStream.decode('utf8'))
		
		if ("ConnACK" in response.keys()):
			print("ConnACK message")
			ack = response["ConnACK"]

			if ("ChosenCrypto" in ack.keys()):
				crypto = ack["ChosenCrypto"]
			else:
				print("Missing ChosenCrypto in ConnACK using default: none")

			time.sleep(0.005)
			respStream = multiReceive(s)

			if respStream:
				lao = respStream
				print("LAO Received")
				handshakeSucceeded = True

				s.send('{ "ConnSTT" : "" }'.encode('utf8'));
				print("ConnSTT sent")
				while True:
					data = s.recv(size).decode('utf8');
					print(data)
					try:
						json.loads(data)
						print("parseable")
					except:
						print("unparseable")
					time.sleep(0.005);
			else:
				print("No answer from server");

		elif ("ConnREJ" in response.keys()):
			rej = response["ConnREJ"]

			if ("Error" in rej.keys()):
				print(rej["Error"]);
			else:
				print("Missing Error in ConnREJ")

		else:
			print("No response from the server")

	else:
		print("No answer from the server")
		
	if (handshakeSucceeded):
		print("Handshake succeeded");
		print(host)
		print(port)
		print(size)
		print(crypto)

	s.close()

testClient()
