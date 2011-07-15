CC = gcc
CFLAGS = -g -Wall

LIBCURSES := -lncurses -lmenu

TARGETS = pxebootselect

all:
	$(CC) `pkg-config libxml-2.0 --cflags --libs` pxebootselect.c -o $(TARGETS) $(LIBCURSES)

clean:
	rm -f $(TARGETS)

test:
	./$(TARGETS) version.xml


