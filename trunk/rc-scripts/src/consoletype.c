/*
 * consoletype.c
 * simple app to figure out whether the current terminal
 * is serial, console (vt), or remote (pty).
 * Copyright © 2005  TUBITAK/UEKAE
 * Licensed under the GNU General Public License, version 2.
 * See the file http://www.gnu.org/copyleft/gpl.txt.
 *
 * Original work belongs Gentoo Linux
 *
 */

#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sys/sysmacros.h>

int main(int argc, char *argv[])
{
	unsigned char twelve = 12;
	int maj;
	struct stat sb;

	fstat(0, &sb);
	maj = major(sb.st_rdev);
	if (maj != 3 && (maj < 136 || maj > 143)) {
		if (ioctl (0, TIOCLINUX, &twelve) < 0) {
			printf("serial\n");
			return 1;
		} else {
			printf("vt\n");
			return 0;
		}
	} else {
		printf("pty\n");
		return 2;
	}
}
