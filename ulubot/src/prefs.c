/*
** Copyright (c) 2004, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

/*
** ulubot - prefs.c
** configuration, log utilities
*/

#include "common.h"
#include <dirent.h>
#include <sys/stat.h>
#include <time.h>

struct  prefs_struct prefs;

static void
prefs_chdir (char *dir_name)
{
	char *t;

	t = getenv ("HOME");
	if (t) chdir (t);

	t = dir_name;
	if (chdir (t) != 0) {
		// dizin mevcut degil, hemen olusturalim
		mkdir (t, 0700);
		if (chdir (t) != 0) {
			printf ("Hata: '%s' dizinini oluşturamadım!\n", dir_name);
			exit (1);
		}
	}
}

static char *
input (char *msg)
{
	static char buf[128];

	printf ("%s> ", msg);
	fflush (stdout);
	fgets (buf, 126, stdin);
	strtok (buf, " \t\r\n");
	return buf;
}

void
prefs_setup (void)
{
	iks *x;

	memset (&prefs, 0, sizeof (struct prefs_struct));

	prefs_chdir (".ulubot");

	if (iks_load ("ayarlar.xml", &x) == IKS_OK) {
		if (iks_strcmp (iks_name (x), "ulubot") == 0) {
			prefs.jid = iks_strdup (iks_find_cdata (x, "id"));
			prefs.pass = iks_strdup (iks_find_cdata (x, "password"));
			prefs.admin_jid = iks_strdup (iks_find_cdata (x, "admin_id"));
			iks_delete (x);
			if (prefs.jid && prefs.pass && prefs.admin_jid) return;
		}
	}

	puts (PACKAGE" v"VERSION" sözlük sunucusuna hoşgeldiniz!");
	puts ("Hemen bir kaç ayar yapalım:");

	prefs.jid = iks_strdup (input ("Botun Jabber hesabı"));
	prefs.pass = iks_strdup (input ("Botun Jabber şifresi"));
	prefs.admin_jid = iks_strdup (input ("Yöneticinin Jabber hesabı"));

	x = iks_new ("ulubot");
	iks_insert_cdata (iks_insert (x, "id"), prefs.jid, 0);
	iks_insert_cdata (iks_insert (x, "password"), prefs.pass, 0);
	iks_insert_cdata (iks_insert (x, "admin_id"), prefs.admin_jid, 0);
	if (iks_save ("ayarlar.xml", x) != IKS_OK) {
		puts ("Hata: ayarları kaydedemedim!");
	}
	iks_delete (x);

	puts ("Ayarlar tamam.");
}

static void
print_time (FILE *f)
{
	static char buf[128];
	time_t t;
	struct tm *bt;

	time (&t);
	bt = gmtime (&t);
	strftime (buf, 127, "%F %T", bt);
	fputs (buf, f);
}

void
log_event (const char *fmt, ...)
{
	va_list ap;
	FILE *f;

	f = fopen ("olaylar.log", "ab");
	va_start (ap, fmt);
	print_time (f);
	fputs (" ", f);
	vfprintf (f, fmt, ap);
	fputs ("\n", f);
	va_end (ap);
	fclose (f);
}

void
log_message (const char *from, const char *message)
{
	FILE *f;

	f = fopen ("istekler.log", "ab");
	print_time (f);
	fprintf (f, " (%s)\n%s\n\n", from, message);
	fclose (f);
}

void
log_protocol (const char *data, int is_incoming, int is_secure)
{
	FILE *f;
	char *sec, *inc;

	if (is_secure) sec = "Sec"; else sec = "";
	if (is_incoming) inc = "RECV"; else inc = "SEND";
	f = fopen ("protokol.log", "ab");
	print_time (f);
	fprintf (f, " %s%s\n%s\n\n", sec, inc, data);
	fclose (f);
}
