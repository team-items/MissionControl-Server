import socket
import sys
import os
import json
from subprocess import Popen

from Connectable import Connectable
from MIDaCSerializer import MSGType, MIDaCSerializationException, MIDaCSerializer
from Logger import Logger
from ConfigHandler import ConfigHandler

#class used to start, connect and manage the rsal
class RS():
    server_address = 'uds_socket'
    connection = None 
    sock = None 
    LAO = None 

    #initializes rs object, creates uds socket used for connection
    def __init__(self, conf, log):
        self.messageSize = conf.SEGMENT_SIZE
        self.conf = conf
        self.midac = MIDaCSerializer()
        self.log = log
        # Make sure the socket does not already exist
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise

        # Create a UDS socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.sock.bind(self.server_address)

        # Listen for incoming connections
        self.sock.listen(1)

    #receives and stitches multiple messages until they are midac parseable
    def multiReceive(self):
        finished = False
        jsonMsg = None

        counter = 0
        msg = self.connection.recv(2048).decode("utf-8")
        msg = msg.strip(' ')
        if not msg:
            return False
        while not finished:
            try:
                counter += 1
                jsonMsg = json.loads(msg)
                finished = True
            except ValueError:
                if counter > 10:
                    return False
                msg1 = self.connection.recv(2048).decode("utf-8")
                msg = msg+msg1

                if not msg1:
                    return False
        return msg

    #handles input from rsal
    def handleInput(self):
        return self.multiReceive().encode("utf-8")

    #handles output to rsal
    def handleOutput(self, msg):
        self.connection.send(msg.encode())

    #launches and connects rsal
    def connect(self):
        self.rsalProcss = Popen(['./RSAL/RSAL'])
        # Wait for a connection
        self.connection, client_address = self.sock.accept()

        data = self.multiReceive()#Connect-B
        #if self.midac.GetMessageType(data) == MSGType.ConnB:

        self.connection.sendall(self.midac.GenerateConnACK_B().encode())#ConnACK
        data = self.multiReceive()#ConnLAO
        self.LAO = data.encode("utf-8")

    #requests new data from rsal
    def request(self):
        self.connection.send('{ "GET" : "" }'.encode())

