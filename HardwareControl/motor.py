import logging
from PCANBasic import *

class Motor(object):

    # init is a method/function that runs before anything else runs. So we are using it to declare methods
    # that are needed in a chronological order.
    def __init__(self):
        self.logger = logging.getLogger('Motor')
        self.InitializeBasicComponents()
        self.InitializeConnection()

    def InitializeBasicComponents(self):
        self.m_objPCANBasic = PCANBasic()

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



    def accelerate(self, rpm):
        self.logger.debug("[*] Accelerating")

    def idle(self):
        self.logger.debug("[*] Motor Idle")
