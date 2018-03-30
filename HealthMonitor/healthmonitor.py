
from time import sleep


class HealthMonitor(object):
    """
    TODO: Make sure to check everything in the spaceX safety checklist
    """

    def __init__(self, comm, state_machine):
        self.comm = comm
        self.state_machine = state_machine

    def update(self):
        pass

    def run(self, frame_rate=100):
        while True:
            self.update()
            sleep(1/frame_rate)
