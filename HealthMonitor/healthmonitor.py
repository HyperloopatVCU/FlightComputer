import logging
from time import sleep


class HealthMonitor(object):
    
    # TODO: Make sure to check everything in the spaceX safety checklist
    

    def __init__(self, comm, state_machine):
        """
        Holds pointer to communication system and state machine
        """

        self.logger = logging.getLogger('HMS')

        self.logger.info("[+] Initializing Health Monitoring System")

        self.comm = comm
        self.state_machine = state_machine

    def update(self):
        pass

    def run(self, frame_rate=10):
        while True:
            self.update()
            sleep(1/frame_rate)
