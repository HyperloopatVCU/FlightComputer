import logging

class State(object):
    """
    Super class for all pod states
    """

    def __init__(self, controllers):
        self.logger = logging.getLogger('SM')
        self.logger.debug("[+] State change: ", str(self))

        self.controllers = controllers

    def on_event(self, event):
        pass

    def __repr__(self):
        return self.__class__.__name__


class StartUp(State):

    def on_event(self, event):

        return Estop(self.controllers)


class HealthCheck(State):

    def on_event(self, event):

        return Estop(self.controllers)


class Accelerate(State):

    def on_event(self, event):

        return Estop(self.controllers)


class MotorShutdown(State):

    def on_event(self, event):

        return Estop(self.controllers)


class Brake(State):

    def on_event(self, event):

        return Estop(self.controllers)

class Finish(State):

    def on_event(self, event):

        return Estop(self.controllers)


class Estop(State):

    def on_event(self, event):
        return self

