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


    def ReadMessageFD(self):
        # We execute the "ReadFD" function of the PCANBasic
        #
        result = self.m_objPCANBasic.ReadFD(self.m_PcanHandle)

        if result[0] == PCAN_ERROR_OK:
            # We show the received message
            #
            self.ProcessMessageFD(result[1:])

        return result[0]

    ## Inserts a new entry for a new message in the Message-ListView
    ##
    def InsertMsgEntry(self, newMsg, timeStamp):
        # Format the new time information
        #
        with self._lock:
            # The status values associated with the new message are created
            #
            msgStsCurrentMsg = MessageStatus(newMsg,timeStamp,len(self.m_LastMsgsList))
            msgStsCurrentMsg.MarkedAsInserted = False
            msgStsCurrentMsg.ShowingPeriod = self.m_ShowPeriod
            self.m_LastMsgsList.append(msgStsCurrentMsg)

    def ProcessMessageFD(self, *args):
        with self._lock:
            # Split the arguments. [0] TPCANMsgFD, [1] TPCANTimestampFD
            #
            theMsg = args[0][0]
            itsTimeStamp = args[0][1]

            for msg in self.m_LastMsgsList:
                if (msg.CANMsg.ID == theMsg.ID) and (msg.CANMsg.MSGTYPE == theMsg.MSGTYPE):
                    msg.Update(theMsg, itsTimeStamp)
                    return
            self.InsertMsgEntry(theMsg, itsTimeStamp)

    ## Processes a received message, in order to show it in the Message-ListView
    ##
    def ProcessMessage(self, *args):
        with self._lock:
            # Split the arguments. [0] TPCANMsg, [1] TPCANTimestamp
            #
            theMsg = args[0][0]
            itsTimeStamp = args[0][1]

            newMsg = TPCANMsgFD()
            newMsg.ID = theMsg.ID
            newMsg.DLC = theMsg.LEN
            for i in range(8 if (theMsg.LEN > 8) else theMsg.LEN):
                newMsg.DATA[i] = theMsg.DATA[i]
            newMsg.MSGTYPE = theMsg.MSGTYPE
            newTimestamp = TPCANTimestampFD()
            newTimestamp.value = (itsTimeStamp.micros + 1000 * itsTimeStamp.millis + 0x100000000 * 1000 * itsTimeStamp.millis_overflow)
            self.ProcessMessageFD([newMsg, newTimestamp])

    ## Thread-Function used for reading PCAN-Basic messages
    ##
    def CANReadThreadFunc(self):
        try:
            self.m_Terminated = False

            # Configures the Receive-Event.
            #
            stsResult = self.m_objPCANBasic.SetValue(self.m_PcanHandle, PCAN_RECEIVE_EVENT, self.m_ReceiveEvent)

            if stsResult != PCAN_ERROR_OK:
                print ("Error: " + self.GetFormatedError(stsResult))
            else:
                while not self.m_Terminated:
                    if win32event.WaitForSingleObject(self.m_ReceiveEvent, 50) == win32event.WAIT_OBJECT_0:
                        self.ReadMessages()

                # Resets the Event-handle configuration
                #
                self.m_objPCANBasic.SetValue(self.m_PcanHandle, PCAN_RECEIVE_EVENT, 0)
        except:
            print ("Error occurred while processing CAN data")


    def accelerate(self, rpm):
        self.logger.debug("[*] Accelerating")

    def idle(self):
		_setThrottle(0)
        self.logger.debug("[*] Motor Idle")

#**************************************************************************************************************#
    # Supporting Functions

    """
    Throttle back-end
	Usage: supply percent of throttle to set (for 30% pass 30)
	Returns nothing
    """
    def _setThrottle(self, percent):
        val = int(255 * (percent / 100))
        spi.writebytes([val])

    """
    Keyswitch back-end
	Usage: to engage keyswitch, pass True
	Returns nothing
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
