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

//! Bus name
char *cfg_bus_name = "tr.org.pardus.comar";

//! Configuration directory
char *cfg_config_dir = CONFIG_DIR;

//! Data directory
char *cfg_data_dir = DATA_DIR;

//! Bus type (system or session)
int cfg_bus_type = DBUS_BUS_SYSTEM;

//! Max idle time to shutdown session service
int cfg_idle_shutdown = 30;

//! Print log messages to console?
int cfg_log_console = 0;

//! Save log messages?
int cfg_log_file = 1;

//! Log file
char *cfg_log_file_name = LOG_FILE;

//! PID file
char *cfg_pid_name = PID_FILE;

//! Log debug flags
int cfg_log_flags = 0;

//! Debug flags
static struct logflag_struct {
    const char *flag;
    int value;
} logflags[] = {
    { "proc", LOG_PROC },
    { "dbus", LOG_DBUS },
    { "perf", LOG_PERF },
    { "policy", LOG_PLCY },
    { "all", LOG_FULL },
    { "full", LOG_FULL },
    { NULL, 0 }
};

//! Command line options
static struct option longopts[] = {
    { "configdir", required_argument, NULL, 'c' },
    { "datadir", required_argument, NULL, 'd' },
    { "debug", required_argument, NULL, 'g' },
    { "idle", required_argument, NULL, 'i' },
    { "print", 0, NULL, 'p' },
    { "type", required_argument, NULL, 't' },
    { "help", 0, NULL, 'h' },
    { "version", 0, NULL, 'v' },
    { NULL, 0, NULL, 0 }
};

//! Short options
static char *shortopts = "c:d:g:i:pt:hv";

//! Help message
static void
print_usage(const char *name)
{
    printf(
        _("Usage: %s [OPTIONS]\n"
        "Pardus configuration manager.\n"
        " -c, --configdir [DIR] Configuration directory.\n"
        "                       (default is %s)\n"
        " -d, --datadir   [DIR] Data storage directory.\n"
        "                       (default is %s)\n"
        " -g, --debug    [FLAG] Set debug flag.\n"
        "                       (Flags: dbus, proc, perf, full)\n"
        " -t, --type     [TYPE] DBus service type (system or session).\n"
        "                       (default is system)\n"
        " -i, --idle     [SECS] Shutdown after [SECS] seconds with no action.\n"
        "                       (Only works with session type, default is %d)\n"
        " -p, --print           Print debug messages to console.\n"
        " -h, --help            Print this text and exit.\n"
        " -v, --version         Print version and exit.\n"
        "Report bugs to http://bugs.pardus.org.tr\n"),
        name,
        cfg_config_dir,
        cfg_data_dir,
        cfg_idle_shutdown
    );
}

//! Version message
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

//! Parses command line options
void
cfg_init(int argc, char *argv[])
{
    /*!
     * Parses command line options and sets cfg_* variables if requested.
     *
     * @argc Number of arguments
     * @argc Array of arguments
     */

    int c, i, j;

    while ((c = getopt_long(argc, argv, shortopts, longopts, &i)) != -1) {
        switch (c) {
            case 'c':
                cfg_config_dir = strdup(optarg);
                break;
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
                cfg_log_file = 0;
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
                print_usage(argv[0]);
                exit(0);
            case 'v':
                print_version();
                exit(0);
            default:
                exit(1);
        }
    }
}
