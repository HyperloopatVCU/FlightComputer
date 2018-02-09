
from socket import *
from threading import Thread


def conn_handler(client):
    """
    TODO:
        Send data to state machine and data grader
        Determine commands to send
    """

    client.close()
    return


def start(host='localhost', port=8000):
    server = socket(AF_INET, SOCK_STREAM) 
    server.bind((host, port))

    server.listen(4)
    print("[+] Listening on port {}".format(port))

    while True:
        client, addr = server.accept()
        print("[+] Connection made with {}".format(addr))

        t = Thread(target=conn_handler, args=(client,))
        t.start()
