
# VCU Hyperloop
---------------------------------------

System to be run on the main computer
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

## Prerequisites
Certain python 3 packages are needed to run some commands
```
~$ pip3 install -r requirements.txt
```
    
## Pod Launch
Command for final launch

```
~$ python3 main.py launch
```    
