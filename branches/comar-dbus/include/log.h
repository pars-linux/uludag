/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

enum LOG {
    LOG_CALL = 0,
    LOG_PROC,
    LOG_DBUS,
    LOG_PERF,
    LOG_FULL
};

void log_start(void);
void log_error(const char *fmt, ...);
void log_info(const char *fmt, ...);
void log_debug(int subsys, const char *fmt, ...);
