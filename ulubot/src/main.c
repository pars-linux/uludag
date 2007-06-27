/*
** Copyright (c) 2004, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

/*
** ulubot - main.c
** main entry point, command line parsing
*/

#include <getopt.h>
#include <sys/stat.h>
#include "common.h"
#include "dict.h"

static struct option longopts[] = {
	{ "daemon", 0, 0, 'd' },
	{ "help", 0, 0, 'h' },
	{ "version", 0, 0, 'V' },
	{ 0, 0, 0, 0 }
};

static char *shortopts = "dhv";

static void
print_usage(void)
{
	puts("Kullanım: "PACKAGE" [SEÇENEKLER]\n"
		" -d, --daemon      Kabuktan ayrıl ve sunucu olarak çalış.\n"
		" -h, --help        Bu metni bas ve çık.\n"
		" -v, --version     Sürümü bas ve çık.\n"
		"Hataları <gurer@uludag.org.tr> ye bildirin."
	);
}

static void
fork_off(void)
{
	pid_t pid, sid;

	pid = fork ();
	if (pid < 0) {
		puts ("fork() failed.");
		exit (1);
	}
	// parent
	if (pid > 0) exit (0);
	// child from now on

	umask (0066);

	sid = setsid ();
	if (sid < 0) exit (1);

	close (STDIN_FILENO);
	close (STDOUT_FILENO);
	close (STDERR_FILENO);
}

int
main(int argc, char *argv[])
{
	int i, c;
	int opt_daemon = 0;

	srand (time (NULL));
	setlocale (LC_ALL, "tr_TR.UTF-8");

	while ((c = getopt_long (argc, argv, shortopts, longopts, &i)) != -1) {
		switch (c) {
			case 'd':
				opt_daemon = 1;
				break;
			case 'h':
				print_usage ();
				exit (0);
			case 'v':
				puts (PACKAGE" "VERSION);
				exit (0);
			default:
				printf ("Bilinmeyen parametre: '%c'", c);
				exit (1);
		}
	}

	import_csv ("sozluk/tbd_sozluk.csv", "TBD", "http://www.tbd.org.tr/");
	import_csv ("sozluk/en_tr.csv", "İng", "İngilizce-Türkçe sözlük");

	prefs_setup ();

	if (opt_daemon) {
		fork_off ();
	}

	while (1) {
		if (0 == jabber_connect ()) {
			while (jabber_poll () == 0) {
			}
			jabber_disconnect ();
		}
		// tekrar denemeden once 15 saniye bekle
		sleep (15);
	}

	return 0;
}
