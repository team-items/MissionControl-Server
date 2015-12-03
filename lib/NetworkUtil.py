import json
import select;
import socket;
import sys
import hashlib
import base64
import struct

def multiReceive(client, SEGMENT_SIZE):
	finished = False;
	jsonMsg = None;
	msg = client.recv(SEGMENT_SIZE).decode("utf-8");

	if not msg:
		return False;
	while not finished:
		try:
			jsonMsg = json.loads(msg);

			finished = True;
		except ValueError:
			inputready, outputready, excepts = select.select([client], [], []);
			if len(inputready) == 1:
				msg1 = client.recv(SEGMENT_SIZE).decode("utf-8");
				msg = msg+msg1;

				if not msg:
					return False;
	return jsonMsg;

def create_handshake(handshake):
    handshakelines = handshake.split("\r\n")
    matching = [s for s in handshakelines if "Sec-WebSocket-Key: " in s]

    returning_handshake = "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "

    if(len(matching) > 0):
        returning_handshake+=base64.b64encode(hashlib.sha1((matching[0][19:]+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
        returning_handshake+="\r\n\r\n"
    return returning_handshake

def decode(data):
    frame = bytearray(data)

    length = frame[1] & 127

    indexFirstMask = 2
    if length == 126:
        indexFirstMask = 4
    elif length == 127:
        indexFirstMask = 10

    indexFirstDataByte = indexFirstMask + 4
    mask = frame[indexFirstMask:indexFirstDataByte]

    i = indexFirstDataByte
    j = 0
    decoded = []
    while i < len(frame):
        decoded.append(frame[i] ^ mask[j%4])
        i += 1
        j += 1

    return "".join(chr(byte) for byte in decoded)

def encode(data):
	"""
	Encode and send a WebSocket message
	"""
	message = bytes()

	b1 = b'\x81'

	payload = data.encode("UTF-8")
	
	# Append 'FIN' flag to the message
	message += b1

	b2 = 0
    
	length = len(payload)
	if length < 126:
		b2 |= length
		message += bytes([b2])
	
	elif length < (2 ** 16) - 1:
		b2 |= 126
		message += bytes([b2])
		l = struct.pack(">H", length)
		message += l
    
	else:
		b2 |= 127
		message += bytes([b2])
		l = struct.pack(">Q", length)
		message += l

	message += payload

	return message

def sendData(sock, data, fin=True, opcode=1, masking_key=False):
    if fin > 0x1:
        raise ValueError('FIN bit parameter must be 0 or 1')
    if 0x3 <= opcode <= 0x7 or 0xB <= opcode:
        raise ValueError('Opcode cannot be a reserved opcode')

    ## +-+-+-+-+-------++-+-------------+-------------------------------+
    ## |F|R|R|R| opcode||M| Payload len |    Extended payload length    |
    ## |I|S|S|S|  (4)  ||A|     (7)     |             (16/63)           |
    ## |N|V|V|V|       ||S|             |   (if payload len==126/127)   |
    ## | |1|2|3|       ||K|             |                               |
    ## +-+-+-+-+-------++-+-------------+ - - - - - - - - - - - - - - - +
    ## +-+-+-+-+--------------------------------------------------------+
    ## |     Extended payload length continued, if payload len == 127   |
    ## + - - - - - - - - - - - - - - - +--------------------------------+
    ## + - - - - - - - - - - - - - - - +-------------------------------+
    ## |                               |Masking-key, if MASK set to 1  |
    ## +-------------------------------+-------------------------------+
    ## | Masking-key (continued)       |          Payload Data         |
    ## +-------------------------------- - - - - - - - - - - - - - - - +
    ## :                     Payload Data continued ...                :
    ## + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
    ## |                     Payload Data continued ...                |
    ## +---------------------------------------------------------------+
 #   try:
    header = struct.pack('!B', ((fin << 7)
                                | (0 << 6)
                                | (0 << 5)
                                | (0 << 4)
                                | opcode))
    if masking_key:
        mask_bit = 1 << 7
    else:
        mask_bit = 0

    length = len(data)
    if length < 126:
        header += struct.pack('!B', (mask_bit | length))
    elif length < (1 << 16):
        header += struct.pack('!B', (mask_bit | 126)) + struct.pack('!H', length)
    elif length < (1 << 63):
        header += struct.pack('!B', (mask_bit | 127)) + struct.pack('!Q', length)

    body = data
    
    try:
        sock.send(bytes(header + body))
    except IOError, e:
        print('error writing - %s' % data)
#    except Exception, e:
#       	print(e)
#        print(e)