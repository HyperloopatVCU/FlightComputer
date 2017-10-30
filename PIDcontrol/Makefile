CC = gcc

OBJS = piddemo.o pidinv.o

DEBUG  =  -g
CFLAGS  =  -Wall -c $(DEBUG)
LFLAGS  =  -Wall $(DEBUG)

piddemo: $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) -o piddemo

piddemo.o : piddemo.c pidinv.h
	$(CC) $(CFLAGS) piddemo.c

.PHONY: clean

clean:
	rm -f *.o *~ piddemo
