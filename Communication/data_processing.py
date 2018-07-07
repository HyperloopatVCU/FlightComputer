
import logging
from configparser import ConfigParser

class Data_Processing(object):

    def __init__(self, tcp):
        self.logger = logging.getLogger('COMM')
        self.logger.info("[+] Initializing Data Processor")

        self.config = ConfigParser()
        self.config.read('config.ini')

        self.frame_rate = self.config['DataProc'].getint('frame_rate')

    def run(self):
        while True:
            self.update()

    def update(self):
        """
        Do the averaging and deviation checking in this function
        """
        pass
