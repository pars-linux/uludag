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

#include "cfg.h"
#include "process.h"
#include "model.h"
#include "data.h"
#include "job.h"
#include "rpc.h"

int
main(int argc, char *argv[])
{
	struct ProcChild *p, *rpc;
	struct ipc_data *ipc;
	int cmd;
	int size;

	cfg_init(argc, argv);

	if (db_init() != 0) return 1;
	proc_init();
	if (model_init() != 0) return 1;

	rpc = proc_fork(rpc_unix_start);

	while (1) {
		if (1 == proc_listen(&p, &cmd, &size, 1)) {
			switch (cmd) {
				case CMD_REGISTER:
				case CMD_REMOVE:
				case CMD_CALL:
					proc_recv(p, &ipc, size);
					job_start(cmd, ipc, size);
					free(ipc);
					break;
			}
		}
//		puts("tick");
	}

	return 0;
}
