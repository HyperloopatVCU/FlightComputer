#include "pidinv.h"	//  PID library
#include <stdio.h>	//  printf
#include <stdlib.h>	//  atof

float testfunc(float x) {
	return 0.468*x;			// testing function.
}

int main(int argc, char* argv[]) {
	if (argc < 6)
		return -1;

	PID props = prop_default;	//  Initialize PID properties to zero.
	props.Kp = atof(argv[1]);	//  Receive command line args for PID constants, setpoint, and num of iterations.
	props.Ki = atof(argv[2]);	//  !! no input protection !!
	props.Kd = atof(argv[3]);
	props.sp = atof(argv[4]);

	int samples = atoi(argv[5]);

	float x = 0.0, dt = 0.1;	//  Initial positions.
					//  Print data to stdout in SC (UNIX spreadsheet program) format
	printf("format A 11 6 0\nformat B 11 6 0\nlabel A0 = \"time\"\nlabel B0 = \"samples\"\n");

	for(int i=1; i<=samples; i++) {
		x += pidder(&props, testfunc(x), dt);	//  Iterable PID, manipulated variable is a constant sum.
		printf("let A%d = %f\nlet B%d = %f\n", i, dt * ((float)i), i, testfunc(x)); //  SC formatted data output
	}

	printf("goto A0 B0\n");		//  Terminate output.
	return 0;
}
