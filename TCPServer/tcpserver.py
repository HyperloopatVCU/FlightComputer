import logging
import threading
from queue import Queue
from socket import *


class TCPComm(object):

    def __init__(self, host, port):

        self.logger = logging.getLogger('TCP')

        self.logger.info("[+] Initializing Communication")

        self.packets = Queue(-1)  # Might need more than one queue for the different sensors
        self.host = host
        self.port = port

        self.num_of_connections = 4

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def connect(self):

        threads = []

        self.server.listen(10)
        self.logger.info("[+] Listening on port", self.port)  # TODO: [!!!] This is a syntax error

        for x in range(self.num_of_connections):
            client, address = self.server.accept()
            threads.append(threading.Thread(target=self.start, args=(client,), name=address))

        for thread in threads:
            thread.start()
            thread.join()

        self.logger.info("[+] Connections successful")

    def start(self, client):
        while True:
            data = client.recv(4096)

            if not data:
                break

            self.packets.put(data)

    def broadcast(self, msg):
        """
        TODO: Broadcast msg (Which should be some hex number) to all microcontrollers
        """
        self.logger.info("[*] Broadcast: %s", msg)  # TODO: [!!!] This is a syntax error

    def pop_data_packet(self):
        """
        TODO: pop a data packet and parse it appropriately

        """
        pass
