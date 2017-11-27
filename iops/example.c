#include"iops.h"
#include<stdio.h>

int raw(uint8_t, uint8_t, char, uint64_t*);

int main() {
	port sys1 = {
		(uint8_t)0,
		(uint8_t)1,
		'p',
		(uint64_t)0x30313233,
		raw
	};
	fx(&sys1);
	return 0;
}

int raw(uint8_t p1, uint8_t p2, char f, uint64_t* dat) {
	int l;
	printf("line1@:%c line2@:%c function:%c data(ascii):%.4s\n", 
			(char)(p1+48), (char)(p2+48), f, (char*)dat);
	for (l=0; l<4; l++) {
		printf("%x ", ((char*)dat)[ l ]);
	}
	putchar('\n');
	return 0;
}
