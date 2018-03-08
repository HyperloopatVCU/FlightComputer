
from time import sleep


class MainSM(object):

    def __init__(self, tcp, *hardware):

        print("[+] Initializing State Machine")

        self.tcp = tcp
        self.hardware = {
            "brakes": hardware[0],
            "motor": hardware[1]
        }

        self.states = {
            "cold": 0x01,  # Pod is off, This is the safe state
            "warm": 0x02,  # Preparing pod for flight
            "hot!": 0x03,  # Pod is in flight
            "cool": 0x04,  # Bring hot pod to a stop
            "stop": 0x05   # Emergency stop
        }

        self.state = self.states["cold"]

    def warm_up(self):
        """
            Disengage Breaks, microcontrollers should zero sensors
        """
        self.state = self.states["warm"]
        self.hardware["brakes"].disengage()

    def launch(self, frame_rate=10):
        print("[+] Launching Pod")
        while True:
            self.update()
            sleep(1/frame_rate)

    def update(self):
        """
        TODO: Logic to determine state!

        if at max speed || at max distance || critical error
            breaks

        """

        pass

    def shutdown(self):
        """
        TODO: Engage brakes
        [!!!] Be 100% sure the pod isn't accelerating before brakes engage
        """
        self.state = self.states["cool"]

        # After velocity = 0

        self.state = self.states["cold"]
