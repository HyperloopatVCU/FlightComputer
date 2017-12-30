*OPST-toc.txt*		Overview of Operational States		Nov. 07, 2017
  public display(){

*Operational_States*	sorted by function
===============================================================================

System states		( |systems.md| - |list_of_systems| )
-------------------------------------------------------------------------------
  |COLD|	|  Cold status, only |MCP| is active.
  |WARM|	|  Warm status, all systems active and ready for operation.
  |HOT!|	|  System has launched.

Queue states		( |commands.md| - |command_queue| )
-------------------------------------------------------------------------------
  |EMTY|	|  The queue is empty and can receive commands.
  |PROC|	|  The commands in the queue are being processed. New
		 \	commands will be added, but must wait to be processed.
  |FULL|	|  No more commands can be received at this moment.

Commands    pre		( |commands.md| - |command_format| )
-------------------------------------------------------------------------------
  |WMUP|     |COLD| |  Setup a pre-launch operational state.
  |CLDN|     |WARM| |  Cancel |WMUP| and shutdown systems.
  |HOLD|     |HOT!| |  Hold all responses at current level. Overrides current
		 \	operational target.
  |LNCH|     |WARM| |  Begin launch routine.
  |STOP|     |HOT!| |  Perform a |SSTOP|, queued.
  |HALT|      ""  |  Preform a |SSTOP|, immediately. Clears queue.
  |AHCF|      ""  |  Perform an |ESTOP|, queued.
  |KILL|      ""  |  Preform an |ESTOP|, immediately. Clears queue.
  |CNCL|     |CONF| |  Cancels current command when on confirmation prompt.
  |SMPL|	|  Send the current data sample to Ground Control asap.
  |STAT|	|  Send the current pod status to Ground Control asap. May be
		 \	set up to run on a timer system.

Process states		( |systems.md| - |processing_model| )
-------------------------------------------------------------------------------
  |TCHK|	|  Communications Check; make sure systems are wired properly.
  |ICON|	|  Initial Check; waits for |WARM| before collecting initial
		 \	condition data samples.
  |COLL|	|  Collecting data. This state is active until all data is
		 \	good and read out of buffers.
  |CONF|	|  Confirmation state. Stops reading queue and waits for
		 \	command or |CNCL| to be (re)sent.
  |WAIT|	|  Waiting for something from the system for which a process
		 \	state hasn't been specified.
  |NETX|	|  Transmitting onto network.
  |NETR|	|  Receiving from network.








 vim:tw=78:ts=8:ft=help:norl:
