
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <strings.h>

int main(int argc, char *argv[]) {
    int socketfd, portNumber, length;
    char readBuffer[2000], message[255];
    struct sockaddr_in serverAddress;
    struct hostent *server;

    sprintf(message, "GET / HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n", argv[1]);

    printf("Sending message: %s", message);

    if(argc <= 1) {
        printf("Incorrect usage, use: ./SampleWebClient.c hostname\n");
        return 2;
    }

    server = gethostbyname(argv[1]);
    if(server == NULL) {
        perror("Socket Client: error - unable to resolve host name.\n");
        return 1;
    }

    socketfd = socket(AF_INET, SOCK_STREAM, 0);
    if(socketfd < 0) {
        perror("Socket Client: error opening TCP IP-based socket.\n");
        return 1;
    }

    bzero((char *) &serverAddress, sizeof(serverAddress));
    portNumber = 8000;
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(portNumber);
    bcopy((char *) server->h_addr, (char *) &serverAddress.sin_addr.s_addr, server->h_length);

    if(connect(socketfd, (struct sockaddr *) &serverAddress, sizeof(serverAddress)) < 0) {
        perror("Socket Client: error connecting to the server.\n");
        return 1;
    }

    if(write(socketfd, message, sizeof(message)) < 0) {
        perror("Socket Client: error writing to socket.\n");
        return 1;
    }

    if(read(socketfd, readBuffer, sizeof(readBuffer)) < 0) {
        perror("Socket Client: error reading from socket\n");
        return 1;
    }

    printf("**START**\n%s\n**END**\n", readBuffer);
    close(socketfd);

    return 0;
}
