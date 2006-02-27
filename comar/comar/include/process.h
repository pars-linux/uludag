/*
** Copyright (c) 2005-2006, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#ifndef PROCESS_H
#define PROCESS_H 1

#include "utility.h"

struct ProcChild {
	int from;
	int to;
	pid_t pid;
	const char *desc;
};

struct Proc {
	// parent info
	struct ProcChild parent;
	const char *desc;
	// children info
	int nr_children;
	int max_children;
	struct ProcChild *children;
};

struct ipc_source {
	void *chan;
	int id;
};

struct ipc_struct {
	struct ipc_source source;
	int node;
};

// per process global variable
extern struct Proc my_proc;

// for readability of send_cmd/data functions
#define TO_PARENT NULL

// ipc commands
enum {
	CMD_FINISH = 0,
	CMD_RESULT,
	CMD_RESULT_START,
	CMD_RESULT_END,
	CMD_FAIL,
	CMD_NONE,
	CMD_ERROR,
	CMD_REGISTER,
	CMD_REMOVE,
	CMD_CALL,
	CMD_CALL_PACKAGE,
	CMD_GETLIST,
	CMD_NOTIFY,
	CMD_DUMP_PROFILE,
	CMD_SHUTDOWN,
	CMD_EVENT
};

// functions
void proc_init(int argc, char *argv[]);
struct ProcChild *proc_get_rpc(void);

struct ProcChild *proc_fork(void (*child_func)(void), const char *desc);
void proc_check_shutdown(void);
void proc_finish(void);

int proc_listen(struct ProcChild **senderp, int *cmdp, size_t *sizep, int timeout);
int proc_put(struct ProcChild *p, int cmd, struct ipc_struct *ipc, struct pack *pak);
int proc_get(struct ProcChild *p, struct ipc_struct *ipc, struct pack *pak, size_t size);


#endif /* PROCESS_H */
