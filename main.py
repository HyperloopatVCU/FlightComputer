
from statemachine.statemachine import MainSM

def main():
    SM = MainSM()

    while True:
        try:
            SM.update()
        except KeyboardInterrupt as e:
            break;
    
    print("\n\n[+] Flight Sequence Finished")


if __name__ == "__main__":
    main()
