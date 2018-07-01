
class Pod(object):
    """

    Data fields associated with the pod

    """

    def __init__(self):
        """
        Add to this 'struct' whatever fields are needed for the statemachine
        and the remote gui
        """
        self.position = 0.0
        self.speed = 0.0
        self.acceleration = { "x": 0.0, "y": 0.0, "z": 0.0 }
        self.temp = {"high": 0.0, "low": 0.0, "front": 0.0, "back": 0.0}
        self.volt = {"high": 0.0, "low": 0.0, "front": 0.0, "back": 0.0}
        self.current = {"high": 0.0, "low": 0.0, "front": 0.0, "back": 0.0}

    def __repr__(self):
        return "<POD pos: {:.2f}, vel: {:.2f}, acc:\
            {:.2f} >".format(self.position, self.speed, self.acceleration["x"])
    

