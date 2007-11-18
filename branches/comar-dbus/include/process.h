/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <dbus/dbus.h>

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

extern struct Proc my_proc;
extern int shutdown_activated;

void proc_init(int argc, char *argv[], const char *name);
int proc_listen(struct ProcChild **senderp, size_t *sizep, int timeout);
void proc_check_shutdown(void);
struct ProcChild *proc_fork(void (*child_func)(void), const char *desc);
struct ProcChild *proc_dbus_call(void (*msg_func)(DBusMessage*, DBusConnection*), DBusMessage *msg, DBusConnection *conn, const char *desc);
void proc_finish(void);
