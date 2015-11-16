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

#ifndef msleep
    #include <unistd.h>
    void msleep(int time){
        usleep(time*1000);
    }
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


int socket_desc;
struct sockaddr_in server;
char *message , server_reply[2048];
int errorCounter = 0;

void sendMessage(char* message){
    char sendingMessage[2048];
    strcpy(sendingMessage, message);

    if( send(socket_desc , sendingMessage , strlen(message) , 0) < 0)
    {
        printf("RSAL_PROC_MESSAGE: Sending failed\n");  
        errorCounter++;      
    } 
    msleep(10);
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
            sendMessage("{ \"ConnLAO\" : {    \"Information\" : { \"Integer\" : { \"Analog1\" : {     \"DataType\" : \"Integer\",     \"MaxBound\" : 2047,     \"MinBound\" : 0,     \"Graph\"  : 40 }, \"Analog2\" : {     \"DataType\" : \"Integer\",     \"MaxBound\" : 2047,     \"MinBound\" : 0,     \"Graph\"  : 40 } }, \"Bool\" : { \"Digital1\" : {     \"DataType\" : \"Bool\",     \"Graph\"  : 40 }, \"Digital2\" : {     \"DataType\" : \"Bool\",     \"Graph\"  : 40 } }     } } }");
            status = 3;
            //printf("RSAL_PROC_MESSAGE: Sent ConnLAO Message\n");
        }   
    }
    /*two threads startoff here*/
    int running = true;
    while(running){
        sendMessage("{\"Data\":{\"Analog1\":500, \"Analog2\":510, \"Digital1\": \"true\", \"Digital2\": \"false\"}}");

        if(errorCounter > 10){
            running = false;
        }
    }
}
