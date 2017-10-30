#ifndef PIDINV_H
#define PIDINV_H

//(design this to be used atomically)


struct pidprops {
	double Kp;
	double Ki;
	double Kd;
	double sp;
	double pe;
	double igral;
	double dtive;
};
extern struct pidprops prop_default;

typedef struct pidprops PID;

double pidder(PID *props, double input, double dt);

#endif
