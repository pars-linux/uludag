CFLAGS=-Wall
CC=gcc $(CFLAGS)

GLIB_FLAGS=`pkg-config --cflags glib-2.0` 
GLIB_LIBS=`pkg-config --libs glib-2.0`

XML_FLAGS=`pkg-config --cflags libxslt`
XML_LIBS=`pkg-config --libs libxslt`


all: ulu.web

strip: ulu.web
	strip $<

ulu.web: scgi.o main.o
	$(CC) $(XML_LIBS) $(GLIB_LIBS) $? -o $@

scgi.o: scgi.c scgi.h
	$(CC) -c $(GLIB_FLAGS) $<

main.o: main.c
	$(CC) -c $(XML_FLAGS) $(GLIB_FLAGS) $<

.PHONY: clean

clean: 
	rm -f *.o ulu.web
