
CC= klcc
EXE= coolplug
OBJS= main.c utility.c module.c devnode.c #scsi.c
INCLUDES= common.h
CFLAGS= -Wall -Os
LDFLAGS= -Wl,-z,noexecstack

$(EXE): $(OBJS) $(INCLUDES)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(EXE) $(OBJS)
	strip -s --remove-section=.note --remove-section=.comment $(EXE)

clean:
	rm -f $(EXE)
