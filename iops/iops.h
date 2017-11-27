#ifndef IOPS_H
#define IOPS_H

#include<stdint.h>

typedef struct pt {
	uint8_t		p1;	/* pin1 number. */
	uint8_t		p2;	/* pin2 number. */
	char		cmd;	/* proto command. */
	uint64_t	dat;	/* outgoing/receving data. */
			/* serial protocol ptr. */
	int		(*proto)(uint8_t, uint8_t, char, uint64_t*);
} port;

extern int	tx(port*);
extern int	rx(port*);
extern int	fx(port*);

#endif
