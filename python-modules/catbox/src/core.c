/*
** Copyright (c) 2006-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include "catbox.h"

#include <sys/wait.h>
#include <sys/types.h>
#include <sys/ptrace.h>
#include <linux/ptrace.h>
#include <linux/user.h>
#include <linux/unistd.h>
#include <fcntl.h>
#include <errno.h>









/*
    Setup the catbox kid with the right options
*/
static int
setup_kid(pid_t pid)
{
	int e;
    //trace clones, forks, vforks (i.e., all kids)
	e = ptrace(PTRACE_SETOPTIONS, pid, 0,
		PTRACE_O_TRACESYSGOOD | PTRACE_O_TRACECLONE |PTRACE_O_TRACEFORK | PTRACE_O_TRACEVFORK);
	if (e != 0)
	printf("ptrace opts error %s\n",strerror(errno));
}








/*------------------------------------------------------*/

/*
    child management
*/

static void
add_child(struct trace_context *ctx, pid_t pid)
{
	struct traced_child *kid;

	kid = &ctx->children[ctx->nr_children++];
	memset(kid, 0, sizeof(struct traced_child));
	kid->pid = pid;
	kid->need_setup = 1;
}

static struct traced_child *
find_child(struct trace_context *ctx, pid_t pid)
{
	int i;

	for (i = 0; i < ctx->nr_children; i++) {
		if (ctx->children[i].pid == pid)
			return &ctx->children[i];
	}
	return NULL;
}

static void
rem_child(struct trace_context *ctx, pid_t pid)
{
	int i;

	for (i = 0; i < ctx->nr_children; i++) {
		if (ctx->children[i].pid == pid)
			goto do_rem;
	}
	puts("bjorkbjork");
do_rem:
	ctx->nr_children -= 1;
	ctx->children[i] = ctx->children[ctx->nr_children];
}

/*------------------------------------------------------*/




static PyObject *
core_trace_loop(struct trace_context *ctx, pid_t pid)
{
	int status;
	unsigned int event;
	long retcode = 0;
	struct traced_child *kid;

	// First one is the process we are tracing
	add_child(ctx, pid);
	// and it is already set up
	ctx->children[0].need_setup = 0;

	while (ctx->nr_children) {
		pid = wait(&status);
		if (pid == (pid_t) -1) return NULL;
		kid = find_child(ctx, pid);
		if (!kid) { puts("borkbork"); continue; }

		if (WIFSTOPPED(status)) {
			int stopsig = WSTOPSIG(status);
			if (stopsig == SIGSTOP && kid->need_setup) {
				setup_kid(pid);
				kid->need_setup = 0;
				ptrace(PTRACE_SYSCALL, pid, 0, 0);
				continue;
			}
			if (stopsig & SIGTRAP) {
				if (stopsig == (SIGTRAP | 0x80)) {
					catbox_syscall_handle(ctx, kid);
					continue;
				}
				event = (status >> 16) & 0xffff;
				if (event == PTRACE_EVENT_FORK
				    || event == PTRACE_EVENT_VFORK
				    || event == PTRACE_EVENT_CLONE) {
					pid_t kpid;
					int e;
					e = ptrace(PTRACE_GETEVENTMSG, pid, 0, &kpid); //get the new kid's pid
					if (e != 0) printf("geteventmsg %s\n", strerror(e));
					add_child(ctx, kpid);  //add the new kid (setup will be done later)
				}
				if (kid->in_execve) {
					kid->in_execve = 0;
					ptrace(PTRACE_SYSCALL, pid, 0, 0);
					continue;
				}
			}
			ptrace(PTRACE_SYSCALL, pid, 0, (void*) stopsig);
		} else if (WIFEXITED(status)) {
			if (kid == &ctx->children[0]) { //if it is our first child
				// keep ret value
				retcode = WEXITSTATUS(status);
			}
			rem_child(ctx, pid);
		} else if (WIFSIGNALED(status)) {
printf("xxxxxxxxxSignal %x pid %d\n", status, pid);
			ptrace(PTRACE_SYSCALL, pid, 0, (void*) WTERMSIG(status));
		} else {
printf("xxxxxxxxxSignal %x pid %d\n", status, pid);
		}
	}

	catbox_retval_set_exit_code(ctx, retcode);
	return ctx->retval;
}

static int got_sig = 0;

static void sigusr1(int dummy) {
	got_sig = 1;
}

PyObject *
catbox_core_run(struct trace_context *ctx)
{
	void (*oldsig)(int);
	pid_t pid;

	got_sig = 0;
	oldsig = signal(SIGUSR1, sigusr1);

	pid = fork();
	if (pid == (pid_t) -1) {
		PyErr_SetString(PyExc_RuntimeError, "fork failed");
		return NULL;
	}

	if (pid == 0) {
		// child process
		PyObject *ret;
		ptrace(PTRACE_TRACEME, 0, 0, 0);
		kill(getppid(), SIGUSR1); //send a signal to parent
		while (!got_sig) ; //wait for confirmation

		ret = PyObject_Call(ctx->func, PyTuple_New(0), NULL); //run the callable
        
		if (!ret) { //handle exception
			PyObject *e;
			PyObject *val;
			PyObject *tb;
			PyErr_Fetch(&e, &val, &tb);
			if (PyErr_GivenExceptionMatches(e, PyExc_SystemExit)) {
				// extract exit code
				if (PyInt_Check(val))
					exit(PyInt_AsLong(val));
				else
					exit(2);
			}
			// error
			exit(1);
		}
		exit(0);
	}

	// parent process
	while (!got_sig) ; //wait for the signal from child
	kill(pid, SIGUSR1); //send a confirmation
	waitpid(pid, NULL, 0); // ??

	setup_kid(pid);
	ptrace(PTRACE_SYSCALL, pid, 0, (void *) SIGUSR1);

	return core_trace_loop(ctx, pid);
}
