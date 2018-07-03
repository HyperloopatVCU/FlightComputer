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
            # accelerating is the only important state right now
            return

        elif sm.state == sm.states["ready"]:
            # accelerating is the only important state right now
            return

        elif sm.state == sm.states["accelerating"]:
            """
            1.)
                Compare sensor values from each queue in the tcpserver.py
                module. If one sensor is a certain deviation away from all the
                rest or there is an error marked by the microcontroller on the
                packet then discard it.

            2.) If a critical sensor has been discarded then stop the pod

            3.) Average all the non-discarded sensor values and update the
                global Pod class in the pod_structure.py module. 
            """
            return

        elif sm.state == sm.states["stopping"]:
            # accelerating is the only important state right now
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

