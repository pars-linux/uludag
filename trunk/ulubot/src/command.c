/*
** Copyright (c) 2004, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

/*
** ulubot - command.c
** dictionary commands
*/

#include "common.h"

static void
cmd_usage (char *user)
{
	jabber_send (user,
		"Sözlük botu v"VERSION" komutları:\n"
		"Türkçe karşılık bulma:\n"
		"!türkçe ...\n"
		"!tr ...\n"
		"...\n"
		"Yabancı dil karşılıkları:\n"
		"!yabancı ...\n"
		"!yb ...\n"
		"Diğer:\n"
		"!yardım\n"
		"!bilgi"
	);
}

static void
cmd_info (char *user)
{
	ikstack *s;
	struct dict_dict *dt;
	char buf[32];
	char *t;

	s = iks_stack_new (0, 512);
	t = iks_stack_strdup (s, "Kullanılan Sözlükler:\n", 0);
	for (dt = dictionaries; dt; dt = dt->next) {
		if (dt != dictionaries) t = iks_stack_strcat (s, t, 0, "\n", 1);
		t = iks_stack_strcat (s, t, 0, dt->short_name, 0);
		t = iks_stack_strcat (s, t, 0, ": ", 2);
		t = iks_stack_strcat (s, t, 0, dt->copyright, 0);
		t = iks_stack_strcat (s, t, 0, " (", 2);
		sprintf (buf, "%d", dt->count);
		t = iks_stack_strcat (s, t, 0, buf, 0);
		t = iks_stack_strcat (s, t, 0, " sözcük)", 0);
	}
	jabber_send (user, t);
	iks_stack_delete (s);
}

int
levenshtein (char *s, int n, char *t)
{
	static int d[64][64];
	int m;
	int i, j, cost, a, b, c;

	if (n >= 63) n = 63;
	m = strlen (t);
	if (m >= 63) m = 63;

	for (i = 0; i < n; i++) d[i][0] = i;
	for (j = 0; j < m; j++) d[0][j] = j;

	for (i = 1; i < n; i++) {
		for (j = 1; j < m; j++) {
			if (s[i] == t[i]) cost = 0; else cost = 1;
			a = d[i-1][j] + 1;
			b = d[i][j-1] + 1;
			c = d[i-1][j-1] + cost;
			if (b > c) b = c;
			if (a > b) a = b;
			d[i][j] = a;
		}
	}
	return d[n-1][m-1];
}

static void
cmd_search (char *user, char *word)
{
	char *word2;
	struct dict_index *index = &dict_yb_index;
	int wlen, i, max_lev, cnt;
	ikstack *s = NULL;
	char *rep = NULL;

	setlocale (LC_ALL, "en_US.UTF-8");
	word2 = strcapdup (word);
	setlocale (LC_ALL, "tr_TR.UTF-8");
	if (!word2) {
		jabber_send (user, "bilmiyorum.");
		return;
	}

	cnt = 0;
	wlen = strlen (word2);
	if (wlen < 3) max_lev = 1;
	else if (wlen < 6) max_lev = 2;
	else if (wlen < 9) max_lev = 3;
	else max_lev = 4;
	for (i = 0; i < index->count; i++) {
		if (levenshtein (word2, wlen, index->words[i]) < max_lev) {
			if (NULL == s) {
				s = iks_stack_new (0, 256);
				rep = iks_stack_strdup (s, "Bildiklerim: ", 0);
			}
			if (cnt) rep = iks_stack_strcat (s, rep, 0, ", ", 2);
			rep = iks_stack_strcat (s, rep, 0, index->terms[i]->synonyms->word, 0);
			cnt++;
			if (cnt > 14) break;
		}
	}
	if (s) {
		rep = iks_stack_strcat (s, rep, 0, ".", 1);
		jabber_send (user, rep);
		iks_stack_delete (s);
	} else {
		jabber_send (user, "bilmiyorum.");
	}

	free (word2);
}

static void
cmd_turkce (char *user, char *word)
{
	struct dict_term *t;
	struct dict_word *w;
	ikstack *s;
	char *rep;

	t = dict_find (word);
	if (t) {
		s = iks_stack_new (0, 256);
		rep = NULL;
		for (w = t->translations; w; w = w->next) {
			if (rep) rep = iks_stack_strcat (s, rep, 0, ", ", 2);
			rep = iks_stack_strcat (s, rep, 0, w->word, 0);
			rep = iks_stack_strcat (s, rep, 0, " (", 2);
			rep = iks_stack_strcat (s, rep, 0, w->source->short_name, 0);
			rep = iks_stack_strcat (s, rep, 0, ")", 1);
		}
		rep = iks_stack_strcat (s, rep, 0, ".", 1);
		if (t->description) {
			rep = iks_stack_strcat (s, rep, 0, "\nAçıklama:\n", 0);
			rep = iks_stack_strcat (s, rep, 0, t->description, 0);
		}
		jabber_send (user, rep);
		iks_stack_delete (s);
	} else {
		cmd_search (user, word);
	}
}

static void
cmd_yabanci (char *user, char *word)
{
	struct dict_term *t;
	struct dict_word *w;
	ikstack *s;
	char *rep;

	t = dict_tr_find (word);
	if (t) {
		s = iks_stack_new (0, 256);
		rep = NULL;
		for (w = t->synonyms; w; w = w->next) {
			if (rep) rep = iks_stack_strcat (s, rep, 0, ", ", 2);
			rep = iks_stack_strcat (s, rep, 0, w->word, 0);
			rep = iks_stack_strcat (s, rep, 0, " (", 2);
			rep = iks_stack_strcat (s, rep, 0, w->source->short_name, 0);
			rep = iks_stack_strcat (s, rep, 0, ")", 1);
		}
		rep = iks_stack_strcat (s, rep, 0, ".", 1);
		jabber_send (user, rep);
		iks_stack_delete (s);
	} else {
		jabber_send (user, "bilmiyorum.");
	}
}

void
command_parse (char *user, char *message)
{
	char *t, *cmd;

	if (!message || message[0] == '\0') return;
	log_message (user, message);

	if (strcmp (message, "kışt") == 0) {
		if (iks_strcmp (user, prefs.admin_jid) == 0) {
			log_event ("Emir üzerine çıkıyorum.");
			exit (0);
		} else {
			jabber_send (user, "Sana kışt :p");
			return;
		}
	}

	if (message[0] != '!' && message[0] != '/') {
		cmd_turkce (user, message);
		return;
	}

	message++;
	t = strchr (message, ' ');
	if (t) {
		*t = '\0';
		t++;
	} else {
		t = "";
	}
	cmd = strcapdup (message);
	if (!cmd) return;

	if (strcmp (cmd, "Yb") == 0 || strcmp (cmd, "Yabancı") == 0) {
		cmd_yabanci (user, t);
	} else if (strcmp (cmd, "?") == 0
		|| strcmp (cmd, "Yardım") == 0) {
			cmd_usage (user);
	} else if (strcmp (cmd, "Bilgi") == 0) {
		cmd_info (user);
	} else if (strcmp (cmd, "Türkçe") == 0
		|| strcmp (cmd, "Tr") == 0) {
			cmd_turkce (user, t);
	} else {
		jabber_send (user, "buyrun?");
	}

	free (cmd);
}
