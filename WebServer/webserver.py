
from socket import *
from threading import Thread

def conn_handler(client):
    client.close()

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8000
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, PORT))

    server.listen(100)
    print("[+] Listening on port {}".format(PORT))

    while True:
        client, addr = sock.accept()
        print("[+] Connection made from {}".format(addr))

        t = Thread(conn_handler, args=(client,))
        t.start()


    
