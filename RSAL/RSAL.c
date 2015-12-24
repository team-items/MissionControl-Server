/*
MIDaC KIPR Link ROSL (Robotic System Abstraction Layer)
Version 0.1
*/
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include "LINKV1.c"

#define SOCK_PATH "uds_socket"

int sock, t, len, i;
struct sockaddr_un remote;
char str[2048];

void sendMsg(char* msg){
    if(strlen(msg) > 2047){
        int ward = (strlen(msg)/2048) + 1;
        char* message = malloc(2048*ward);
        strcpy(message, msg);
        for(i=strlen(msg); i<2048*ward; i++){
            message[i] = ' ';
        }
        message[2048*ward] = '\0';
        if (send(sock, message, strlen(message), 0) == -1) {
            perror("send");
            exit(1);
        }
        free(message);
    }else{
        char* message = malloc(2048);
        strcpy(message, msg);
        for(i=strlen(msg); i<2048; i++){
            message[i] = ' ';
        }
        message[2048] = '\0';
        if (send(sock, message, strlen(message), 0) == -1) {
            perror("send");
            exit(1);
        }
        free(message);
    }
}

char* receiveMsg(){
    if ((t=recv(sock, str, 2048, 0)) > 0) {
        str[t] = '\0';
        return str;
    } else {
        if (t < 0) perror("recv");
        else printf("RSAL_PROC_MSG: Server closed connection\n");
        exit(1);
    }
}

int estConnection(){
    sendMsg("{ \"B-Connect\" : \"\"}");
    receiveMsg();
    sendMsg(generateConnLAO());
    return 0;
}

int main(int argc, char *argv[])
{

    if ((sock = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
        perror("socket");
        exit(1);
    }


    remote.sun_family = AF_UNIX;
    strcpy(remote.sun_path, SOCK_PATH);
    len = strlen(remote.sun_path) + sizeof(remote.sun_family) + 1;
    if (connect(sock, (struct sockaddr *)&remote, len) == -1) {
        perror("connect");
        exit(1);
    }

    estConnection();

    while(1) {
        char* msg = receiveMsg();
        if(is_get(msg)){ 
            msg = generateDataMsg();
            sendMsg(msg);
        } else {
            control(msg);
        }
    }

    close(sock);

    return 0;
}