/*
** Copyright (c) 2004, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

/*
** ulubot - common.h
** common includes, macros and prototypes
*/

#ifndef COMMON_H
#define COMMON_H 1

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <sys/types.h>
#include <stdio.h>
#include <time.h>
#include <ctype.h>

#ifdef STDC_HEADERS
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#elif HAVE_STRINGS_H
#include <strings.h>
#endif

#include <wctype.h>

#ifdef HAVE_UNISTD_H
#include <unistd.h>
#endif

#ifdef HAVE_ERRNO_H
#include <errno.h>
#endif
#ifndef errno
extern int errno;
#endif

#include "i18n.h"
#include <iksemel.h>

#include "dict.h"

// prefs

struct prefs_struct {
	char *jid;
	char *pass;
	char *admin_jid;
};

extern struct  prefs_struct prefs;

void prefs_setup (void);
void log_event (const char *fmt, ...);
void log_message (const char *from, const char *message);
void log_protocol (const char *data, int is_incoming, int is_secure);

// jabber stuff

void jabber_setup ();
int jabber_connect ();
int jabber_poll (void);
void jabber_send (char *user, char *message);
void jabber_disconnect (void);

// commands

void command_parse (char *user, char *message);

// importers

void import_belgeler (char *file_name, char *short_name, char *desc);
void import_csv (char *file_name, char *short_name, char *desc);


#endif	/* COMMON_H */
