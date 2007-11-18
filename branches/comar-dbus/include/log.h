/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#define LOG_PROC 1
#define LOG_DB 2
#define LOG_JOB 4
#define LOG_PERF 8
#define LOG_ALL 0xffffffff

void log_start(void);
void log_error(const char *fmt, ...);
void log_info(const char *fmt, ...);
void log_debug(int subsys, const char *fmt, ...);
