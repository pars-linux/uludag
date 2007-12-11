/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/time.h>
#include <fcntl.h>
#include <dbus/dbus.h>
#include <time.h>

#include "cfg.h"
#include "log.h"
#include "process.h"

struct Proc my_proc;
int shutdown_activated = 0;
static char *name_addr;
static size_t name_size;
static time_t time_lastaction = 0;

static void
handle_sigterm(int signum)
{
    shutdown_activated = 1;
}

static void
handle_signals(void)
{
    struct sigaction act;
    struct sigaction ign;

    act.sa_handler = handle_sigterm;
    /*! initialize and empty a signal set. Signals are to be blocked while executing handle_sigterm */
    sigemptyset(&act.sa_mask);
    act.sa_flags = 0; /*!< special flags */

    ign.sa_handler = SIG_IGN;
    sigemptyset(&ign.sa_mask);
    ign.sa_flags = 0;

    sigaction(SIGTERM, &act, NULL);
    sigaction(SIGINT, &act, NULL);
    sigaction(SIGPIPE, &ign, NULL);
}

static void
set_my_name(const char *name)
{
    if (strlen(name) + 1 < name_size) {
        memset(name_addr, 0, name_size);
        strcpy(name_addr, name);
    }
}

int
proc_check_idle()
{
    if (cfg_bus_type == DBUS_BUS_SYSTEM) {
        return 0;
    }
    if (my_proc.nr_children == 0 && time_lastaction != 0 && difftime(time(0), time_lastaction) > cfg_idle_shutdown) {
        return 1;
    }
    return 0;
}

void
proc_init(int argc, char *argv[], const char *name)
{
    int i;

    name_addr = argv[0];
    name_size = 0;
    for (i = 0; i < argc; i++) {
        name_size += strlen(argv[i]) + 1;
    }

    memset(&my_proc, 0, sizeof(struct Proc));
    my_proc.parent.to = -1;
    my_proc.parent.from = -1;
    my_proc.desc = name;
    my_proc.max_children = 8;
    my_proc.children = calloc(8, sizeof(struct ProcChild));
    handle_signals();
    set_my_name(my_proc.desc);
    time_lastaction = time(0);
}

static struct ProcChild *
add_child(pid_t pid, int to, int from, const char *desc, DBusMessage *bus_msg)
{
    int i;

    i = my_proc.nr_children;
    if (i >= my_proc.max_children) {
        if (i == 0) {
            my_proc.max_children = 4;
        } else {
            my_proc.max_children *= 2;
        }
        my_proc.children = realloc(my_proc.children,
            my_proc.max_children * sizeof(struct ProcChild)
        );
    }
    memset(&my_proc.children[i], 0, sizeof(struct ProcChild));
    my_proc.children[i].from = from;
    my_proc.children[i].to = to;
    my_proc.children[i].pid = pid;
    my_proc.children[i].desc = desc;
    my_proc.children[i].bus_msg = bus_msg;
    ++my_proc.nr_children;
    return &my_proc.children[i];
}

static void
rem_child(int nr)
{
    int status;
    waitpid(my_proc.children[nr].pid, &status, 0);
    close(my_proc.children[nr].to);
    close(my_proc.children[nr].from);
    time_lastaction = time(0);
    if (my_proc.children[nr].bus_msg != NULL) {
        dbus_message_unref(my_proc.children[nr].bus_msg);
    }
    --my_proc.nr_children;
    if (0 == my_proc.nr_children) return;
    (my_proc.children)[nr] = (my_proc.children)[my_proc.nr_children];
}

static void
stop_children(void)
{
    struct timeval start;
    struct timeval cur;
    struct timeval tv;
    unsigned long msec;
    fd_set fds;
    int i, sock, max;
    int len;
    char tmp[100];

    // hey kiddo, finish your homework and go to bed
    for (i = 0; i < my_proc.nr_children; i++) {
        kill(my_proc.children[i].pid, SIGTERM);
    }

    gettimeofday(&start, NULL);
    msec = 0;

    while (my_proc.nr_children && msec < 3000) {
        // 1/5 second precision for the 3 second maximum shutdown time
        tv.tv_sec = 0;
        tv.tv_usec = 200000;
        max = 0;
        FD_ZERO(&fds);
        for (i = 0; i < my_proc.nr_children; i++) {
            sock = my_proc.children[i].from;
            FD_SET(sock, &fds);
            if (sock > max) max = sock;
        }
        ++max;

        if (select(max, &fds, NULL, NULL, &tv) > 0) {
            for (i = 0; i < my_proc.nr_children; i++) {
                sock = my_proc.children[i].from;
                if (FD_ISSET(sock, &fds)) {
                    len = read(sock, &tmp, sizeof(tmp));
                    if (0 == len) {
                        rem_child(i);
                    }
                }
            }
        }

        gettimeofday(&cur, NULL);
        msec = (cur.tv_sec * 1000) + (cur.tv_usec / 1000);
        msec -= (start.tv_sec * 1000) + (start.tv_usec / 1000);
    }

    // sorry kids, play time is over
    for (i = 0; i < my_proc.nr_children; i++) {
        kill(my_proc.children[i].pid, SIGKILL);
    }
}

void
proc_finish(void)
{
    if (my_proc.nr_children) stop_children();
    log_debug(LOG_PROC, "%s process %d ended\n", my_proc.desc, getpid());
    exit(0);
}

void
proc_check_shutdown(void)
{
    if (shutdown_activated) {
        if (my_proc.parent.from != -1)
            proc_finish();
    }
}

struct ProcChild *
proc_fork(void (*child_func)(void), const char *desc, DBusConnection *bus_conn, DBusMessage *bus_msg)
{
    pid_t pid;
    int fdr[2], fdw[2];
    int i;

    pipe(fdr);
    pipe(fdw);
    pid = fork();
    if (pid == -1) return NULL;

    if (pid == 0) {
        // new child process starts
        // we have to close unneeded pipes inherited from the parent
        if (my_proc.parent.to != -1) close(my_proc.parent.to);
        if (my_proc.parent.from != -1) close(my_proc.parent.from);
        for (i = 0; i < my_proc.nr_children; i++) {
            close(my_proc.children[i].to);
            close(my_proc.children[i].from);
        }
        close(fdw[1]);
        close(fdr[0]);
        // stop parent's pipes from propagating through an exec()
        fcntl(fdw[0], F_SETFD, FD_CLOEXEC);
        fcntl(fdr[1], F_SETFD, FD_CLOEXEC);
        // now setup our own data
        memset(&my_proc, 0, sizeof(struct Proc));
        my_proc.parent.from = fdw[0];
        my_proc.parent.to = fdr[1];
        my_proc.parent.pid = getppid();
        my_proc.desc = desc;
        my_proc.bus_conn = bus_conn;
        my_proc.bus_msg = bus_msg;
        handle_signals();
        set_my_name(desc);
        log_debug(LOG_PROC, "%s process %d started\n", desc, getpid());
        // finally jump to the real function
        child_func();
        proc_finish();
        while (1) {} // to keep gcc happy
    } else {
        // parent process continues
        close(fdw[0]);
        close(fdr[1]);
        return add_child(pid, fdw[1], fdr[0], desc, bus_msg);
    }
}

static int
proc_setup_fds(fd_set *fds)
{
    int sock;
    int i;
    int max = 0;

    proc_check_shutdown();

    FD_ZERO(fds);
    sock = my_proc.parent.from;
    if (sock != -1) {
        // we have a parent to listen for
        FD_SET(sock, fds);
        if (sock > max) max = sock;
    }
    // and some children maybe?
    for (i = 0; i < my_proc.nr_children; i++) {
        sock = my_proc.children[i].from;
        FD_SET(sock, fds);
        if (sock > max) max = sock;
    }

    return ++max;
}

static int
proc_select_fds(fd_set *fds, int max, struct ProcChild **senderp, size_t *sizep, int timeout_sec, int timeout_usec)
{
    unsigned int ipc;
    struct timeval tv, *tvptr;
    int sock;
    int len;
    int i;

    tv.tv_sec = timeout_sec;
    tv.tv_usec = timeout_usec;
    if (timeout_sec != -1) tvptr = &tv; else tvptr = NULL;

    if (select(max, fds, NULL, NULL, tvptr) > 0) {
        sock = my_proc.parent.from;
        if (sock != -1 && FD_ISSET(sock, fds)) {
            len = read(sock, &ipc, sizeof(ipc));
            if (0 == len) {
                // parent process left us
                // tell me that there is something worth living for tonight
                log_debug(LOG_PROC, "Parent left %s process %d\n", my_proc.desc, getpid());
                proc_finish();
            }
            *senderp = &my_proc.parent;
            *sizep = (ipc & 0x00FFFFFF);
            return 1;
        }
        for (i = 0; i < my_proc.nr_children; i++) {
            sock = my_proc.children[i].from;
            if (FD_ISSET(sock, fds)) {
                len = read(sock, &ipc, sizeof(ipc));
                if (len == sizeof(ipc)) {
                    *senderp = &my_proc.children[i];
                    *sizep = (ipc & 0x00FFFFFF);
                    return 1;
                } else {
                    rem_child(i);
                    *senderp = NULL;
                    *sizep = 0;
                    return 1;
                }
            }
        }
        *senderp = NULL;
        *sizep = 0;
        return 1;
    }
    return 0;
}

int
proc_listen(struct ProcChild **senderp, size_t *sizep, int timeout_sec, int timeout_usec)
{
    fd_set fds;
    int max;

    max = proc_setup_fds(&fds);

    return proc_select_fds(&fds, max, senderp, sizep, timeout_sec, timeout_usec);
}
