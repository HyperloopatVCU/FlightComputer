
class Pod(object):
    """

    Data fields associated with the pod

    """

    def __init__(self):
        """
        Add to this 'struct' whatever fields are needed for the statemachine
        and the remote gui
        """
        self.fiducialCount = 0
        self.position = { "x": 0.0, "y": 0.0, "z": 0.0}                     # meters
        self.brakePosition = {"front_left": 0.0, "front_right":\
                0.0, "back_left": 0.0, "back_right": 0.0}                   # millimeters
        self.speed = {"x": 0.0}                                             # meters per second
        self.acceleration = { "x": 0.0, "y": 0.0, "z": 0.0 }                # meters per square second
        self.temp = {"high": 0.0, "low": 0.0, "front": 0.0, "back": 0.0}    # celsius
        self.volt = {"high": 0.0, "low": 0.0, "front": 0.0, "back": 0.0}    # volt
        self.current = {"high": 0.0, "low": 0.0, "front": 0.0, "back": 0.0} # ampere
        self.throttle = 0.0                                                 # percent

        # Contains errors from Communication
        self.error = []

    def __repr__(self):
        return "<POD pos: {:.2f}, vel: {:.2f}, acc:\
            {:.2f} >".format(self.position["x"], self.speed["x"], self.acceleration["x"])
    

