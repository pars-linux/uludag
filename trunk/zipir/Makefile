CC=gcc
CFLAGS=-g -Wall

UNZ_OBJS = zipir.o -lz
TARGETS = zipir

.c.o:
	$(CC) -c $(CFLAGS) $*.c

all: $(TARGETS)

zipir:  $(UNZ_OBJS)
	$(CC) $(CFLAGS) -o $@ $(UNZ_OBJS)

clean:
	rm -f *.o *~ $(TARGETS)
