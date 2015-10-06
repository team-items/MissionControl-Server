from termcolor import colored;

def coloredPrint(text, color):
	if(color in ['grey','red','green','yellow','blue','magenta','cyan','white']):
		print(colored(text, color));
	elif(color == 'black'):
		print(text);
	else:
		raise UserWarning('Given color not supported');

def warning(text):
	print(colored("[Warning] "+text, 'yellow'));

def error(text):
	print(colored("[Error] "+text, 'red'));

def success(text):
	print(colored("[Success] "+text, 'green'));

def info(text):
	print(colored("[Info] "+text, 'grey'))