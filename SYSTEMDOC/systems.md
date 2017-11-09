*systems.txt*		Documentation on Pod Systems		Nov.07, 2017

*Pod_Systems*		sorted by initialization order
===============================================================================
|Main_Computer|
  |MCP|		|  Master Control Program
	|FR|	 \	Flight Routine			( |software.txt| )
	|HR|	  |	Health Routine			( |software.txt| )
	|DR-MCP|    |	Data registration		( |protocol.txt| )
	|CT-MCP|    |	Communication			( |protocol.txt| )
	|NT|	  |	Networking

|Data_and_Actuation_System|
  |DAQ|		|  Data Acquisition Controller
	|SR|	 \	Sampling Routine		( |software.txt| )
	|DR-DAS|    |	Data Registration		( |protocol.txt| )
	|CT-DAS|    |	Communication			( |protocol.txt| )
  |MAC|		|  Mechanism and Attitude Controller
	|PR|	 \	|PID| execution routine		( |software.txt| )
	|CT-MAC|    |	Communication			( |protocol.txt| )
	|HS|	  |	Header layout specification	( |hardware.txt| )



 vim:tw=78:ft=help:norl:
