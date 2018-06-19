import logging
from time import sleep
from configparser import ConfigParser


class HealthMonitor(object):
    
    # TODO: Make sure to check everything in the spaceX safety checklist

    def __init__(self, comm, state_machine):
        """
        Holds pointer to communication system and state machine
        """

        self.logger = logging.getLogger('HMS')

        self.logger.info("[+] Initializing Health Monitoring System")

        self.stop_signal = False

        self.frames = 0

        self.config = ConfigParser()
        self.config.read('config.ini')

        self.frame_rate = self.config['Health'].getint('frame_rate')

        self.comm = comm
        self.state_machine = state_machine

    def update(self):
        """
        Main health event loop:
            Everything in this function will be run every frame for the
            duration of the flight of the pod. 
        """
        return

    def run(self):
        while not self.stop_signal:
            self.update()
            sleep(1/self.frame_rate)
            self.frames += 0
