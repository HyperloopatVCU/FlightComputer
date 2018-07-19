
from time import sleep
from socket import *

class TCPClient(object):

    def __init__(self, pod):

        self.pod = pod

        self.host = 'localhost'
        self.port = 8000

    def run(self):
        while True:
            self.update()
            sleep(0.1)

    def update(self):
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((self.host, self.port))

        pod_dict = self.pod.to_dict()
        
        client.send(json.dumps(pod_dict))

        client.close()
