
all: test

.PHONY: test

test: test_comarrpc.cpp
	g++ -I${KDEDIR}/include/ -I${QTDIR}/include -L${KDEDIR}/lib -L${QTDIR}/lib -lcomarrpc -o test test_comarrpc.cpp
