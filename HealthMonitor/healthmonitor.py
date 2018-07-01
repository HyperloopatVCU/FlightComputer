import logging
from time import sleep
from configparser import ConfigParser


class HealthMonitor(object):
    
    # TODO: Make sure to check everything in the spaceX safety checklist

    def __init__(self, Pod, comm, state_machine):
        """
        Holds reference to communication system and state machine
        """

        self.logger = logging.getLogger('HMS')

        self.logger.info("[+] Initializing Health Monitoring System")

        self.stop_signal = False

        self.frames = 0
        
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.frame_rate = self.config['Health'].getint('frame_rate')

        self.Pod = Pod
        self.comm = comm
        self.sm = state_machine

    def update(self):
        """
        Main health event loop:
            Everything in this function will be run every frame for the
            duration of the flight of the pod. 

        Any threshold values that may need to be adjusted should be added to
        the config.ini file in the root of the program directory. 
        """
        
        if sm.state == sm.states["cold"]:
            return

        elif sm.state == sm.states["ready"]:
            return

        elif sm.state == sm.states["accelerating"]:
            return

        elif sm.state == sm.states["stopping"]:
            return

        else:
            # It definitely shouldn't get here
            self.logger.critical("[!!!] Something is very wrong, State: %s", \
                                 sm.state)

    def run(self):
        while not self.stop_signal:
            self.update()
            sleep(1/self.frame_rate)
            self.frames += 1

