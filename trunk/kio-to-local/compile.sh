g++ -c -I/usr/kde/3.5/include -I/usr/qt/3/include main.cpp
g++ -o kio-to-local -L/usr/kde/3.5/lib -L/usr/qt/3/lib main.o -lkio -lkdecore -lqt-mt
rm -f main.o
