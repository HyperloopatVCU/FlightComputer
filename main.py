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

    Spin up the different threads for comm, state machine, and health.

    """
    PROMPT = "~$ "

    tcp = TCPComm()
    sm = MainSM(tcp, Brakes(), MotorController())
    health = HealthMonitor(tcp, sm)

    while True:
        user_input = input(PROMPT)

        if user_input == "launch":

            if sm.state != 0x02:
                self.logger.info("[*] State much be warm before launching")
                continue

                # Separate threads let everything be concurrent
            tcp_thread = Thread(target=tcp.connect, name='TCPThread')
            sm_thread = Thread(target=sm.launch, args=(0,), name='StateMachineThread')
            health_thread = Thread(target=health.run, name='HealthThread')

            # Running the threads
            tcp_thread.start()
            sm_thread.start()
            health_thread.start()

            # Joining threads back to main
            sm_thread.join()
            tcp.stop_signal = True
            health.stop_signal = True
            tcp_thread.join()
            health_thread.join()


        elif user_input == "warm":
            sm.warm_up()
    
        elif user_input == "idle":
            if sm.state != 0x02:
                root_logger.info("[!!!] Cannot move pod before warming up")
                continue

            # Separate threads let everything be concurrent
            tcp_thread = Thread(target=tcp.connect, name='TCPThread')
            sm_thread = Thread(target=sm.launch, args=(1,), name='StateMachineThread')
            health_thread = Thread(target=health.run, name='HealthThread')

            # Running the threads
            tcp_thread.start()
            sm_thread.start()
            health_thread.start()

            # Joining threads back to main
            sm_thread.join()
            tcp.stop_signal = True
            health.stop_signal = True
            tcp_thread.join()
            health_thread.join()

        elif user_input == "shutdown":
            return

        else:
            continue


if __name__ == "__main__":

    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.ini')
    logging.config.fileConfig(log_file_path)
    logger = logging.getLogger('root')
    """
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
    """
    print("SYSTEM LOGS:")
    print("------------------------------------------------------------------------")

    time_naught = time()
    main(logger)
    time_final = time() - time_naught

    logger.info("[+] Finished")
    logger.info("[+] Time Elapsed {0:.2f} seconds\n".format(time_final))

    print("------------------------------------------------------------------------")
    print("\n")
    print("END OF FLIGHT")

