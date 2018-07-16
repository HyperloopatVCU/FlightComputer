#!/usr/bin/python3

import logging
from os import path 
from logging import config 
from time import time
from threading import Thread
from pod_structure import Pod
from StateMachine.statemachine import MainSM
from Communication.tcpserver import TCPComm
from Communication.data_processing import Data_Processing
from HealthMonitor.healthmonitor import HealthMonitor
from HardwareControl.brakes import Brakes
from HardwareControl.motor import Motor

def main(root_logger):
    """
    Prompt for hyperloop

    The prompt will soon come from the remote computer controlling the pod
    but for now it is here. 

    """
    PROMPT = "[Hyperloop@\x1b[33mVCU\x1b[m] ~$ "

    pod = Pod()
    tcp = TCPComm()
    sm = MainSM(pod, Brakes(pod), Motor())
    dp = Data_Processing(tcp)
    health = HealthMonitor(pod, tcp, sm)

    health_thread = Thread(target=health.run, name='HealthThread')
    dp_thread = Thead(target=health.run, name='DPThread')
    health_thread.start()
    dp_thread.start()

    hist = open('.pod_history', 'w')

    while True:
        user_input = input(PROMPT)
        hist.write(user_input + '\n')

        if user_input == "state":
            print(sm.state)
			
        elif user_input == "launch":

            if input("Are you sure? [y/N]") in ("Y", "y"):
                sm.on_event('launch')

        elif user_input == "drift":
            sm.on_event('drift')

        elif user_input == "estop":
            if input("Are you sure (Program must be restarted to recover from estop)? [y/N] ") in ("Y", "y"):
                """ESTOP the pod"""
                sm.on_event('estop')
            else:
                continue
				
        elif user_input == "shutdown":
            if sm.state != "Pre_Opeartional" or sm.state != "Estop":
                print("[*] Program cannot exit safety currently!")
                print("======> State: %s", sm.state)
                continue

            tcp.close()

            health.stop_signal = True
            dp.stop_signal = True
            health_thread.join()
            dp_thread.join()

            hist.write('\n')
            hist.close()
            return

        else:
            print("Commands: ")
            print("[1]     help     : This menu")
            print("[2]     state    : Current State")
            print("[3]     launch   : Launch pod with max speed")
            print("[4]     drift    : Launch pod slowly")
            print("[5]     estop    : Emergency stop the moving pod")
            print("[6]     shutdown : Shutdown program")


if __name__ == "__main__":

    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.ini')
    logging.config.fileConfig(log_file_path)
    logger = logging.getLogger('root')

    print("====================================================================================================================================")
    print("\n\n\x1b[33m")
    print("\n")
    print("██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗      ██████╗  ██████╗ ██████╗      █████╗ ████████╗    ██╗   ██╗ ██████╗██╗   ██╗")
    print("██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗    ██╔══██╗╚══██╔══╝    ██║   ██║██╔════╝██║   ██║")
    print("███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     ██║   ██║██║   ██║██████╔╝    ███████║   ██║       ██║   ██║██║     ██║   ██║")
    print("██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║     ██║   ██║██║   ██║██╔═══╝     ██╔══██║   ██║       ╚██╗ ██╔╝██║     ██║   ██║")
    print("██║  ██║   ██║   ██║     ███████╗██║  ██║███████╗╚██████╔╝╚██████╔╝██║         ██║  ██║   ██║        ╚████╔╝ ╚██████╗╚██████╔╝")
    print("╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝         ╚═╝  ╚═╝   ╚═╝         ╚═══╝   ╚═════╝ ╚═════╝")
    print("\n")
    print("\n\x1b[m")
    print("====================================================================================================================================")

    time_naught = time()
    main(logger)
    time_final = time() - time_naught

    logger.info("[+] Finished")
    logger.info("[+] Time Elapsed {0:.2f} seconds\n".format(time_final))

    print("\n")
    print("END OF FLIGHT")

