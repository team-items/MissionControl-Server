import sys
import xml.etree.ElementTree as ET

#direct use
flags = [] 
includes = []
variables = []
functions = []
dataFields = []
controlFields = []
getters = []
actions = []

integers = []
floats = []
bools = []
groups = []
sliders = []
buttons = []


result = ""

information_dotset_string_lao = 'json_object_dotset_string(root_object_lao, "ConnLAO.Information.'
information_dotset_number_lao = 'json_object_dotset_number(root_object_lao, "ConnLAO.Information.'

control_dotset_string_lao = 'json_object_dotset_string(root_object_lao, "ConnLAO.Controller.'
control_dotset_number_lao = 'json_object_dotset_number(root_object_lao, "ConnLAO.Controller.'

data_dotset_string = 'json_object_dotset_string(root_object, "Data.'
data_dotset_number = 'json_object_dotset_number(root_object, "Data.'

def printChilds(root):
	for child in root:
		print(child.tag)
		printChilds(child)

def grabLibraryElements(root):
	for library in root.findall("Libraries"):
		for child in library:
			if child.tag == "Flag":
				flags.append(child.text)
			if child.tag == "Include":
				includes.append("#include <"+child.text+">")

def grabMonitorElements(root):
	for monitor in root.findall("Monitor"):
		for Integers in monitor.findall("Integer"):
			for intVal in Integers.findall("IntegerValue"):
				integers.append(intVal)
		for Floats in monitor.findall("Float"):
			for floatVal in Floats.findall("FloatValue"):
				floats.append(floatVal)
		for Bools in monitor.findall("Bool"):
			for boolVal in Bools.findall("BoolValue"):
				bools.append(boolVal)

def grabSupportElements(root):
	for support in root.findall("Support"):
		for variable in support.findall("Variable"):
			variables.append(variable.text.strip())
		for function in support.findall("Function"):
			functions.append(function.text.strip().replace("\t", ""))

def grabControlElements(root):
	for control in root.findall("Control"):
		for group in control.findall("Group"):
			groups.append(group)
		for slider in control.findall("Slider"):
			sliders.append(slider)
		for button in control.findall("Button"):
			buttons.append(button)

def grabElements(path):
	tree = ET.parse(path)
	root = tree.getroot()

	grabLibraryElements(root)
	grabMonitorElements(root)
	grabSupportElements(root)
	grabControlElements(root)


def generateVariables():
	for slider in sliders:
		variables.append(createSliderVariableDefinition(slider))
	for group in groups:
		slider = group.find('Slider')
		variables.append(createSliderVariableDefinition(slider))

def getSliderName(slider):
	return slider.find('Name').text.replace(' ', '_')

def getSliderMinValue(slider):
	return slider.find('MinBound').text

def createSliderVariableDefinition(slider):
	return "int "+getSliderName(slider)+" = "+getSliderMinValue(slider)+";"


def generateNumberField(field, type):
	prefix = field.find('Name').text
	minbound = field.find('MinBound')
	maxbound = field.find('MaxBound')
	graph = field.find('Graph')

	if (type == "Float" or type == "Integer") and (minbound == None or maxbound == None):
		raise Exception("Min and maxbound required for Float and Integer")

	returnVal = information_dotset_string_lao+type+'.'+prefix+'.DataType", "'+type+'");' 
	if minbound != None:
		returnVal += '\n'+information_dotset_number_lao+type+'.'+prefix+'.MinBound", '+minbound.text+');'
	if maxbound != None:
		returnVal += '\n'+information_dotset_number_lao+type+'.'+prefix+'.MaxBound", '+maxbound.text+');'
	if graph != None:
		returnVal += '\n'+information_dotset_number_lao+type+'.'+prefix+'.Graph", '+graph.text+');'
	return returnVal

def generateIntegerField(integerField):
	return generateNumberField(integerField, 'Integer')

def generateFloatField(floatField):
	return generateNumberField(floatField, 'Float')

def generateBoolField(field):
	return generateNumberField(field, 'Bool')

def generateButtonControl(field, prefixAddition = ""):
	prefix = field.find('Name').text
	if prefixAddition != "":
		prefix = prefixAddition+"."+prefix
	descriptor = field.find('Descriptor')

	returnVal = control_dotset_string_lao+prefix+'.ControlType", "Button");'
	if descriptor != None:
		returnVal += '\n'+control_dotset_string_lao+prefix+'.Descriptor", "'+descriptor.text+'");'
	return returnVal

def generateSliderControl(field, prefixAddition = ""):
	prefix = field.find('Name').text
	if prefixAddition != "":
		prefix = prefixAddition+"."+prefix
	minbound = field.find('MinBound')
	maxbound = field.find('MaxBound')

	if (minbound == None or maxbound == None):
		raise Exception("Min and maxbound required for Slider")

	returnVal = control_dotset_string_lao+prefix+'.ControlType", "Slider");'
	returnVal += '\n'+control_dotset_number_lao+prefix+'.MinBound", '+minbound.text+');'
	returnVal += '\n'+control_dotset_number_lao+prefix+'.MaxBound", '+maxbound.text+');'
	return returnVal

def generateGetter(field, type):
	returnVal = ""
	if type == 'Float' or type == 'Integer':
		returnVal = data_dotset_number
	else:
		returnVal = data_dotset_string
	return returnVal+field.find('Name').text+'", '+field.find('Getter').text+');'

def button_dotget(name):
	return 'json_object_dotget_string(input, "Control.'+name+'")'

def slider_dotget(name):
	return 'json_object_dotget_number(input, "Control.'+name+'")'

def generateButtonAction(field):
	name = field.find('Name').text
	action = field.find('Action')

	result = "if(("+button_dotget(name)+") != NULL){"
	if action.text != None and action.text != None:
		result+="\n"+action.text.replace('\t', "")
	return result + "\n}"

def generateSliderAction(field):
	name = field.find('Name').text
	action = field.find('Action')

	result = "if(((int)"+slider_dotget(name)+") != 0){"
	result += "\n"+getSliderName(field)+" = (int)"+slider_dotget(name)+";"
	if action != None and action.text != None:
		result+="\n"+action.text.replace('\t', "")
	return result + "\n}"


def grabDataFields():
	for integerField in integers:
		dataFields.append(generateIntegerField(integerField))
	for floatField in floats:
		dataFields.append(generateFloatField(floatField))
	for boolField in bools:
		dataFields.append(generateBoolField(boolField))

def grabControlFields():
	for button in buttons:
		controlFields.append(generateButtonControl(button))
	for group in groups:
		button = group.find('Button')
		controlFields.append(generateButtonControl(button, group.find('Name').text))
	for slider in sliders:
		controlFields.append(generateSliderControl(slider))
	for group in groups:
		slider = group.find('Slider')
		controlFields.append(generateSliderControl(slider, group.find('Name').text))

def grabGetters():
	for field in integers:
		getters.append(generateGetter(field, 'Integer'))
	for field in floats:
		getters.append(generateGetter(field, 'Float'))
	for field in bools:
		getters.append(generateGetter(field, 'Bool'))

def grabActions():
	for slider in sliders:
		actions.append(generateSliderAction(slider))
	for group in groups:
		actions.append(generateSliderAction(group.find('Slider')))
	for button in buttons:
		actions.append(generateButtonAction(button))
	for group in groups:
		actions.append(generateButtonAction(group.find('Button')))

def generateString(arr):
	result = ""
	for str in arr:
		result+=str+"\n"
	return result

def generateCompileLine():
	result = "gcc -o RSAL/RSAL RSAL/RSAL.c"
	for flag in flags:
		result += " "+flag
	return result

########################

if len(sys.argv) > 1:
	grabElements(sys.argv[1])
	generateVariables()
	grabDataFields()
	grabControlFields()
	grabGetters()
	grabActions()

	with open('ControllerTemplate', 'r') as template:
	    templateString=template.read()

	templateString = templateString.replace('<CustomIncludes>', generateString(includes))
	templateString = templateString.replace('<Variables>', generateString(variables))
	templateString = templateString.replace('<Functions>', generateString(functions))
	templateString = templateString.replace('<DataFields>', generateString(dataFields))
	templateString = templateString.replace('<ControlFields>', generateString(controlFields))
	templateString = templateString.replace('<Getters>', generateString(getters))
	templateString = templateString.replace('<Actions>', generateString(actions))

	result = open('CONTROLLER.c','w')
	result.write(templateString)
	result.close()

	print(generateCompileLine())



