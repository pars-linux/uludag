CC = gcc
CFLAGS = -g -Wall

LIBCURSES := -lncurses -lmenu

TARGETS = pxebootselect

all:
	$(CC) $(CFLAGS) `xml2-config --cflags` pxebootselect.c -o $(TARGETS) $(LIBCURSES) `xml2-config --libs`

clean:
	rm -f $(TARGETS)

test:
	./$(TARGETS) version.xml


