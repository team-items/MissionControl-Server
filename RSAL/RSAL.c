/*
MIDaC KIPR Link ROSL (Robotic System Abstraction Layer)
Version 0.1
*/

#define true 1
#define false 0

#include <stdio.h>
#include <unistd.h>
#include <string.h> /* for strncpy */

#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include "LINKV1.c"

#define SOCK_PATH "echo_socket"
#define MSG_LENGTH 2048

void splitAndSend(char* msg);
void sendMessage(char* message);
char* recvMessage();

int s, t, len, i, leng;
struct sockaddr_un remote;
char str[MSG_LENGTH],splitbuff[MSG_LENGTH], buff[2049];


char *StringPadRight(char *string, int padded_len, char *pad) {
    leng = (int) strlen(string);
    if (leng >= padded_len) {
        return string;
    }
    int i;
    for (i = 0; i < padded_len - leng; i++) {
        strcat(string, pad);
    }
    return string;
}

void splitAndSend(char* msg){
    for(i=0; i<strlen(msg); i+=2047){
        memcpy( splitbuff, &msg[i], 2047 );
        splitbuff[2047] = '\0';
        sendMessage(splitbuff);
    }
}


void sendMessage(char* message){
    if(strlen(message) <= 2048){
        memcpy( buff, &message[0], 2048 );
        message = StringPadRight(buff, 2048, " ");
        message[2048] = '\0';      
    } else {
        splitAndSend(message);
    }

    if (send(s, buff, strlen(buff), 0) == -1) {
        //printf("RSAL_PROC_MESSAGE: Sending failed\n");  
    }  else {
        //printf("sendsuccess\n");
    }
    //msleep(50);
}

char* recvMessage(){
    if( recv(s, str, MSG_LENGTH, 0) < 0)
    {
        printf("RSAL_PROC_MESSAGE: Receiving failed\n");
        return "Failed";
    } 

    return str;
}

int main(void)
{

    if ((s = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
        perror("socket");
        exit(1);
    }

    printf("RSAL_PROC_MESSAGE: Trying to connect...\n");

    remote.sun_family = AF_UNIX;
    strcpy(remote.sun_path, SOCK_PATH);
    len = strlen(remote.sun_path) + sizeof(remote.sun_family) +1;
    if (connect(s, (struct sockaddr *)&remote, len) == -1) {
        //perror("connect");
        exit(1);
    }

    int status = 0;
    while(status < 3){
        if(status == 0){
            sendMessage("{ \"B-Connect\" : \"\" }");
            status = 1;
            printf("RSAL_PROC_MESSAGE: Sent B-Connect Message\n");
        } else if (status == 1){
            recvMessage();
            status = 2;
            printf("RSAL_PROC_MESSAGE: Received Conn-Ack\n");
        } else if (status == 2){
           /*Send the connLao*/
            sendMessage(generateConnLAO());
            status = 3;
            printf("RSAL_PROC_MESSAGE: Sent ConnLAO Message\n");
        }   
    }
    printf("RSAL_PROC_MESSAGE: Connected\n");

    
    for(;;){

        char* msg = generateDataMsg();
        sendMessage(msg);
    }
        //if ((t=recv(s, str, MSG_LENGTH, 0)) > 0) {
        //    str[t] = '\0';
        //    printf("echo> %s", str);
        //} else {
        //    if (t < 0) perror("recv");
        //    else printf("Server closed connection\n");
        //    exit(1);
        //}

    close(s);

    return 0;
}