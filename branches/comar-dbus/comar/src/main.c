/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdlib.h>
#include <sys/time.h>
#include <dbus/dbus.h>

#include "cfg.h"
#include "data.h"
#include "dbus.h"
#include "i18n.h"
#include "log.h"
#include "model.h"
#include "process.h"

int
main(int argc, char *argv[])
{
    struct ProcChild *p;
    int size;

    // l10n
    setlocale(LC_MESSAGES, "");
    bindtextdomain("comar", "/usr/share/locale");
    bind_textdomain_codeset("comar", "UTF-8");
    bind_textdomain_codeset("libc", "UTF-8");
    textdomain("comar");

    // Parse commandline options
    cfg_init(argc, argv);

    // Only root can register system bus
    if (cfg_bus_type == DBUS_BUS_SYSTEM && getuid() != 0) {
        puts(_("System service should be started as root."));
        exit(1);
    }

    // Load models
    if (model_init() != 0) {
        puts(_("Unable to load model.xml."));
        exit(1);
    }

    // Initialize DB
    if (db_init() != 0) {
        puts(_("Database is corrupt."));
        exit(1);
    }

    // Initialize main process
    proc_init(argc, argv, "Comar");

    // Start logging
    log_start();

    // Listen for DBus calls
    proc_fork(dbus_listen, "ComarDBus", NULL, NULL);

    while (1) {
        if (shutdown_activated || my_proc.nr_children == 0) {
            proc_finish();
        }
        proc_listen(&p, &size, -1, 0);
    }
}
