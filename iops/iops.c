#include"iops.h"

	/* transmit function defined in protocol by 't'. */
int	tx(struct pt *p) {
	return (*(p->proto))(p->p1, p->p2, 't', &(p->dat));
}

	/* recieve function defined in protocol by 'r'. */
int	rx(struct pt *p) {
	return (*(p->proto))(p->p1, p->p2, 'r', &(p->dat));
}

	/* use any other letter for needed functionality. */
int	fx(struct pt *p){
	return (*(p->proto))(p->p1, p->p2, p->cmd, &(p->dat));
}
