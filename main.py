import argparse
from time import time
from threading import Thread
from StateMachine.statemachine import MainSM
from TCPServer.tcpserver import TCPComm
from HardwareControl.hardwarecontroller import Brakes, MotorController


def main(behavior, host, port):
    """

    TODO: Change behavior based on `behavior` argument
            e.g. Launch, Debug, Test, Run GUI, etc., etc.

    1.) Start Web Server
    2.) Initialize State Machine
    TODO: Initialize Health Monitoring System

    """

    tcp = TCPComm(host, port)
    tcp.connect()
    sm = MainSM(tcp, Brakes(), MotorController())

    try:
        # Separate threads let the server and state machine be concurrent
        tcp_thread = Thread(target=tcp.start)
        sm_thread = Thread(target=sm.warm_up, args=(0.1,))

        # Kills threads when the main thread finishes
        tcp_thread.setDaemon(True)
        sm_thread.setDaemon(True)

        tcp_thread.start()
        sm_thread.start()

        # Prevents the main thread from exiting immediately
        sm_thread.join()
        tcp_thread.join()
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

    time_naught = time()
    main(args.behavior, args.host, args.port)
    time_final = time() - time_naught

    print("\n\n[+] Flight Sequence Finished")
    print("[+] Time Elapsed {} seconds\n\n".format(time_final))

