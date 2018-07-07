
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


class Pre_Operational(State):

    def on_event(self, event):

        if event == 'start-up':
            # TODO: If moving forward, goto estop

        elif event == 'launch':
            return Operational(self.controllers)
        elif event == 'drift':
            return Operational(self.controllers)
        else:
            return Estop(self.controllers)


class Operational(State):

    def on_event(self, event):
        
        if event == 'launch-clear':
            return Accelerating(self.controllers)
        if event == 'drift-clear':
            return Accelerating(self.controllers)
        else:
            return Estop(self.controllers)


class Accelerating(State):

    def on_event(self, event):

        if event == 'motor-disengage':
            return Decelerating(self.controllers)
        else:
            return Estop(self.controllers)


class Decelerating(State):

    def on_event(self, event):
        if event == 'brakes-engage':
            return Stop(self.controllers)
        else:
            return Estop(self.controllers)


class Stop(State):

    def on_event(self, event):
        if event == 'stopped':
            return Pre_Operational(self.controllers)
        else:
            return Estop(self.controllers)


class Estop(State):

    def on_event(self, event):
        return self

