
from time import time
from threading import Thread
from StateMachine.statemachine import MainSM
from WebServer.webserver import start


def main():
    """

    1.) Start Web Server
    2.) Initialize State Machine
    TODO: Initialize Health Monitoring System

    """

    host = 'localhost'
    port = 8000

    sm = MainSM()

    try:
        # Separate threads let the server and sm be concurrent
        sm_thread = Thread(target=sm.run, args=(0.1,))
        tcp_thread = Thread(target=start, args=(host, port))

        # Kills threads when the main thread finishes
        sm_thread.setDaemon(True)
        tcp_thread.setDaemon(True)

        sm_thread.start()
        tcp_thread.start()

        # Prevents the main thread from exiting immediately
        sm_thread.join()
        tcp_thread.join()
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    """
    TODO: 
        Command line arguments to explicitly state whether the pod is being
        tested, launched, debugged etc. etc. and new behaviors to change accordingly
    """

    time_naught = time()
    main()
    time_final = time() - time_naught

    print("\n\n[+] Flight Sequence Finished")
    print("[+] Time Elapsed {:0.2} seconds\n\n".format(time_final))

