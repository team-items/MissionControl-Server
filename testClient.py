#First Party Libraries
import sys
import socket
import json
import time

#Own Libraries
from mclib import *

#Third Party Libraries
from termcolor import colored

CONFIG = '{"ConnREQ" : {"HardwareType" : "Smartphone","SupportedCrypto" : ["AES128", "RSA512"],"PreferredCrypto" : "None","SupportedDT" : ["Bool", "String", "Integer", "Slider", "Button"]}}'

def testClient():


	host = 'localhost'
	port = 62626
	size = 2048
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

	respStream = s.recv(2048)

	if respStream:
		print(respStream.decode("utf8"))
		response = json.loads(respStream.decode('utf8'))
		
		if ("ConnACK" in response.keys()):
			printSuccess("recieved Acknoledgement package")
			ack = response["ConnACK"]

			if ("ChosenCrypto" in ack.keys()):
				crypto = ack["ChosenCrypto"]
			else:
				printWarning("Missing ChosenCrypto in ConnACK using default: none")

			time.sleep(0.005)
			respStream = s.recv(2048)

			if respStream:
				print(respStream.decode("utf8"))
				lao = json.loads(respStream.decode('utf8'))

				#storage stuff goes here
				handshakeSucceeded = True
			else:
				printError("No answer from the server")

		elif ("ConnREJ" in response.keys()):
			rej = response["ConnREJ"]

			if ("Error" in rej.keys()):
				printError(rej["Error"])
			else:
				printWarning('Missing Error in ConnREJ')

		else:
			printError("no response from the server")

	else:
		printError("No answer from the server")
		
	if (handshakeSucceeded):
		printSuccess("Handshake succeeded; ready for transmissions")
		print(host)
		print(port)
		print(size)
		print(crypto)

	s.close()

testClient()
