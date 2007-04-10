/*
** Copyright (c) 2006-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <Python.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

/* per process tracking data */
struct traced_child {
	pid_t pid;
	int proc_mem_fd;
	int need_setup;
	int in_syscall;
	int in_execve;
	unsigned long orig_eax;
	int error_code;
};

/* general tracking data */
struct trace_context {
	PyObject *func;
	PyObject *logger;
	PyObject *retval;
	char **pathlist;
	int network_allowed;
	unsigned int nr_children;
	struct traced_child children[512];
};

char *catbox_paths_canonical(pid_t pid, char *path, int dont_follow);
int path_writable(char **pathlist, pid_t pid, char *path, int dont_follow, int mkdir_case);
void free_pathlist(char **pathlist);
char **make_pathlist(PyObject *paths);

int catbox_retval_init(struct trace_context *ctx);
void catbox_retval_set_exit_code(struct trace_context *ctx, int retcode);
void catbox_retval_add_violation(struct trace_context *ctx, const char *operation, const char *path);

PyObject *catbox_core_run(struct trace_context *ctx);

void catbox_syscall_handle(struct trace_context *ctx, struct traced_child *kid);
