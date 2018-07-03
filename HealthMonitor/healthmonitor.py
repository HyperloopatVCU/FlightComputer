"""
    Improvements that need to be made:
    Instead of providing exact numbers, we need ranges of values for necessary data
"""

class Temperature:
    def battery(self, battery_temperature):
        if self.battery_temperature >= 112:
            print("battery temperature good")
        elif self.battery_temperature <= 122:
            print("max battery temperature reached")
        else:
            print("battery temperature too high")
            self.sm.estop_signal = True

    def motor(self, motor_temperature):
        if self.motor_temperature >= 165:
            print("motor temp good")
        elif self.motor_temperature <=175:
            print("max motor temperature reached")
        else:
            print("motor temp too high")
            self.sm.estop_signal = True

    def controller(self, motor_controller):
        if self.motor_controller >= 184:
            print("controller temp good")
        elif self.motor_controller <= 194:
            print("controller reached max temp")
        else:
            print("controller temp too high")
            self.sm.estop_signal = True

class HighPower:
    def high_battery(self, voltage, current):
        if self.voltage <= 90.8 and self.current <= 465:
            print("high power battery and voltage are fine")
        else:
            print("high power battery voltage or current too high")
            if self.voltage >= 90.8:
                print("voltage nearing max")
            elif voltage == 100.8:
                print("voltage at maximum")
            else:
                print("voltage too high")
                self.sm.estop_signal = True
            if self.current >= 465:
                print("current nearing max")
            elif current == 475:
                print("current at max")
            else:
                print ("current too high")
                self.sm.estop_signal = True

class LowPowerOne:
    def LowPowerOne(self, voltage, current):
        if self.voltage <= 50.4 and self.current <= 3:
            print("low power systems good")
        else:
            print("low power critical")
            if self.voltage > 50.4:
                print("voltage too high")
                self.sm.estop_signal = True
            if self.current >= 3:
                print("current too high")
                self.sm.estop_signal = True

class LowPowerTwoBrake:
    class BrakeA:
        def LowBrakeA(self, voltage, current):
            if self.voltage <= 12.6 and self.current <= 4:
                print("brake power good")
            else:
                print("brake systems critical")
                if self.voltage > 12.6:
                    print("voltage too high")
                    self.sm.estop_signal = True
                if self.current > 4:
                    print("current too high")
                    self.sm.estop_signal = True
    class BrakeB:
        def LowBrakeB(self, voltage, current):
            if self.voltage <= 12.6 and self.current <= 4:
                print("brake power good")
            else:
                print("brake systems critical")
                if self.voltage > 12.6:
                    print("voltage too high")
                   self.sm.estop_signal = True
                if self.current > 4:
                    print("current too high")
                   self.sm.estop_signal = True

class PotentiometerBrakes:
    def BrakePotentiometer(self, voltage, current):
        if self.voltage <= 1 and self.current <= 3:
            print("potentiometer average good")
        else:
            print("potentiometer average too much voltage or current")
            if self.voltage >= 12.6:
                print("voltage too high")
               self.sm.estop_signal = True
            if self.current >= 4:
                print("current too high")
               self.sm.estop_signal = True
#        Change Values

class Distance:
    def pod_distance_from_track(self,time):
        if self.time <=17.08:
            acceleration = 4.5
            distance = acceleration * time**2
        else:
            acceleration = -21.5
            distance = acceleration * time**2

class Sensors:
    def HPS_check(self,hpsone,hpstwo,hpsthree,hpsfour, hpsfailcount):
        self.hpsfailcount = 0
        while True:
            try:
                packet1 = self.comm.controller1.get(timeout=2)
            except:
                "Emergency Stop the Pod"
                self.hpsfailcount = self.hpsfailcount + 1

            if packet1["horizontal"]["error"] == 0:
                self.hpsone = 1
            else:
                self.hpsone = 0
                self.hpsfailcount = self.hpsfailcount + 1
                print("Error with HPS #1")

            try:
                packet2 = self.comm.controller2.get(timeout=2)
            except:
                "Emergency Stop the Pod"
                self.hpsfailcount = self.hpsfailcount + 1
            if packet2["horizontal"]["error"] == 0:
                self.hpstwo = 1
            else:
                self.hpstwo = 0
                self.hpsfailcount = self.hpsfailcount + 1
                print("Error with HPS #2")

            try:
                packet3 = self.comm.controller3.get(timeout=2)
            except:
                "Emergency Stop the Pod"
                self.hpsfailcount = self.hpsfailcount + 1
                return 1
            if packet3["horizontal"]["error"] == 0:
                self.hpsthree = 1
            else:
                self.hpsthree = 0
                self.hpsfailcount = self.hpsfailcount + 1
                print("Error with HPS #3")

            try:
                packet4 = self.comm.controller4.get(timeout=2)
            except:
                "Emergency Stop the Pod"
                self.hpsfailcount = self.hpsfailcount + 1
            if packet4["horizontal"]["error"] == 0:
                self.hpsfour = 1
            else:
                self.hpsfour = 0
                self.hpsfailcount = self.hpsfailcount + 1
                print("Error with HPS #3")

            if self.hpsfailcount >= 2:
                self.sm.estop_signal = True== True

    def VPS(self,vpsone,vpstwo,vpsthree,vpsfour, vpsfailcount):
        self.vpsfailcount = 0
        while True:

            packet1 = comm.controller1.get(timeout=2)
            if self.comm.microcontroller[1]["vertical"]["error"] == 0:
                self.vpsone = 1
            else:
                self.vpsone = 0
                self.vpsfailcount = self.vpsfailcount + 1
                print("Error with VPS #1")

            packet2 = comm.controller2.get(timeout=2)
            if self.comm.microcontroller[2]["vertical"]["error"] == 0:
                self.vpstwo = 1
            else:
                self.vpstwo = 0
                self.vpsfailcount = self.vpsfailcount + 1
                print("Error with VPS #2")

            packet3 = comm.controller3.get(timeout=2)
            if self.comm.microcontroller[3]["vertical"]["error"] == 0:
                self.vpsthree = 1
            else:
                self.vpsthree = 0
                self.vpsfailcount = self.vpsfailcount + 1
                print("Error with VPS #3")

            packet4 = comm.controller4.get(timeout=2)
            if self.comm.microcontroller[4]["vertical"]["error"] == 0:
                self.vpsfour = 1
            else:
                self.vpsfour = 0
                self.vpsfailcount = self.vpsfailcount + 1
                print("Error with VPS #4")

            if self.vpsfailcount >= 2:
                self.sm.estop_signal = True== True

    def IMU(self,imuone,imutwo,imuthree,imufour, imufailcount):
        self.imufailcount = 0
        sensorcondition = True
        while sensorcondition:

            packet1 = comm.controller1.get(timeout=2)
            if self.comm.microcontroller[1]["accelerometer"]["error"] == 0:
               self.imuone = 1
            else:
                self.imuone = 0
                self.imufailcount = self.imufailcount + 1
                print("Error with IMU #1")

            packet2 = comm.controller2.get(timeout=2)
            if self.comm.microcontroller[2]["accelerometer"]["error"] == 0:
                self.imutwo = 1
            else:
                self.imutwo = 0
                self.imufailcount = self.imufailcount + 1
                print("Error with IMU #2")

            packet3 = comm.controller3.get(timeout=2)
            if self.comm.microcontroller[3]["accelerometer"]["error"] == 0:
                self.imuthree = 1
            else:
                self.imuthree = 0
                self.imufailcount = self.imufailcount + 1
                print("Error with IMU #3")

            packet4 = comm.controller4.get(timeout=2)
            if self.comm.microcontroller[4]["accelerometer"]["error"] == 0:
                self.imufour = 1
            else:
                self.imufour = 0
                self.imufailcount = self.imufailcount + 1
                print("Error with IMU #4")

            if self.imufailcount >= 2:
                sensorcondition = False

                self.sm.estop_signal = True== True


    def BMS(self, bmsone, bmstwo,bmsthree,bmsfour, bmsfive, bmssix, bmsseven, bmseight, bmsnine, bmsten, bmseleven, bmstwelve, bmsthirteen, bmsfourteen, bmsifteen,bmsfailcount):
            # while Something
            #if data exist
                self.bmsone = 1
            #else
                self.bmsone = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #1")
            #if data exists
                self.bmstwo = 1
            #else
                self.bmstwo = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #2")
            #if data exists
                self.bmsthree = 1
            #else
                self.bmsthree = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #3")
            #if data exists
                self.bmsfour = 1
            #else
                self.bmsfour = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #4")
            #if data exists
                self.bmsfive = 1
            #else
                self.bmsfive = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #5")
            #if data exists
                self.bmssix = 1
            #else
                self.bmssix = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #6")
            #if data exists
                self.bmsseven = 1
            #else
                self.bmsseven = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #7")
            #if data exists
                self.bmseight = 1
            #else
                self.bmseight = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #8")
            #if data exists
                self.bmsnine = 1
            #else
                self.bmsnine = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #9")
            #if data exists
                self.bmsten = 1
            #else
                self.bmsten = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #10")
            #if data exists
                self.bmseleven = 1
            #else
                self.bmseleven = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #11")
            #if data exists
                self.bmstwelve = 1
            #else
                self.bmstwelve = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #12")
            #if data exists
                self.bmsthirteen = 1
            #else
                self.bmsthirteen = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #13")
            #if data exists
                self.bmsfourteen = 1
            #else
                self.bmsfourteen = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #14")
            #if data exists
                self.bmsfifteen = 1
            #else
                self.bmsfifteen = 0
                self.bmsfailcount = self.bmsfailcount + 1
                print("Error with BMS #15")
            if self.bmsfailcount >= 4:
                self.sm.estop_signal = True== True

class HealthMonitor(object):

    def __init__(self, comm, sm, pod):
        self.comm = comm
        self.sm = sm

        self.logger = logging.getLogger('TCP')

        self.logger.info("[+] Initializing Health Monitoring")

        self.stop_signal = False

        self.config = ConfigParser()
        self.config.read('config.ini')
        
        self.frames = 0
        self.frame_rate = self.config['Health'].getint('frame_rate')

    def run(self):
            while not self.stop_signal:
                self.update()
                sleep(1/self.frame_rate)
                self.frames += 1

    def update(self):    
        """
        Any threshold values that may need to be adjusted should be added to
        the config.ini file in the root of the program directory. 
        """
        
        if sm.state == sm.states["cold"]:
            # accelerating is the only important state right now
            return

        elif sm.state == sm.states["ready"]:
            # accelerating is the only important state right now
            return

        elif sm.state == sm.states["accelerating"]:
            """
            1.)
                Compare sensor values from each queue in the tcpserver.py
                module. If one sensor is a certain deviation away from all the
                rest or there is an error marked by the microcontroller on the
                packet then discard it.

            2.) If a critical sensor has been discarded then stop the pod

            3.) Average all the non-discarded sensor values and update the
                global Pod class in the pod_structure.py module. 
            """
            return

        elif sm.state == sm.states["stopping"]:
            # accelerating is the only important state right now
            return

