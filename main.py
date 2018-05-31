#!/usr/bin/python3

import logging
from os import path
from logging import config
from time import time
from threading import Thread
from StateMachine.statemachine import MainSM
from Communication.tcpserver import TCPComm
from HealthMonitor.healthmonitor import HealthMonitor
from HardwareControl.brakes import Brakes
from HardwareControl.motor import MotorController


# TODO: Added a config file for the configuration of the network for the microcontrollers
def main(root_logger):
    """

    Spin out the different threads for comm, state machine, and health.

    """

    tcp = TCPComm()
    sm = MainSM(tcp, Brakes(), MotorController())
    health = HealthMonitor(tcp, sm)

    try:
        # Separate threads let everything be concurrent
        tcp_thread = Thread(target=tcp.connect, name='TCPThread')
        sm_thread = Thread(target=sm.cold_loop, name='StateMachineThread')
        health_thread = Thread(target=health.run, name='HealthThread')

        # Kills threads when the main thread finishes
        tcp_thread.setDaemon(True)
        sm_thread.setDaemon(True)
        health_thread.setDaemon(True)

        # Running the threads
        tcp_thread.start()
        sm_thread.start()
        health_thread.start()

        # Prevents the main thread from exiting immediately
        sm_thread.join()
        tcp_thread.join()
        health_thread.join()
    except KeyboardInterrupt:
        root_logger.info("[*] Keyboard Interrupt!!!") 
        pass
    finally:
        root_logger.debug("[+] Shutdown triggered")
        health.shutdown_pod()


if __name__ == "__main__":

    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.ini')
    logging.config.fileConfig(log_file_path)
    logger = logging.getLogger('root')

    print("\n\n\x1b[33m")
    print("====================================================================================================================================")
    print("\n")
    print("██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗      ██████╗  ██████╗ ██████╗      █████╗ ████████╗    ██╗   ██╗ ██████╗██╗   ██╗")
    print("██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗    ██╔══██╗╚══██╔══╝    ██║   ██║██╔════╝██║   ██║")
    print("███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     ██║   ██║██║   ██║██████╔╝    ███████║   ██║       ██║   ██║██║     ██║   ██║")
    print("██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║     ██║   ██║██║   ██║██╔═══╝     ██╔══██║   ██║       ╚██╗ ██╔╝██║     ██║   ██║")
    print("██║  ██║   ██║   ██║     ███████╗██║  ██║███████╗╚██████╔╝╚██████╔╝██║         ██║  ██║   ██║        ╚████╔╝ ╚██████╗╚██████╔╝")
    print("╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝         ╚═╝  ╚═╝   ╚═╝         ╚═══╝   ╚═════╝ ╚═════╝")
    print("\n")
    print("====================================================================================================================================")
    print("\n\x1b[m")
    print("SYSTEM LOGS:")
    print("------------------------------------------------------------------------")

    time_naught = time()
    main(logger)
    time_final = time() - time_naught

    logger.info("[+] Flight Sequence Finished")
    logger.info("[+] Time Elapsed {0:.2f} seconds\n".format(time_final))

    print("------------------------------------------------------------------------")
    print("\n")
    print("END OF FLIGHT")

