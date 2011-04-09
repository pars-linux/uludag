CC=g++

CFLAGS=-c -Wall

all: hello

hello: main.o factorial.o hello.o
		$(CC) main.o factorial.o hello.o -o hello

main.o: main.cpp
		$(CC) $(CFLAGS) main.cpp

factorial.o: factorial.cpp
		$(CC) $(CFLAGS) factorial.cpp

hello.o: hello.cpp
		$(CC) $(CFLAGS) hello.cpp

clean:
		rm -rf *o hello


