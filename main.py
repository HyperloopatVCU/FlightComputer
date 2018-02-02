
from StateMachine.statemachine import MainSM
from WebServer.webserver import start
from threading import Thread
from time import time, sleep

def main():
    '''

    1.) Start Web Server
    2.) Initialize State Machine

    '''

    host = 'localhost'
    port = 8000


    SM = MainSM()

    try:
        # Serperate threads let the server and sm be concurrent
        sm_thread = Thread(target=SM.run, args=(0.1,))
        tcp_thread = Thread(target=start)

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
    t0 = time()
    main()
    tf = time() - t0

    print("\n\n[+] Flight Sequence Finished {:0.2}\n\n".format(tf))

