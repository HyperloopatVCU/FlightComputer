#!/usr/bin/python3

import time
from queue import Queue


class PodStateMachine(object):

    def __init__(self):

        self.states = {
            "cold":  1,
            "warm": 2,
            "hot": 3,
            "bust": 4
        }

        self.state = 1

    def update(self):
        pass


if __name__ == '__main__':

    pod_state_machine = PodStateMachine()

    while True:
        pod_state_machine.update(

            )

        time.sleep(0.01)

    print("Finished flight")
