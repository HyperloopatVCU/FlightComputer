*states.txt*		Operational States			Nov. 08, 2017


===============================================================================

	This document defines the specific operational states within which the
pod's systems may exist. The pod is described as a state machine because the
controlled flight is dependent upon its previous state. These systems of the
pod depend upon each other in order to react appropriately to the pod's
response and any external commands. Additionally, I should explain that the
pod is designed to be majorally autonomous, and any external control exists as
either a safeguard for unforseen events or as a result of removing manual
controls from the physical pod.

	These states are transmitted by the pod in the data packet. Most of
them are not required to be transmitted, but exist as a debugging tool for
ground control. These states are reported by the Master Control Program, which
keeps track of when these states are active. States aren't explicitly 




-------------------------------------------------------------------------------
*System_States*
-------------------------------------------------------------------------------

*COLD* - Total system suspension, all systems offline except main computer and
NAP.

*WARM* - All systems are activated and "warmed up". Any hardware that requires
initialization is done so while the system is warming up.

*HOT!* - The pod is only in this state once it has launched. This state can
only be exited once the pod has stopped.

*BUST* - This mode is transmitted if the pod has exitted a hot state before
stopping, either by some mechanical failure or repeatedly (and unsuccessfully)
attempting to stop. The pod may be in an unknown state. All systems except the
main computer should be killed.


-------------------------------------------------------------------------------
*Queue_States*
-------------------------------------------------------------------------------

*EMTY* - The command queue is empty.

*PROC* - The command queue is not empty nor full. Commands which exist in the
queue are being processed.


-------------------------------------------------------------------------------
*Process_States*
-------------------------------------------------------------------------------


 vim:tw=78:ts=8:ft=help:norl:
