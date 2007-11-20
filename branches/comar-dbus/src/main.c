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
#include "dbus.h"
#include "i18n.h"
#include "log.h"
#include "process.h"

int
main(int argc, char *argv[])
{
    struct ProcChild *p;
    int size;

    setlocale(LC_MESSAGES, "");
    bindtextdomain("comar", "/usr/share/locale");
    bind_textdomain_codeset("comar", "UTF-8");
    bind_textdomain_codeset("libc", "UTF-8");
    textdomain("comar");

    cfg_init(argc, argv);
    if (getuid() != 0) {
        puts(_("This program is a system service and should not be started by users."));
        exit(1);
    }

    cfg_init(argc, argv);
    proc_init(argc, argv, "Comar");

    log_start();

    proc_fork(dbus_listen, "ComarDBus", NULL, NULL);
    while (1) {
        if (shutdown_activated) {
            proc_finish();
        }
        proc_listen(&p, &size, -1);
    }
}
