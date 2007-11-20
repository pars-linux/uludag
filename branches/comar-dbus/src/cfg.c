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
#include <string.h>
#include <getopt.h>
#include <dbus/dbus.h>

#include "cfg.h"
#include "i18n.h"
#include "log.h"
#include "utility.h"

// Global options
char *cfg_bus_name = "tr.org.pardus.comar";
char *cfg_data_dir = "/var/db/comar";
int cfg_bus_type = DBUS_BUS_SYSTEM;
int cfg_idle_shutdown = 30;
int cfg_log_console = 0;
int cfg_log_file = 1;
char *cfg_log_file_name = "/var/log/comar.log";
int cfg_log_flags = 0;

// Log flags
static struct logflag_struct {
    const char *flag;
    int value;
} logflags[] = {
    { "proc", LOG_PROC },
    { "db", LOG_DB },
    { "job", LOG_JOB },
    { "perf", LOG_PERF },
    { "all", LOG_ALL },
    { "full", LOG_ALL },
    { NULL, 0 }
};

// Command line options
static struct option longopts[] = {
    { "datadir", required_argument, NULL, 'd' },
    { "debug", required_argument, NULL, 'g' },
    { "idle", required_argument, NULL, 'i' },
    { "print", 0, NULL, 'p' },
    { "type", required_argument, NULL, 't' },
    { "help", 0, NULL, 'h' },
    { "version", 0, NULL, 'v' },
    { NULL, 0, NULL, 0 }
};

static char *shortopts = "d:g:i:pt:hv";

// Help message
static void
print_usage(void)
{
    printf(
        _("Usage: comar [OPTIONS]\n"
        "Pardus configuration manager.\n"
        " -d, --datadir [DIR] Data storage directory.\n"
        "                     (default is %s)\n"
        " -g, --debug [FLAGS] Enable debug output.\n"
        " -t, --type   [TYPE] DBus service type (system or session).\n"
        "                     (default is system)\n"
        " -i, --idle   [SECS] Shutdown after [SECS] seconds with no action.\n"
        "                     (Only works with session type, default is %d)\n"
        " -p, --print         Print debug messages to console.\n"
        " -h, --help          Print this text and exit.\n"
        " -v, --version       Print version and exit.\n"
        "Report bugs to http://bugs.pardus.org.tr\n"),
        cfg_data_dir,
        cfg_idle_shutdown
    );
}

// Version
static void
print_version(void)
{
    printf(
        _("COMAR %s\n"
        "Copyright (c) 2005-2007, TUBITAK/UEKAE\n"
        "This program is free software; you can redistribute it and/or modify it\n"
        "under the terms of the GNU General Public License as published by the\n"
        "Free Software Foundation; either version 2 of the License, or (at your\n"
        "option) any later version.\n"),
        VERSION
    );
}

// Parse command line options
void
cfg_init(int argc, char *argv[])
{
    int c, i, j;

    while ((c = getopt_long(argc, argv, shortopts, longopts, &i)) != -1) {
        switch (c) {
            case 'd':
                cfg_data_dir = strdup(optarg);
                break;
            case 'g':
                for (j = 0; logflags[j].flag; ++j) {
                    if (strstr(optarg, logflags[j].flag))
                        cfg_log_flags |= logflags[j].value;
                }
                break;
            case 'i':
                cfg_idle_shutdown = strtol(optarg, NULL, 0);
                if (cfg_idle_shutdown == 0) {
                    cfg_idle_shutdown = 30;
                }
                break;
            case 'p':
                cfg_log_console = 1;
                break;
            case 't':
                if (strcmp(optarg, "session") == 0) {
                    cfg_bus_type = DBUS_BUS_SESSION;
                }
                else {
                    cfg_bus_type = DBUS_BUS_SYSTEM;
                }
                break;
            case 'h':
                print_usage();
                exit(0);
            case 'v':
                print_version();
                exit(0);
            default:
                exit(1);
        }
    }
}
