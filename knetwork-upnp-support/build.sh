g++ -c -I/usr/kde/3.5/include -I/usr/qt/3/include -DQT_THREAD_SUPPORT upnpdiscover.cpp
g++ -c -I/usr/kde/3.5/include -I/usr/qt/3/include kupnp.cpp
g++ -c -I/usr/kde/3.5/include -I/usr/qt/3/include main.cpp
g++ -o upnp_test main.o kupnp.o -L/usr/kde/3.5/lib -L/usr/qt/3/lib -lkdecore -lqt-mt
