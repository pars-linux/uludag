/*
** Copyright (c) 2004, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

/*
** ulubot - import.c
** dictionary loaders
*/

#include "common.h"

static void
belge_wordinfo (struct dict_dict *dd, iks *x)
{
	iks *y;
	char *word;

	if (!x) return;
	for (y = iks_child (iks_find (x, "synonym")); y; y = iks_next (y)) {
		if (iks_type (y) == IKS_TAG && iks_strcmp (iks_name (y), "indexterm") == 0) {
			word = iks_find_cdata (y, "primary");
			if (word) dict_add_translation (dd, word, iks_find_cdata (iks_parent (x), "title"));
		}
	}
}

void
import_belgeler (char *file_name, char *short_name, char *desc)
{
	iks *x, *y, *z;
	struct dict_dict *dd;

	printf ("'%s' sözlüğü (%s) yükleniyor...\n", short_name, file_name);
	fflush (stdout);
	if (iks_load (file_name, &x) != IKS_OK) {
		puts ("başarısız!");
		return;
	}

	dd = dict_add (short_name, desc);

	for (y = iks_find (x, "sect1"); y; y = iks_next_tag (y)) {
		if (iks_strcmp (iks_name (y), "sect1") == 0) {
			belge_wordinfo (dd, iks_find (y, "wordinfo"));
			for (z = iks_find (y, "sect2"); z; z = iks_next_tag (z)) {
				if (iks_strcmp (iks_name (z), "sect2") == 0) {
					belge_wordinfo (dd, iks_find (z, "wordinfo"));
				}
			}
		}
	}

	iks_delete (x);
}

void
import_csv (char *file_name, char *short_name, char *desc)
{
	char buf[512];
	char *word, *def;
	struct dict_dict *dd;
	FILE *f;

	printf ("'%s' sözlüğü (%s) yükleniyor...\n", short_name, file_name);
	fflush (stdout);

	f = fopen (file_name, "r");
	if (!f) {
		puts ("başarısız!\n");
		return;
	}

	dd = dict_add (short_name, desc);
	while (fgets (buf, 511, f)) {
		// csv parse edelim
		word = strtok (buf, "\t");
		def = strtok (NULL, "\"\r\n");
		if (word[0] == '"') word++;
		if (def[0] == '"') def++;
		strtok (word, "\"");
		// karsiliksiz terimleri ekleme
		if (iks_strcmp (def, "tanımı yazılacak") == 0) continue;
		// bkz leri esanlamli olarak ekle
		if (strncmp (def, "bkz. ", 5) == 0) {
			def += 5;
			dict_add_synonym (dd, word, def);
		} else {
			// ekleyelim
			dict_add_translation (dd, word, def);
		}
	}

	fclose (f);
}
