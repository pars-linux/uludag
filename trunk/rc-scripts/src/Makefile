# Copyright © 2005  TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# Original work belongs Gentoo Linux

CC = gcc
LD = gcc

CFLAGS = -Wall -O2
DESTDIR =

BIN_TARGETS =
SBIN_TARGETS = start-stop-daemon start_unicode

TARGET = $(BIN_TARGETS) $(SBIN_TARGETS)

all: $(TARGET)

start-stop-daemon: start-stop-daemon.c
	$(CC) -o $@ $(CFLAGS) -DHAVE_ERROR_H -DHAVE_TIOCNOTTY -DHAVE_SETSID $^

start_unicode: start_unicode.c
	$(CC) -o $@ $(CFLAGS) $^

install: $(TARGET)
	install -m 0755 -d $(DESTDIR)/bin
	install -m 0755 -d $(DESTDIR)/sbin
	install -m 0755 $(SBIN_TARGETS) $(DESTDIR)/sbin

clean:
	rm -f $(TARGET)
	rm -f *.o *~ core
