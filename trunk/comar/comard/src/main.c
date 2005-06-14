/*
** Copyright (c) 2005, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "process.h"

void job_start(void);

int
main(int argc, char *argv[])
{
	int i;

	proc_init();

	for (i = 0; i < 16; i++)
		proc_fork(job_start);

	while (1) {
		proc_listen(1);
		puts("tick");
	}

	return 0;
}
