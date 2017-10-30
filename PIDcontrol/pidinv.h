#ifndef PIDINV_H
#define PIDINV_H

struct pidprops {
	double Kp;
	double Ki;
	double Kd;
	double sp;
	double pe;
	double igral;
};

typedef struct pidprops PID;

extern PID prop_default;

double pidder(PID *props, double input, double dt);

#endif
