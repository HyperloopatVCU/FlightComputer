#ifndef PIDINV_H
#define PIDINV_H

struct pidprops {	//  PID properties structure
	float Kp;	//  Proportional constant
	float Ki;	//  Integral constant
	float Kd;	//  Derivative constant
	float sp;	//  Setpoint (target value)

	float pe;	//  Previous ;error'
	float igral;	//  Previous integral value
};

typedef struct pidprops PID;

extern PID prop_default;

float pidder(PID *props, float input, float dt);

#endif
