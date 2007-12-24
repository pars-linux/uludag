TARGET = qt3.so
OFILES = mainloop.o moc_mainloop.o
HFILES =  mainloop.h

CXX = g++
LINK = g++
CPPFLAGS = -I. -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/python2.4 -DQT_SHARED -DQT_TABLET_SUPPORT -DQT_NO_DEBUG -DQT_THREAD_SUPPORT -D_REENTRANT -I/usr/qt/3/include
CFLAGS = -pipe -fPIC -O2 -Wall -W -D_REENTRANT
CXXFLAGS = -pipe -fPIC -O2 -Wall -W -D_REENTRANT
LFLAGS = -shared -Wl,-rpath,/usr/qt/3/lib -Wl,--version-script=qt.exp
LIBS = -L/usr/qt/3/lib -L/usr/X11R6/lib -ldbus-1 -lqt-mt -lmng -ljpeg -lpng -lz -lXi -lXrender -lXrandr -lXcursor -lXinerama -lXft -lfreetype -lfontconfig -lXext -lX11 -lm -lSM -lICE -ldl -lpthread
MOC = /usr/qt/3/bin/moc
.SUFFIXES: .c .o .cpp .cc .cxx .C

.cpp.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.cc.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.cxx.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

.C.o:
	$(CXX) -c $(CXXFLAGS) $(CPPFLAGS) -o $@ $<

$(TARGET): $(OFILES)
	@echo '{ global: initqt3; local: *; };' > qt.exp
	$(LINK) $(LFLAGS) -o $(TARGET) $(OFILES) $(LIBS)

$(OFILES): $(HFILES)

moc_mainloop.cpp: mainloop.h
	$(MOC) -o moc_mainloop.cpp mainloop.h

install: $(TARGET)
	@test -d $(DESTDIR)/usr/lib/python2.4/site-packages/dbus/mainloop || mkdir -p $(DESTDIR)/usr/lib/python2.4/site-packages/dbus/mainloop
	cp -f $(TARGET) $(DESTDIR)/usr/lib/python2.4/site-packages/dbus/mainloop/$(TARGET)
	strip $(DESTDIR)/usr/lib/python2.4/site-packages/dbus/mainloop/$(TARGET)

clean:
	-rm -f $(TARGET)
	-rm -f *.o
	-rm -f moc_mainloop.cpp
	-rm -f qt.exp
