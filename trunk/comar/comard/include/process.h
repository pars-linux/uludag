/*
** Copyright (c) 2005, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#ifndef PROCESS_H
#define PROCESS_H 1

struct ProcChild {
	int from;
	int to;
	pid_t pid;
};

struct Proc {
	// parent info
	struct ProcChild parent;
	// children info
	int nr_children;
	int max_children;
	struct ProcChild *children;
};

// per process global variable
extern struct Proc my_proc;

// for readability of send_cmd/data functions
#define TO_PARENT NULL

void proc_init(void);
struct ProcChild *proc_fork(void (*child_func)(void));
int proc_listen(struct ProcChild **senderp, int *cmdp, size_t *sizep, int timeout);
int proc_send(struct ProcChild *p, int cmd, const void *data, size_t data_size);
int proc_recv(struct ProcChild *p, void **datap, size_t size);
int proc_recv_to(struct ProcChild *p, void *data, size_t size);


#endif /* PROCESS_H */
