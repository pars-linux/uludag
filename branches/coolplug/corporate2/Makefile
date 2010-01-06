CC= dietlibc-gcc
EXE= coolplug
OBJS= main.c utility.c module.c devnode.c
INCLUDES= common.h
CFLAGS= -Wall -O2
LDFLAGS= -Wl,-z,noexecstack

$(EXE): $(OBJS) $(INCLUDES)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(EXE) $(OBJS)
	strip -s --remove-section=.note --remove-section=.comment $(EXE)

clean:
	rm -f $(EXE)
