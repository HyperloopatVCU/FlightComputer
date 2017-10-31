#include"pidinv.h"

struct pidprops prop_default = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};	//  Define initial positions of default properties.

float pidder(PID *props, float input, float dt) {
	float de = props->sp - input;			//  Specify 'error'.
	props->igral += de * dt;			//  Produce next integral step.
	float output = (props->Kp * de) + (props->Ki * props->igral) + (props->Kd * (de - props->pe) / dt); //  Calculate PID output.
	props->pe = de;					//  Update past 'error'.
	return output;
}
