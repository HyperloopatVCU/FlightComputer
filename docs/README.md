
# VCU Hyperloop
---------------------------------------

## DISCLAIMER
------------------------------------
This is a *prototype* of the program for the main computer. The real program is
written in C and is currently still in contruction. Although this is a
prototype, it works exactly like the real version just slower. By natural of
the language, python is slower than C but python is much faster to develop
which is why it is common to prototype projects in python and write them in C
later. Python unfortunately has a feature called the GIL. This prevents python
programs from running different threads parallel to each other on multiple CPU
cores. This is also why the real program is being written in C. If the real
version hasn't been finished yet and you need this program immediately then *it
will work*. 

# Program to be run on the main computer
---------------------------------------

The software is split into four packages: Communication, StateMachine,
HealthMonitor, and HardwareControllers. The communication handles everything
involving getting data from sensors to other services. StateMachine controls
the state of the pod at all times. It is in charge of getting the pod from a
braking position to full speed to braking again. The HealthMonitor checks to
ensure that nothing is going wrong. If something goes wrong such as a software
error or mechanical failure, the HealthMonitor will tell the StateMachine to
stop the pod. Finally, the HardwareControllers are controlled by the
StateMachine to control things like the motor and brakes.

## Configuration
Generally most configuration information and collection of glabal variables on the
pod are stored in the config.ini file at the programs root. The two things not
configured in the config.ini file are the logger and the network. The logger is
configured using its own seperate log.ini file and the network configuration file will be
created soon. To clarify, by the network configuration, I do not mean the
configuration file for the tcp server, I am referring to the file that gets
broadcasted across the network at the start up of the pod to let the
microcontroller understand how the system looks.

## Prerequisites
Certain python 3 packages are needed to run some commands
```
~$ pip3 install -r requirements.txt
```
    
## Pod Launch
Command for final launch

```
~$ sudo python3 main.py
```  

