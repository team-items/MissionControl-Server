#include "parson.h"
#include "parson.c"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <kovan/kovan.h>

//int digital(int wat){ return 0; }
//int analog(int wat){ return 999; }
//void msleep(int time) {} 

JSON_Value *root_value;
JSON_Object *root_object;
JSON_Value *ctrl_root_value;
JSON_Object *input;
char *serialized_string = NULL;
int number;

char* getDigitalWrapped(int port){
	if(digital(port)){
		return "true";
	}
	return "false";
}

char* generateConnLAO(){
    JSON_Value *root_value_lao = json_value_init_object();
    JSON_Object *root_object_lao = json_value_get_object(root_value_lao);

    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 1.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 1.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 1.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 1.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 2.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 2.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 2.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 2.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 3.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 3.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 3.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 3.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 4.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 4.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 4.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 4.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 5.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 5.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 5.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 5.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 6.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 6.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 6.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 6.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 7.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 7.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 7.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 7.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 8.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 8.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 8.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 8.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 1.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 1.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 2.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 2.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 3.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 3.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 4.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 4.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 5.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 5.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 6.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 6.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 7.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 7.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 8.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 8.Graph", 20);


    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 1.Slider S1.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 1.Slider S1.MinBoud", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 1.Slider S1.MaxBound", 2047);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 2.Slider S2.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 2.Slider S2.MinBoud", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 2.Slider S2.MaxBound", 2047);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 3.Slider S3.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 3.Slider S3.MinBoud", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 3.Slider S3.MaxBound", 2047);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 4.Slider S4.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 4.Slider S4.MinBoud", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 4.Slider S4.MaxBound", 2047);


    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 1.Motor 1 Slider.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 1.Motor 1 Slider.MinBoud", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 1.Motor 1 Slider.MaxBound", 1500);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 1.Motor 1 Button.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 2.Motor 2 Slider.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 2.Motor 2 Slider.MinBoud", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 2.Motor 2 Slider.MaxBound", 1500);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 2.Motor 2 Button.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 3.Motor 3 Slider.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 3.Motor 3 Slider.MinBoud", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 3.Motor 3 Slider.MaxBound", 1500);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 3.Motor 3 Button.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 4.Motor 4 Slider.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 4.Motor 4 Slider.MinBoud", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 4.Motor 4 Slider.MaxBound", 1500);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 4.Motor 4 Button.ControlType", "Button");

    return json_serialize_to_string_pretty(root_value_lao);
}

char* generateDataMsg(){
	root_value = json_value_init_object();
	root_object = json_value_get_object(root_value);

	json_object_dotset_number(root_object, "Data.Analog 1", analog(0));
	json_object_dotset_number(root_object, "Data.Analog 2", analog(1));
	json_object_dotset_number(root_object, "Data.Analog 3", analog(2));
	json_object_dotset_number(root_object, "Data.Analog 4", analog(3));
	json_object_dotset_number(root_object, "Data.Analog 5", analog(4));
	json_object_dotset_number(root_object, "Data.Analog 6", analog(5));
	json_object_dotset_number(root_object, "Data.Analog 7", analog(6));
	json_object_dotset_number(root_object, "Data.Analog 8", analog(7));
    json_object_dotset_string(root_object, "Data.Digital 1", getDigitalWrapped(8));
    json_object_dotset_string(root_object, "Data.Digital 2", getDigitalWrapped(9));
    json_object_dotset_string(root_object, "Data.Digital 3", getDigitalWrapped(10));
    json_object_dotset_string(root_object, "Data.Digital 4", getDigitalWrapped(11));
    json_object_dotset_string(root_object, "Data.Digital 5", getDigitalWrapped(12));
    json_object_dotset_string(root_object, "Data.Digital 6", getDigitalWrapped(13));
    json_object_dotset_string(root_object, "Data.Digital 7", getDigitalWrapped(14));
    json_object_dotset_string(root_object, "Data.Digital 8", getDigitalWrapped(15));

	return json_serialize_to_string_pretty(root_value);
}

void control(char * msg){
	ctrl_root_value = json_parse_string(msg);

    input = json_value_get_object(ctrl_root_value);

    if(json_object_dotget_string(input, "Control.Motor 1-Button") != NULL){
    	puts("Motor 1-Button Clicked");
    }
    if(json_object_dotget_string(input, "Control.Motor 2-Button") != NULL){
    	puts("Motor 2-Button Clicked");
    }
    if(json_object_dotget_string(input, "Control.Motor 3-Button") != NULL){
    	puts("Motor 3-Button Clicked");
    }
    if(json_object_dotget_string(input, "Control.Motor 4-Button") != NULL){
    	puts("Motor 4-Button Clicked");
    }
    
    number = 0;
    if((number = (int)json_object_dotget_number(input, "Control.Motor 1")) != 0){
    	printf("Motor 1: %d\n", number);
    }
    if((number = (int)json_object_dotget_number(input, "Control.Motor 2")) != 0){
    	printf("Motor 2: %d\n", number);
    }
    if((number = (int)json_object_dotget_number(input, "Control.Motor 3")) != 0){
    	printf("Motor 3: %d\n", number);
    }
    if((number = (int)json_object_dotget_number(input, "Control.Motor 4")) != 0){
    	printf("Motor 4: %d\n", number);
    }
    if((number = (int)json_object_dotget_number(input, "Control.Servo 1")) != 0){
    	printf("Servo 1: %d\n", number);
    }
    if((number = (int)json_object_dotget_number(input, "Control.Servo 2")) != 0){
    	printf("Servo 2: %d\n", number);
    }
    if((number = (int)json_object_dotget_number(input, "Control.Servo 3")) != 0){
    	printf("Servo 3: %d\n", number);
    }
    if((number = (int)json_object_dotget_number(input, "Control.servo 4")) != 0){
    	printf("Servo 4: %d\n", number);
    }
}

int is_get(char * msg){
    ctrl_root_value = json_parse_string(msg);

    input = json_value_get_object(ctrl_root_value);

    if(json_object_dotget_string(input, "GET") != NULL){
        return 1;
    }
    return 0;
}
