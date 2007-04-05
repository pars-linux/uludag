/*
** Copyright (c) 2006-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include "catbox.h"

#include <sys/ptrace.h>
#include <linux/unistd.h>
#include <fcntl.h>
#include <linux/user.h>


static char *
get_str(pid_t pid, unsigned long ptr)
{
	// FIXME: lame function
	char buf1[512];
	static char buf2[5120];
	int i = 0;
	int f;

	sprintf(buf1, "/proc/%ld/mem", pid);
	f = open(buf1, O_RDONLY);
	lseek(f, ptr, 0);
	while (1) {
		read(f, buf2+i, 1);
		if (buf2[i] == '\0')
			break;
		i++;
	}
	close(f);
	return buf2;
}

static int
path_arg_writable(struct trace_context *ctx, pid_t pid, int argno, const char *name, int dont_follow)
{
	unsigned long arg;
	char *path;
	char *path_copy;
	int len;
	int ret;

	arg = ptrace(PTRACE_PEEKUSER, pid, argno * 4, 0);
	path = get_str(pid, arg);
	path_copy = strdup(path);
	len = strlen(path);
	if (path[len-1] == '/') {
		path[len-1] = '\0';
	}
	ret = path_writable(ctx->pathlist, pid, path, dont_follow);
	if (ret == 0) {
		catbox_retval_add_violation(ctx, name, path_copy);
		free(path_copy);
		return 0;
	}
	free(path_copy);

	return 1;
}

#define CHECK_PATH 1    // First argument should be a valid path
#define CHECK_PATH2 2   // Second argument should be a valid path
#define DONT_FOLLOW 4   // Don't follow last symlink in the path while checking
#define LOG_OWNER 8     // Don't do the chown operation but log the new owner
#define LOG_MODE 16     // Don't do the chmod operation but log the new mode
#define FAKE_ID 32      // Fake builder identity as root
#define NET_CALL 64     // System call depends on network allowed flag

static struct syscall_def {
	int no;
	const char *name;
	unsigned int flags;
} system_calls[] = {
	{ __NR_open,       "open",       CHECK_PATH },
	{ __NR_creat,      "creat",      CHECK_PATH },
	{ __NR_truncate,   "truncate",   CHECK_PATH },
	{ __NR_truncate64, "truncate64", CHECK_PATH },
	{ __NR_unlink,     "unlink",     CHECK_PATH | DONT_FOLLOW },
	{ __NR_link,       "link",       CHECK_PATH | CHECK_PATH2 },
	{ __NR_symlink,    "symlink",    CHECK_PATH2 | DONT_FOLLOW },
	{ __NR_rename,     "rename",     CHECK_PATH | CHECK_PATH2 },
	{ __NR_mknod,      "mknod",      CHECK_PATH },
	{ __NR_chmod,      "chmod",      CHECK_PATH | LOG_MODE },
	{ __NR_lchown,     "lchown",     CHECK_PATH | LOG_MODE | DONT_FOLLOW },
	{ __NR_chown,      "chown",      CHECK_PATH | LOG_OWNER },
	{ __NR_lchown32,   "lchown32",   CHECK_PATH | LOG_OWNER | DONT_FOLLOW },
	{ __NR_chown32,    "chown32",    CHECK_PATH | LOG_OWNER },
	{ __NR_mkdir,      "mkdir",      CHECK_PATH },
	{ __NR_rmdir,      "rmdir",      CHECK_PATH },
	{ __NR_mount,      "mount",      CHECK_PATH },
	{ __NR_umount,     "umount",     CHECK_PATH },
	{ __NR_utime,      "utime",      CHECK_PATH },
	{ __NR_getuid,     "getuid",     FAKE_ID },
	{ __NR_getuid32,   "getuid32",   FAKE_ID },
	{ __NR_geteuid,    "geteuid",    FAKE_ID },
	{ __NR_geteuid32,  "geteuid32",  FAKE_ID },
	{ __NR_getgid,     "getgid",     FAKE_ID },
	{ __NR_getgid32,   "getgid32",   FAKE_ID },
	{ __NR_getegid,    "getegid",    FAKE_ID },
	{ __NR_getegid32,  "getegid32",  FAKE_ID },
	{ __NR_socketcall, "socketcall", NET_CALL },
	{ 0, NULL, 0 }
};

static int
handle_syscall(struct trace_context *ctx, pid_t pid, int syscall)
{
	int i;
	unsigned int flags;
	const char *name;
	// exception, we have to check access mode for open
	if (syscall == __NR_open) {
		// open(path, flags, mode)
		flags = ptrace(PTRACE_PEEKUSER, pid, 4, 0);
		if (flags & O_WRONLY || flags & O_RDWR) {
			if (!path_arg_writable(ctx, pid, 0, "open", 0))
				return -1;
		}
		return 0;
	}

	for (i = 0; system_calls[i].name; i++) {
		if (system_calls[i].no == syscall)
			goto found;
	}
	return 0;
found:
	flags = system_calls[i].flags;
	name = system_calls[i].name;

	if (flags & CHECK_PATH) {
		if (!path_arg_writable(ctx, pid, 0, name, flags & DONT_FOLLOW))
			return -1;
	}

	if (flags & CHECK_PATH2) {
		if (!path_arg_writable(ctx, pid, 1, name, flags & DONT_FOLLOW))
			return -1;
	}

	if (flags & NET_CALL && !ctx->network_allowed) {
		catbox_retval_add_violation(ctx, "socketcall", "");
		return -1;
	}

return 0;
    //below we only trap changes to owner/mode within the fishbowl. 
    // The rest are taken care of in the above blocks
    if(0 & LOG_OWNER) {
        struct user_regs_struct regs;
        ptrace(PTRACE_GETREGS, pid, 0, &regs);
        const char* path = get_str(pid, regs.ebx);
        uid_t uid = (uid_t)regs.ecx;
        gid_t gid = (gid_t)regs.edx;
//        PyObject* dict = PyObject_GetAttrString( ctx->ret_object, "ownerships" );
//        PyDict_SetItem( dict, PyString_FromString(path), PyTuple_Pack( 2, PyInt_FromLong(uid), PyInt_FromLong(gid)) );
        return 1;
    }
    if(0 & LOG_MODE) {
        struct user_regs_struct regs;
        ptrace(PTRACE_GETREGS, pid, 0, &regs);
        const char* path = get_str(pid, regs.ebx);
        mode_t mode = (mode_t)regs.ecx;
//        PyObject* dict = PyObject_GetAttrString( ctx->ret_object, "modes" );
//        PyDict_SetItem( dict, PyString_FromString(path), PyInt_FromLong(mode) );
        return 1;
    }
    if(0 & FAKE_ID) {
        return 2;
    }
	return 0;
}

void
catbox_syscall_handle(struct trace_context *ctx, struct traced_child *kid)
{
	int syscall;
	struct user_regs_struct regs;
	pid_t pid;

	pid = kid->pid;
	ptrace(PTRACE_GETREGS, pid, 0, &regs);
	syscall = regs.orig_eax;

	if (kid->in_syscall) {
		if (syscall == 0xbadca11) {
			ptrace(PTRACE_POKEUSER, pid, 44, kid->orig_eax);
			if (kid->orig_eax == __NR_mkdir) {
				ptrace(PTRACE_POKEUSER, pid, 24, -EEXIST);
			} else {
				ptrace(PTRACE_POKEUSER, pid, 24, -EACCES);
			}
		}
		kid->in_syscall = 0;
	} else {
		int ret = handle_syscall(ctx, pid, syscall);
		if (ret != 0) {
			kid->orig_eax = regs.orig_eax;
			ptrace(PTRACE_POKEUSER, pid, 44, 0xbadca11);
		}
		kid->in_syscall = 1;
	}

	ptrace(PTRACE_SYSCALL, pid, 0, 0);
}
