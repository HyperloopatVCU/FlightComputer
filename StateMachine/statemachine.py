
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
            "cold": 0x01,
            "warm": 0x02,
            "hot!": 0x03,
            "cool": 0x04
        }

        self.state = self.states["cold"]

    def warm_up(self):
        """
            Disengage Breaks, Arduino should zero sensors
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
        When state = 'cold' broadcast state change
        """
        self.state = self.states["cool"]
