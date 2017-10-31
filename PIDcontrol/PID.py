
import sys
import time

def testfunc(x):
    return x * 0.468

class PID(object):

    def __init__(self, kp=0, kd=0, ki=0, goal=1, func=None, dt=0.1):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.goal = goal
        self.previous_error = 0
        self.integral = 0

        self.func = func
        self.actual = 0
        self.dt = dt

    def run(self):
        de = self.goal - self.func(self.actual)

        self.integral = de * self.dt

        P = (self.kp * de)
        I = (self.ki * self.integral)
        D = (self.kd * (de - self.previous_error)/self.dt)

        output = P + I + D

        self.previous_error = de

        self.actual += output

        return self.actual

    def __next__(self):
        for i in range(self.limit):

            out = self.run()

            time.sleep(0.5)  # makes things less overwhelming

            yield out

    def __iter__(self):
        return self


    def __call__(self, limit=10):
        self.limit = limit
        return next(self)


if __name__ == '__main__':

    pid = PID(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), func=testfunc)

    for x in pid():
        print(testfunc(x))
