/*
** Copyright (c) 2004, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

/*
** ulubot - dict.h
** dictionary database header
*/

#ifndef DICT_H
#define DICT_H 1

struct dict_dict {
	struct dict_dict *next, *prev;
	char *short_name;
	char *copyright;
	int count;
};

struct dict_word {
	struct dict_word *next, *prev;
	char *word;
	struct dict_dict *source;
};

struct dict_term {
	struct dict_term *next, *prev;
	char *description;
	struct dict_word *translations;
	struct dict_word *last_translation;
	struct dict_word *synonyms;
	struct dict_word *last_synonym;
};

struct dict_index {
	int size;
	int count;
	char **words;
	struct dict_term **terms;
};

extern struct dict_dict *dictionaries;
extern struct dict_term *dict_terms;
extern struct dict_index dict_tr_index;
extern struct dict_index dict_yb_index;

char *strcapdup (char *word);

struct dict_dict *dict_add (char *short_name, char *copyright);
struct dict_term *dict_find (char *word);
struct dict_term *dict_tr_find (char *word);
void dict_add_translation (struct dict_dict *dd, char *yb_word, char *tr_word);
void dict_add_synonym (struct dict_dict *dd, char *yb_word1, char *yb_word2);
void dict_add_description (struct dict_dict *dd, char *yb_word, char *desc);

int dict_load (char *file_name);
int dict_save (char *file_name);



#endif	/* DICT_H */
