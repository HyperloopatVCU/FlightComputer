import logging
from queue import Queue
from socket import *


class TCPComm(object):

    def __init__(self, host='localhost', port=8000):

        self.logger = logging.getLogger('TCP')

        self.logger.info("[+] Initializing Communication")

        self.packets = Queue(-1)
        self.host = host
        self.port = port

        self.client = None
        self.client_address = None

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def connect(self):
        self.server.listen(10)
        self.logger.info("[+] Listening on port", self.port)  # [!!!] This is a syntax error

        self.client, self.client_address = self.server.accept()
        self.logger.info("[+] Connection successful from", self.client_address)  # [!!!] This is a syntax error

    def start(self):
        while True:
            data = self.client.recv(4096)

            if not data:
                break

            self.packets.put(data)

    def broadcast(self, msg):
        """
        TODO: Broadcast msg (Which should be some hex number) to all microcontrollers
        """
        self.logger.info("[*] Broadcast: %s", msg)  # [!!!] This is a syntax error

    def pop_data_packet(self):
        """
        TODO: pop a data packet and parse it appropriately

        """
        pass
