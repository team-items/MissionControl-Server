import json
import select;
import socket;

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