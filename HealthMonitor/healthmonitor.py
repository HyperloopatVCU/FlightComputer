import logging
from time import sleep


class HealthMonitor(object):
    
    # TODO: Make sure to check everything in the spaceX safety checklist
    # TODO: HAHAHAHAHAHAA
    

    def __init__(self, comm, state_machine):
        """
        Holds pointer to communication system and state machine
        """

        self.logger = logging.getLogger('HMS')

        self.logger.info("[+] Initializing Health Monitoring System")

        self.frames = 0

        self.health = "Green"

        self.comm = comm
        self.state_machine = state_machine

    def shutdown_pod(self):
        self.logger.info("[+] Shutting down pod systems")
        state_machine.shutdown()
        comm.close()

    def update(self):
        """
        Main event loop:
            Everything in this function will be run every frame for the
            duration of the flight of the pod. 
        """
        if self.frames != 0 and self.frames % 100 == 0:
            self.logger.debug("[*] System Health: %s", self.health)

    def run(self, frame_rate=10):
        while True:
            self.update()
            sleep(1/frame_rate)
            self.frames += 1
