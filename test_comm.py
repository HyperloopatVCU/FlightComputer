
from threading import Thread
from pod_structure import Pod
from Communication.tcpserver import TCPServer
from Communication.data_processing import Data_Processing

def main():
    pod = Pod()
    comm = TCPServer()
    processing = Data_Processing(comm)

    try:
        tcp_thread = Thread(target=comm.connect) 
        data_thread = Thread(target=processing.run)

        tcp_thread.start()
        data_thread.start() 
    
    except:
        tcp.stop_signal = True
        tcp_thread.join()
        tcp.close()

if __name__ == '__main__':
    main()
