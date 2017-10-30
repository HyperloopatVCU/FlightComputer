#include"pidinv.h"

struct pidprops prop_default = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};	//  Define initial positions of default properties.

double pidder(PID *props, double input, double dt) {
	double de = props->sp - input;		//  Specify "error".
	props->igral += de * dt;		//  Produce next integral step.
	double output = (props->Kp * de) + (props->Ki * props->igral) +
		(props->Kd * (de - props->pe) / dt); //  Calculate PID output.
	props->pe = de;		//  Update past 'error'.
	return output;
}
