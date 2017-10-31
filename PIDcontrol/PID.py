
import sys

def testfunc(x):
    return x * 0.468

class PID(object):

    def __init__(self, kp=0, kd=0, ki=0, goal=1):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.goal = goal
        self.previous_error = 0
        self.integral = 0

    def run(self, actual, dt):
        de = self.goal - actual

        self.integral = de * dt

        P = (self.kp * de)
        I = (self.ki * self.integral)
        D = (self.kd * (de - self.previous_error)/dt)

        output = P + I + D

        self.previous_error = de

        return output


if __name__ == '__main__':

    x, dt = 0, 0.1

    pid = PID(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))

    for i in range(5):
        x += pid.run(testfunc(x), dt)
        print("%d %.2f %f" % (i, dt*i, testfunc(x)))
