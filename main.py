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
    Prompt for hyperloop

    The prompt will soon come from the remote computer controlling the pod
    but for now it is here. 

    """
    PROMPT = "~$ "

    tcp = TCPComm()
    sm = MainSM(tcp, Brakes(), MotorController())
    health = HealthMonitor(tcp, sm)

    while True:
        user_input = input(PROMPT)

        if user_input == "launch":

            sm_thread = Thread(target=sm.launch, args=(0,), name='StateMachineThread')
            sm_thread.start()
            sm_thread.join()


        elif user_input == "warm":
            sm.warm_up()
    
        elif user_input == "idle":

            sm_thread = Thread(target=sm.launch, args=(1,), name='StateMachineThread')
            sm_thread.start()
            sm_thread.join()

        elif user_input == "shutdown":
            if sm.start != sm.states["cold"]:
                self.logger.warn("[*] Program cannot exit safety currently!")
                self.logger.warn("======> State: %s", sm.states_str(sm.state))
            return

        elif user_input == "estop":
            

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

