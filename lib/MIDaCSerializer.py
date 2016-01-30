import json

#ENUM style class for easier comparison
class MSGType():
	ConnREQ = 1 
	ConnACK = 2 
	ConnREJ = 3 
	ConnLAO = 4 
	ConnSTT = 5 
	ConnB   = 6 

#exception thrown when a message is not midac serializeable 
class MIDaCSerializationException(Exception):
	def __init__(self, value):
		self.value = value 
	def __str__(self):
		return "MIDaC Serialization Exception for "+repr(self.value) 

#Class used to create, compare and serialze midac messages
class MIDaCSerializer():

	def GetMessageType(self, msg):
		if type(msg) is str:
			json.loads(msg) 
		if type(msg) is dict:
			if "ConnLAO" in msg:
				return MSGType.ConnLAO 
			if "ConnACK" in msg:
				return MSGType.ConnACK 
			if "ConnREQ" in msg:
				return MSGType.ConnREQ 
			if "ConnREJ" in msg:
				return MSGType.ConnREJ 
			if "ConnSTT" in msg:
				return MSGType.ConnSTT 
			if "B-Connect" in msg:
				return MSGType.ConnB 
		else:
			raise MIDaCSerializationException(msg) 

	def GenerateConnACK(self, crypto, size):
		ConnACK = '{"ConnACK" : {"ChosenCrypto" : crypto, "SegmentSize" : size}}\n'
		return ConnACK

	def GenerateConnACK_B(self):
		ConnACK = { "ConnACK" : ""} 
		return json.dumps(ConnACK) 

	def GenerateConnLAO(self, integers, floats, bools, strings, sliders, buttons):
		ConnLAO = {"ConnLAO" : {
				"Information" : {
					"Integer" : integers,
					"Float" : floats,
					"Bool" : bools,
					"String" : strings
				},
				"Control" : {
					"Slider" : sliders,
					"Button" : buttons
				}
			}
		}

		return json.dumps(ConnLAO) 

	def GenerateConnREJ(self, message):
		ConnREJ = {"ConnREJ" : {"Error" : message}}

	def GenerateIntegerLAO(self, name, minbound, maxbound, graph):
		if graph is None:
			IntLAO = {name : {
					"DataType" : "Integer",
					"MinBound" : minbound,
					"MaxBound" : maxbound,
				}
			}
			return IntLAO 
		else:
			IntLAO = {name : {
					"DataType" : "Integer",
					"MinBound" : minbound,
					"MaxBound" : maxbound,
					"Graph" : graph
				}
			}
			return IntLAO 

	def GenerateFloatLAO(self, name, minbound, maxbound, graph):
		if graph is None:
			FloatLAO = {name : {
					"DataType" : "Float",
					"MinBound" : minbound,
					"MaxBound" : maxbound,
				}
			}
			return FloatLAO
		else:
			FloatLAO = {name : {
					"DataType" : "Float",
					"MinBound" : minbound,
					"MaxBound" : maxbound,
					"Graph" : graph
				}
			}
			return FloatLAO

	def GenerateStringLAO(self, name, minlength, maxlength):
		StringLAO = {name : {
				"DataType" : "String",
				"MinLength" : minlength,
				"MaxBound" : maxlength,
			}
		}
		return StringLAO

	def GenerateBoolLAO(self, name):
		BoolLAO = {name : {
				"DataType" : "Bool"
			}
		}
		return BoolLAO 

	def GenerateSliderLAO(self, name, maxbound, minbound):
		SliderLAO = {name : {
				"ControlType" : "Slider",
				"MinBound" : minbound,
				"MaxBound" : maxbound
			}
		}
		return SliderLAO 

	def GenerateButtonLAO(self, name):
		ButtonLAO = {name : {
				"ControlType" : "Button"
			}
		}
		return ButtonLAO

