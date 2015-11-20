/*
MIDaC KIPR Link ROSL (Robotic System Abstraction Layer)
Version 0.1
*/

#ifdef _WIN32
#   error "Not supported platform"
#elif __APPLE__
    #include "TargetConditionals.h"
    #if TARGET_IPHONE_SIMULATOR
#   error "Not supported platform"
    #elif TARGET_OS_IPHONE
#   error "Not supported platform"
    #elif TARGET_OS_MAC
        #define Platform 0
    #else
    #   error "Unknown Apple platform"
    #endif
#elif __linux__
    #define Platform 1
#elif __unix__ // all unices not caught above
#   error "Not supported platform"
#elif defined(_POSIX_VERSION)
#   error "Not supported platform"
#else
#   error "Unknown compiler"
#endif


#define true 1
#define false 0

#include <stdio.h>
#include <unistd.h>
#include <string.h> /* for strncpy */

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <arpa/inet.h>
#include "LINKV1.c"


int socket_desc;
struct sockaddr_in server;
char *message , server_reply[2048];
int errorCounter = 0;

void splitAndSend(char* msg);
void sendMessage(char* message);
char* recvMessage();
char* getIP();

char *StringPadRight(char *string, int padded_len, char *pad) {
    int len = (int) strlen(string);
    if (len >= padded_len) {
        return string;
    }
    int i;
    for (i = 0; i < padded_len - len; i++) {
        strcat(string, pad);
    }
    return string;
}

void splitAndSend(char* msg){
    char buff[2048];
    int i;
    for(i=0; i<strlen(msg); i+=2047){
        memcpy( buff, &msg[i], 2047 );
        buff[2047] = '\0';
        sendMessage(buff);
    }
}

void sendMessage(char* message){
    if(strlen(message) > 2047){
        splitAndSend(message);
    } else {
        char sendingMessage[2049];

        memcpy( sendingMessage, &message[0], 2048 );
        StringPadRight(sendingMessage, 2048, " ");
        sendingMessage[2048] = '\0';

        if( send(socket_desc , sendingMessage , strlen(sendingMessage) , 0) < 0)
        {
            printf("RSAL_PROC_MESSAGE: Sending failed\n");  
            errorCounter++;      
        } 
    }
    msleep(5);
}

char* recvMessage(){
    if( recv(socket_desc, server_reply , 2000 , 0) < 0)
    {
        printf("RSAL_PROC_MESSAGE: Receiving failed\n");
        return "Failed";
    } 

    return server_reply;
}

char* getIP(){
    
    int fd;
    struct ifreq ifr;
    
    
    /* I want to get an IPv4 IP address */
    ifr.ifr_addr.sa_family = AF_INET;
    
    /* I want IP address attached to "eth0" */
    if(Platform == 0){
        strncpy(ifr.ifr_name, "en0", IFNAMSIZ-1);
    }
    else
    {
        strncpy(ifr.ifr_name, "wlan0", IFNAMSIZ-1);
    }
    
    ioctl(socket_desc, SIOCGIFADDR, &ifr);
    
    /* display result */
    return inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr);
}

int main(){
    //Create socket
    socket_desc = socket(AF_INET , SOCK_STREAM , 0);
    if (socket_desc == -1)
    {
        //printf("RSAL_PROC_MESSAGE: Could not create socket\n");
    }
    

    server.sin_addr.s_addr = inet_addr(getIP());
    server.sin_family = AF_INET;
    server.sin_port = htons( 62626 );
 
    //Connect to remote server
    if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
        //puts("RSAL_PROC_MESSAGE: connect error");
        return 1;
    }
    //printf("RSAL_PROC_MESSAGE: Connected\n");

    int status = 0;
    while(status < 3){
        if(status == 0){
            sendMessage("{ \"B-Connect\" : \"\" }");
            status = 1;
            //printf("RSAL_PROC_MESSAGE: Sent B-Connect Message\n");
        } else if (status == 1){
            recvMessage();
            status = 2;
            //printf("RSAL_PROC_MESSAGE: Received Conn-Ack\n");
        } else if (status == 2){
           /*Send the connLao*/
            sendMessage(generateConnLAO());
            status = 3;
            //printf("RSAL_PROC_MESSAGE: Sent ConnLAO Message\n");
        }   
    }
    printf("RSAL_PROC_MESSAGE: Connected\n");
    
    /*two threads startoff here*/
    int running = true;
    while(running){
        sendMessage(generateDataMsg());

        if(errorCounter > 10){
            running = false;
        }
    }
}
