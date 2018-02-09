
from time import sleep


class MainSM(object):

    def __init__(self):

        print("[+] Initializing State Machine")

        self.states = {
                    "cold": "cold",
                    "warm": "warm",
                    "hot!": "hot!"
                    }

        self.state = self.states["cold"]

    def update(self):
        """
        TODO: Logic to determine state!
        """
        pass

    def run(self, frame_rate=10):
        while True:
            self.update()
            sleep(1/frame_rate)


