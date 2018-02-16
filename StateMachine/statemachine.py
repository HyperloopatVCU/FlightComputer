
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
            "cold": "cold",
            "warm": "warm",
            "hot!": "hot!"
        }

        self.state = self.states["cold"]

    def warm_up(self):
        """
        TODO: Disengage brakes, zero sensors
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
        When velocity = 0, broadcast software system shutdown
        """

        pass

