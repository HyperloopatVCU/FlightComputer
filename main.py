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
    PROMPT = "[Hyperloop@\x1b[33mVCU\x1b[m] ~$ "

    tcp = TCPComm()
    sm = MainSM(tcp, Brakes(), MotorController())
    health = HealthMonitor(tcp, sm)

    health_thread = Thread(target=health.run, name='HealthThread')
    health_thread.start()

    while True:
        user_input = input(PROMPT)

        if user_input == "launch":

            sm_thread = Thread(target=sm.launch, args=(0,), name='StateMachineThread')
            sm_thread.start()

        elif user_input == "warm":
            sm.warm_up()
    
        elif user_input == "drift":

            sm_thread = Thread(target=sm.launch, args=(1,), name='StateMachineThread')
            sm_thread.start()

        elif user_input == "shutdown":
            if sm.state != sm.states["cold"]:
                root_logger.warn("[*] Program cannot exit safety currently!")
                root_logger.warn("======> State: %s", sm.state_str[sm.state])
                continue

            health.stop_signal = True
            health_thread.join()
            return

        elif user_input == "estop":
            if input("Are you sure? [y/N] ") in ("Y", "y"):
                """ESTOP the pod"""
                sm.estop()
            else:
                continue

        elif user_input == "state":
            print(sm.state_str[sm.state])

        elif user_input == "help":
            print("Usage: ")
            print("[1]     help     : This menu")
            print("[2]     state    : Current state")
            print("[3]     warm     : Warm up pod")
            print("[4]     launch   : Launch pod with max speed")
            print("[5]     drift    : Launch pod slowly")
            print("[6]     estop    : Emergency stop the moving pod")
            print("[7]     shutdown : Shutdown program")
            print()

        else:
            print("Usage: ")
            print("[1]     help     : This menu")
            print("[2]     state    : Current State")
            print("[3]     warm     : Warm up pod")
            print("[4]     launch   : Launch pod with max speed")
            print("[5]     drift    : Launch pod slowly")
            print("[6]     estop    : Emergency stop the moving pod")
            print("[7]     shutdown : Shutdown program")
            print()

        

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

