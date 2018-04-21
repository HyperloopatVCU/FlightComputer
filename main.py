import argparse
import logging
from logging import config
from time import time
from threading import Thread
from StateMachine.statemachine import MainSM
from TCPServer.tcpserver import TCPComm
from HealthMonitor.healthmonitor import HealthMonitor
from HardwareControl.hardwarecontroller import Brakes, MotorController


# TODO: Added a config file for the configuration of the network for the microcontrollers
# TODO: Add logging to every package and possibly change from .conf file to .json
def main(behavior, host, port):
    """

    TODO: Change behavior based on `behavior` argument
            e.g. Launch, Debug, Test, Run GUI, etc., etc.

    1.) Start Web Server
    2.) Initialize State Machine
    3.) Initialize Health Monitor

    """

    tcp = TCPComm(host, port)
    sm = MainSM(tcp, Brakes(), MotorController())
    health = HealthMonitor(tcp, sm)

    try:
        # Separate threads let everything be concurrent
        tcp_thread = Thread(target=tcp.connect, name='TCPThread')
        sm_thread = Thread(target=sm.warm_up, args=(10,), name='StateMachineThread')
        health_thread = Thread(target=health.run, args=(10,), name='HealthThread')

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
        return


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Change pod behavior")
    parser.add_argument('behavior', metavar='Behavior', type=str,
                        help="Controller for how the system should run")
    parser.add_argument('--host', dest='host', type=str,
                        default='localhost', help="Host address for the server")
    parser.add_argument('--port', dest='port', type=int,
                        default=8000, help="Connection port for the server")

    args = parser.parse_args()

    logging.config.fileConfig('log.conf')
    logger = logging.getLogger('root')

    time_naught = time()
    main(args.behavior, args.host, args.port)
    time_final = time() - time_naught

    logger.info("\n\n[+] Flight Sequence Finished")
    logger.info("[+] Time Elapsed {} seconds\n\n".format(time_final))

