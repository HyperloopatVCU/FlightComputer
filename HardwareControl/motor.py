import logging
import fnmatch #### supporting libraries
import os
import re
import sys

try:
    import RPi.GPIO as gpio
    import spidev #### This library needs to be installed and the SPI device enabled. (add "dtparam=spi=on" to /boot/config.txt)
except RuntimeError:
    print("Did you run this on the RPi as root?")
    sys.exit(1)

from PCANBasic import *

class Motor(object):

    _SAFETY = 25

    # init is a method/function that runs before anything else runs. So we are using it to declare methods
    # that are needed in a chronological order.
    def __init__(self):
        self.logger = logging.getLogger('Motor')
        self.InitializeBasicComponents()
        self.InitializeConnection()

        # initialize raw gpio line
        gpio.setup(self.SAFETY, gpio.OUT)

        # initialize new SPI object
        self.spi = spidev.SpiDev()
        self.spi.bits_per_word = 8

        # attempt to find device parameters (if this doesn't work out, replace with manual initialization)
        self.spidevname = ""
        for file in os.listdir("/dev/"):
            if fnmatch.fnmatch(file, "spidev*"):
                self.spidevname = file
                break
        if len(self.spidevname) < 10:
            raise FileNotFoundError("cannot find spidev device in '/dev/' (bad search query, perhaps?)")
        else:
            match = re.search(r"(?P<X>\d+)[.](?P<Y>\d+)", self.spidevname)
            if not match:
                raise ValueError("cannot parse spidev device name (bad regex, perhaps?)")
            else:
                # open spi device with found parameters
                self.spi.open(int(match.group('X')), int(match.group('Y')))

    def InitializeBasicComponents(self):
        self.m_objPCANBasic = PCANBasic()

        self.m_IDTXT = StringVar(value="000")
        self.m_LengthNUD = StringVar(value="8")
        self.slip_frequency = 0
        self.temperature = 0

        # This is used to make sure that default channel is undefined before/after use.
        self.m_PcanHandle = PCAN_NONEBUS

        # Initilizes Channel to use. In our case, we are using USB-channel 1.
        # We have channel options from 1 till 16.
        self.m_CHANNEL = PCAN_USBBUS1

        # Initlizes USBCHANNEL 1
        result = self.m_objPCANBasic.InitializeFD(self.m_CHANNEL, self.m_BitrateTXT.get())

        # Handler for channel
        if result != PCAN_ERROR_OK:
            if result != PCAN_ERROR_CAUTION:
                print(self.GetFormatedError(result))
            else:
                self.IncludeTextMessage('******************************************************')
                self.IncludeTextMessage('The bitrate being used is different than the given one')
                self.IncludeTextMessage('******************************************************')
                result = PCAN_ERROR_OK
        else:
                # Prepares the PCAN-Basic's PCAN-Trace file
                #
                self.ConfigureTraceFile()

        # Sets the connection status of the form
        #
        self.SetConnectionStatus(result == PCAN_ERROR_OK)



    # This is the connection string for flexible data transfer rates, (Make changes to this according to our needs)
    def InitializeConnection(self):
        self.m_BitrateTXT = StringVar(value="f_clock_mhz=20, nom_brp=5, nom_tseg1=2, nom_tseg2=1, nom_sjw=1, data_brp=2, data_tseg1=3, data_tseg2=1, data_sjw=1")


    ## Help Function used to get an error as text
    ##
    def GetFormatedError(self, error):
        # Gets the text using the GetErrorText API function
        # If the function success, the translated error is returned. If it fails,
        # a text describing the current error is returned.
        #
        stsReturn = self.m_objPCANBasic.GetErrorText(error, 0)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            return stsReturn[1]

    def WriteDataFD(self):

        CANMsg = TPCANMsg()

        # We configurate the Message.  The ID,
        # Length of the Data, Message Type and the data
        #
        CANMsg.ID = int(self.m_IDTXT.get(),16)
        CANMsg.DLC = int(self.m_LengthNUD.get())
        CANMsg.MSGTYPE = PCAN_MESSAGE_EXTENDED if self.m_ExtendedCHB.get() else PCAN_MESSAGE_STANDARD
        CANMsg.MSGTYPE |= PCAN_MESSAGE_FD.value if self.m_FDCHB.get() else PCAN_MESSAGE_STANDARD.value
        CANMsg.MSGTYPE |= PCAN_MESSAGE_BRS.value if self.m_BRSCHB.get() else PCAN_MESSAGE_STANDARD.value

        # If a remote frame will be sent, the data bytes are not important.
        #
        if self.m_RemoteCHB.get():
            CANMsg.MSGTYPE |= PCAN_MESSAGE_RTR.value
        else:
            #iLength = self.GetLengthFromDLC(CANMsg.DLC, not(CANMsg.MSGTYPE & PCAN_MESSAGE_FD.value))
            iLength = GetLengthFromDLC(CANMsg.DLC, not(CANMsg.MSGTYPE & PCAN_MESSAGE_FD.value))
            # We get so much data as the Len of the message
            #
            for i in range(iLength):
                CANMsg.DATA[i] = int(self.m_DataEdits[i].get(),16)

                # The message is sent to the configured hardware
                #
        return self.m_objPCANBasic.WriteFD(self.m_PcanHandle, CANMsg)





    def accelerate(self, rpm):
        self.logger.debug("[*] Accelerating")

    def idle(self):
        self.logger.debug("[*] Motor Idle")

#**************************************************************************************************************#
    # Supporting Functions
    
    """
    Throttle back-end
    """
    def _setThrottle(self, percent):
        val = int(255 * percent)
        spi.writebytes([val])
        return percent * 12 # return expected voltage at wiper position

    """
    Keyswitch back-end
    """
    def _safety(self, safe):
        if safe:
            gpio.output(self._SAFETY, gpio.HIGH)
        else:
            gpio.output(self._SAFETY, gpio.LOW)

#**************************************************************************************************************#
    # Error Handlers

    ## Entry txtID OnLeave handler
    ##
    def txtID_Leave(self,*args):
        # Calculates the text length and Maximum ID value according
        # with the Message Typ
        #
        if self.m_ExtendedCHB.get():
            iTextLength = 8
            uiMaxValue = 0x1FFFFFFF
        else:
            iTextLength = 3
            uiMaxValue = 0x7FF

        try:
            iValue = int(self.m_IDTXT.get(),16)
        except ValueError:
            iValue = 0
        finally:
            # The Textbox for the ID is represented with 3 characters for
            # Standard and 8 characters for extended messages.
            # We check that the ID is not bigger than current maximum value
            #
            if iValue > uiMaxValue:
                iValue = uiMaxValue
                self.m_IDTXT.set("{0:0{1}X}".format(iValue,iTextLength))
                return True
