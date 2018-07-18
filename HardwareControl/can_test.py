# Importing PCANBasic API for tests
# Importing Json to read json file
# pprint to check if json is being decoded properly

from PCANBasic import *
import json
from pprint import pprint

# main function decodes the json
def main():
    print("PCAN TESTING!!")
    # Function calls for the tests
    initializeChannelTest()

    with open("can_test_msg.json") as can_data:
        canJsonData = json.loads(can_data.read())
        for line in can_data:
            writeTest(self,canJsonData['ID'], canJsonData['MSGTYPE'], canJsonData['DLC'], canJsonData['DATA'])
            readTest()

# Initializes channel to test
def initializeChannelTest():
    m_objPCANBasic = PCANBasic()
    m_CHANNEL = PCAN_USBBUS1
    result = m_objPCANBasic.InitializeFD(m_CHANNEL, m_BitrateTXT.get())
    if result == PCAN_ERROR_OK:
        print("No errors found with initialization!")
        if result == PCAN_ERROR_CAUTION:
            print("irregularities were found while communicating")
    else:
        print("Error code: " + result + " Check the API for the kind of error occcured")


# Connection string for baud_rate (can be modified to our requirements)
def InitializeConnection(self):
    self.m_BitrateTXT = StringVar(value="f_clock_mhz=20, nom_brp=5, nom_tseg1=2, nom_tseg2=1, nom_sjw=1, data_brp=2, data_tseg1=3, data_tseg2=1, data_sjw=1")


# Checks if reads are being made properly
def readTest():
    readResults = m_objPCANBasic.ReadFD(m_channel)
    if result == PCAN_ERROR_OK:
        print("No errors found! (read)")
        print(result[1:])  # Prints the message
    else:
        print("Error code: " + result + " Check the API for the kind of error occcured")

# Checks if writes are being made properly
def writeTest(self, Id, Type, length, data):
    CANMsg = TPCANMsg(Id, Type, length, data)
    writeResult = self.m_objPCANBasic.WriteFD(m_PcanHandle, TestCANMsg)
    if writeResult == PCAN_ERROR_OK:
        print("No errors found! (write)")
    else:
        print("Error code: " + result + " Check the API for the kind of error occcured")

if __name__ == '__main__':
    main()
