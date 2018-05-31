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

        self.frames = 0

        self.health = "Green"

        self.config = ConfigParser()
        self.config.read('HealthMonitor/config.ini')

        self.comm = comm
        self.state_machine = state_machine

    def shutdown_pod(self):
        self.logger.info("[+] Shutting down pod systems")
        self.state_machine.shutdown()
        self.comm.close()

    def update(self):
        """
        Main event loop:
            Everything in this function will be run every frame for the
            duration of the flight of the pod. 
        """
        if self.frames != 0 and self.frames % 100 == 0:
            self.logger.debug("[*] System Health: %s", self.health)

    def run(self):
        while True:
            self.update()
            sleep(1/self.config['Health'].getint('frame_rate'))
            self.frames += 1
