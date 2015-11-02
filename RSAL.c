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

void sendMessage(char message[]){
	if( send(socket_desc , message , strlen(message) , 0) < 0)
    {
		printf("Sending failed\n");        
    } else {
		printf("Sending succeeded\n");
	}
}

char* recvMessage(){
	if( recv(socket_desc, server_reply , 2000 , 0) < 0)
    {
        printf("Receiving failed\n");
    	return "Failed";
	} else {
		printf("Receiving successful\n");
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
        strncpy(ifr.ifr_name, "eth0", IFNAMSIZ-1);
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
        printf("Could not create socket");
    }
    
    server.sin_addr.s_addr = inet_addr(getIP());
    server.sin_family = AF_INET;
    server.sin_port = htons( 62626 );
 
    //Connect to remote server
    if (connect(socket_desc , (struct sockaddr *)&server , sizeof(server)) < 0)
    {
        puts("connect error");
        return 1;
    }
}
