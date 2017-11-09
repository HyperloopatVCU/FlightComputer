*software.txt*		Software Specifics			Nov. 08, 2017

*Software*		sorted by initialization order
===============================================================================
  |Flight_Routine|  |  Interfaces with the |MAC| to control the craft.
  |Health_Routine|  |  Produces a report of craft status based on collected
		     \ data samples. Grades severity of hardware errors.
  |Sample_Routine|  |  One big part of the |DAS| -> |DAQ|; Collects and
		     \ packages data samples from all attached sensors.
  |Pidder_Routine|  |  One big part of the |DAS| -> |MAC|; Produces the control
		     \ signals for all connected hardware devices.


 vim:tw=78:ft=help:norl:
