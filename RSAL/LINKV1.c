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

int servoPos1 = 0;
int servoPos2 = 0;
int servoPos3 = 0;
int servoPos4 = 0;

int motorSpeed1 = 0;
int motorSpeed2 = 0;
int motorSpeed3 = 0;
int motorSpeed4 = 0;

int motorStat1 = 0;
int motorStat2 = 0;
int motorStat3 = 0;
int motorStat4 = 0;

void init(){
    enable_servos();

}

char* getDigitalWrapped(int port){
	if(digital(port)){
		return "true";
	}
	return "false";
}

char* generateConnLAO(){
    JSON_Value *root_value_lao = json_value_init_object();
    JSON_Object *root_object_lao = json_value_get_object(root_value_lao);

    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Integer.Analog 0.DataType", "Integer");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 0.MinBound", 0);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 0.MaxBound", 1023);
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Integer.Analog 0.Graph", 20);
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
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 8.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 8.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 9.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 9.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 10.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 10.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 11.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 11.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 12.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 12.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 13.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 13.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 14.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 14.Graph", 20);
    json_object_dotset_string(root_object_lao, "ConnLAO.Information.Bool.Digital 15.DataType", "Bool");
    json_object_dotset_number(root_object_lao, "ConnLAO.Information.Bool.Digital 15.Graph", 20);


    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 0.Slider S1.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 0.Slider S1.MinBound", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 0.Slider S1.MaxBound", 2047);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 0.Button S1.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 1.Slider S2.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 1.Slider S2.MinBound", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 1.Slider S2.MaxBound", 2047);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 1.Button S2.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 2.Slider S3.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 2.Slider S3.MinBound", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 2.Slider S3.MaxBound", 2047);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 2.Button S3.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 3.Slider S4.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 3.Slider S4.MinBound", 1);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Servo 3.Slider S4.MaxBound", 2047);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Servo 3.Button S4.ControlType", "Button");


    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 0.Motor 1 Slider.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 0.Motor 1 Slider.MinBound", -1000);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 0.Motor 1 Slider.MaxBound", 1000);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 0.Motor 1 Button.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 1.Motor 2 Slider.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 1.Motor 2 Slider.MinBound", -1000);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 1.Motor 2 Slider.MaxBound", 1000);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 1.Motor 2 Button.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 2.Motor 3 Slider.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 2.Motor 3 Slider.MinBound", -1000);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 2.Motor 3 Slider.MaxBound", 1000);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 2.Motor 3 Button.ControlType", "Button");
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 3.Motor 4 Slider.ControlType", "Slider");
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 3.Motor 4 Slider.MinBound", -1000);
    json_object_dotset_number(root_object_lao, "ConnLAO.Controller.Motor 3.Motor 4 Slider.MaxBound", 1000);
    json_object_dotset_string(root_object_lao, "ConnLAO.Controller.Motor 3.Motor 4 Button.ControlType", "Button");

    return json_serialize_to_string_pretty(root_value_lao);
}

char* generateDataMsg(){
	root_value = json_value_init_object();
	root_object = json_value_get_object(root_value);

	json_object_dotset_number(root_object, "Data.Analog 0", analog(0));
	json_object_dotset_number(root_object, "Data.Analog 1", analog(1));
	json_object_dotset_number(root_object, "Data.Analog 2", analog(2));
	json_object_dotset_number(root_object, "Data.Analog 3", analog(3));
	json_object_dotset_number(root_object, "Data.Analog 4", analog(4));
	json_object_dotset_number(root_object, "Data.Analog 5", analog(5));
	json_object_dotset_number(root_object, "Data.Analog 6", analog(6));
	json_object_dotset_number(root_object, "Data.Analog 7", analog(7));
    json_object_dotset_string(root_object, "Data.Digital 8", getDigitalWrapped(8));
    json_object_dotset_string(root_object, "Data.Digital 9", getDigitalWrapped(9));
    json_object_dotset_string(root_object, "Data.Digital 10", getDigitalWrapped(10));
    json_object_dotset_string(root_object, "Data.Digital 11", getDigitalWrapped(11));
    json_object_dotset_string(root_object, "Data.Digital 12", getDigitalWrapped(12));
    json_object_dotset_string(root_object, "Data.Digital 13", getDigitalWrapped(13));
    json_object_dotset_string(root_object, "Data.Digital 14", getDigitalWrapped(14));
    json_object_dotset_string(root_object, "Data.Digital 15", getDigitalWrapped(15));

	return json_serialize_to_string_pretty(root_value);
}

void control(char* msg){
	ctrl_root_value = json_parse_string(msg);


    input = json_value_get_object(ctrl_root_value);
    if(json_object_dotget_string(input, "Control.Motor 1 Button") != NULL){
        if(motorStat1 == 0){
            motorStat1 = 1;
            mav(0, motorSpeed1);
        } else {
            motorStat1 = 0;
        }
    }
    if(json_object_dotget_string(input, "Control.Motor 2 Button") != NULL){
        if(motorStat2 == 0){
            motorStat2 = 1;
            mav(1, motorSpeed2);
        } else {
            motorStat2 = 0;
        }
    }
    if(json_object_dotget_string(input, "Control.Motor 3 Button") != NULL){
        if(motorStat3 == 0){
            motorStat3 = 1;
            mav(2, motorSpeed3);
        } else {
            motorStat3 = 0;
        }
    }
    if(json_object_dotget_string(input, "Control.Motor 4 Button") != NULL){
        if(motorStat4 == 0){
            motorStat4 = 1;
            mav(3, motorSpeed4);
        } else {
            motorStat4 = 0;
        }
    }

    if(json_object_dotget_string(input, "Control.Button S1") != NULL){
        set_servo_position(0, servoPos1);
    }
    if(json_object_dotget_string(input, "Control.Button S2") != NULL){
        set_servo_position(1, servoPos2);
    }
    if(json_object_dotget_string(input, "Control.Button S3") != NULL){
        set_servo_position(2, servoPos3);
    }
    if(json_object_dotget_string(input, "Control.Button S4") != NULL){
        set_servo_position(3, servoPos4);
    }
    
    number = 0;
    if((number = (int)json_object_dotget_number(input, "Control.Motor 1 Slider")) != 0){
        motorSpeed1 = number;
        if(motorStat1 == 1){
            mav(0, motorSpeed1);
        }
    }
    if((number = (int)json_object_dotget_number(input, "Control.Motor 2 Slider")) != 0){
        motorSpeed2 = number;
        if(motorStat2 == 1){
            mav(1, motorSpeed2);
        }
    }
    if((number = (int)json_object_dotget_number(input, "Control.Motor 3 Slider")) != 0){
        motorSpeed3 = number;
        if(motorStat3 == 1){
            mav(2, motorSpeed3);
        }
    }
    if((number = (int)json_object_dotget_number(input, "Control.Motor 4 Slider")) != 0){
        motorSpeed4 = number;
        if(motorStat4 == 1){
            mav(3, motorSpeed4);
        }
    }
    if((number = (int)json_object_dotget_number(input, "Control.Slider S1")) != 0){
        servoPos1 = number;
    }
    if((number = (int)json_object_dotget_number(input, "Control.Slider S2")) != 0){
        servoPos2 = number;
    }
    if((number = (int)json_object_dotget_number(input, "Control.Slider S3")) != 0){
        servoPos3 = number;
    }
    if((number = (int)json_object_dotget_number(input, "Control.Slider S4")) != 0){
        servoPos4 = number;
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
