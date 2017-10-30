#include"pidinv.h"
//(design this to be used atomically)

struct pidprops prop_default = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

double pidder(PID *props, double input, double dt) {
	double de = props->sp - input;
	props->igral += de * dt;
	props->dtive = (de - props->pe) / dt;
	double output = (props->Kp * de) + (props->Ki * props->igral) + (props->Kd * props->dtive);
	props->pe = de;
	return output;
}
