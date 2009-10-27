main: core.o enroll.o image.o verify.o
	gcc -g -lfprint -Wall core.o enroll.o image.o verify.o -o pyfinger

core.o: core.c
	gcc -g -Wall -c core.c

enroll.o: enroll.c
	gcc -g -Wall -c enroll.c

image.o: image.c
	gcc -g -Wall -c image.c

verify.o: verify.c
	gcc -g -Wall -c verify.c

clean:
	@rm -f *.o &> /dev/null
	@rm -f pyfinger &>/dev/null
