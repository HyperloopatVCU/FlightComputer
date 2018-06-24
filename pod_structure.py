
class Pod(object):
    """

    Data fields associated with the pod

    """

    def __init__(self):
        self.acceleration = { "x": 0.0, "y": 0.0, "z": 0.0 }
        self.speed = 0.0
        self.position = 0.0

    def __str__(self):
        pass

    def __repr__(self):
        return "<POD(pos: {:.2f}, vel: {:.2f}, acc:\
            {:.2f})>".format(self.position, self.speed, self.acceleration["x"])
    

