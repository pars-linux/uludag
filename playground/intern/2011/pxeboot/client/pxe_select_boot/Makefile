CC = gcc
CFLAGS = -g -Wall

LIBCURSES := -lncurses -lmenu
LIBIKSEMEL := -liksemel

TARGETS = selection


all:
	$(CC) selection.c -o $(TARGETS) $(LIBCURSES) $(LIBIKSEMEL)

clean:
	rm -f $(TARGETS)
