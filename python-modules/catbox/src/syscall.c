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
	int ret;

	arg = ptrace(PTRACE_PEEKUSER, pid, argno * 4, 0);
	path = get_str(pid, arg);
	ret = path_writable(ctx->pathlist, pid, path, dont_follow);
	if (ret == 0) {
		catbox_retval_add_violation(ctx, name, path);
		return 0;
	}

	return 1;
}

#define CHECK_PATH 1
#define CHECK_PATH2 2
#define LOG_OWNER 4
#define LOG_MODE 8
#define FAKE_ID 16
#define DONT_FOLLOW 32

// TRAP_xxxxx check for remode operations
// xxown(): get the real uid/gid, store path and replace with process uid/gid
// xxmod(): get the real mode
// xxid(): return uid=0, gid=0
#define TRAP_xxOWN 4
#define TRAP_xxMOD 8
#define TRAP_xxID  16

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
	{ __NR_symlink,    "symlink",    CHECK_PATH2 },
	{ __NR_rename,     "rename",     CHECK_PATH | CHECK_PATH2 },
	{ __NR_mknod,      "mknod",      CHECK_PATH },
	{ __NR_chmod,      "chmod",      CHECK_PATH | TRAP_xxMOD },
	{ __NR_lchown,     "lchown",     CHECK_PATH | TRAP_xxOWN | DONT_FOLLOW },
	{ __NR_chown,      "chown",      CHECK_PATH | TRAP_xxOWN },
	{ __NR_lchown32,   "lchown32",   CHECK_PATH | TRAP_xxOWN | DONT_FOLLOW },
	{ __NR_chown32,    "chown32",    CHECK_PATH | TRAP_xxOWN },
	{ __NR_mkdir,      "mkdir",      CHECK_PATH },
	{ __NR_rmdir,      "rmdir",      CHECK_PATH },
	{ __NR_mount,      "mount",      CHECK_PATH },
	{ __NR_umount,     "umount",     CHECK_PATH },
	{ __NR_utime,      "utime",      CHECK_PATH },
	{ __NR_getuid,     "getuid",     TRAP_xxID },
	{ __NR_getuid32,   "getuid32",   TRAP_xxID },
	{ __NR_geteuid,    "geteuid",    TRAP_xxID },
	{ __NR_geteuid32,  "geteuid32",  TRAP_xxID },
	{ __NR_getgid,     "getgid",     TRAP_xxID },
	{ __NR_getgid32,   "getgid32",   TRAP_xxID },
	{ __NR_getegid,    "getegid",    TRAP_xxID },
	{ __NR_getegid32,  "getegid32",  TRAP_xxID },
	{ 0, NULL, 0 }
};

int
before_syscall(struct trace_context *ctx, pid_t pid, int syscall)
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

    //below we only trap changes to owner/mode within the fishbowl. 
    // The rest are taken care of in the above blocks
    if(0 & TRAP_xxOWN) {
        struct user_regs_struct regs;
        ptrace(PTRACE_GETREGS, pid, 0, &regs);
        const char* path = get_str(pid, regs.ebx);
        uid_t uid = (uid_t)regs.ecx;
        gid_t gid = (gid_t)regs.edx;
//        PyObject* dict = PyObject_GetAttrString( ctx->ret_object, "ownerships" );
//        PyDict_SetItem( dict, PyString_FromString(path), PyTuple_Pack( 2, PyInt_FromLong(uid), PyInt_FromLong(gid)) );
        return 1;
    }
    if(0 & TRAP_xxMOD) {
        struct user_regs_struct regs;
        ptrace(PTRACE_GETREGS, pid, 0, &regs);
        const char* path = get_str(pid, regs.ebx);
        mode_t mode = (mode_t)regs.ecx;
//        PyObject* dict = PyObject_GetAttrString( ctx->ret_object, "modes" );
//        PyDict_SetItem( dict, PyString_FromString(path), PyInt_FromLong(mode) );
        return 1;
    }
    if(0 & TRAP_xxID) {
        return 2;
    }
	return 0;
}
