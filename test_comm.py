import sys
from socket import *
from threading import Thread

def handler(client):
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break

            print(data.decode('UTF-8'))
        except:
            break

server = socket(AF_INET, SOCK_STREAM)
server.bind(('10.0.0.0', 8000))
server.listen(10)

try:
    while True:
        client, addr = server.accept()
        t = Thread(target=handler, args=(client,))
        t.start()
    
finally:
    print("Closing")
    server.close()
    sys.exit(0)


