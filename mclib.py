from termcolor import colored;

def coloredPrint(text, color):
	if(color == 'grey' or color == 'red' or color == 'green' or color == 'yellow' or color == 'blue' or color == 'magenta' or color == 'cyan' or color == 'white'):
		print(colored(text, color));
	elif(color == 'black'):
		print(text);
	else:
		raise UserWarning('Given color not supported');

def printWarning(text):
	print(colored("[Warning] "+text, 'yellow'));

def printError(text):
	print(colored("[Error] "+text, 'red'));

def printSuccess(text):
	print(colored("[Success] "+text, 'green'));