/*
** Copyright (c) 2004, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

/*
** ulubot - dict.c
** dictionary database
*/

#include "common.h"

struct dict_dict *dictionaries;
struct dict_term *dict_terms;
struct dict_index dict_tr_index;
struct dict_index dict_yb_index;

// yeni bir sözlük ekler
struct dict_dict *
dict_add (char *short_name, char *copyright)
{
	struct dict_dict *dd;

	dd = malloc (sizeof (struct dict_dict));
	memset (dd, 0, sizeof (struct dict_dict));
	dd->short_name = short_name;
	dd->copyright = copyright;
	if (dictionaries) {
		dictionaries->prev = dd;
		dd->next = dictionaries;
	}
	dictionaries = dd;
	return dd;
}

// stringin ilk harfi büyük, diğerleri küçük kopyasını çıkarır
// sözcükler bellekte hep bu biçimde utf8 olarak tutulacak
// ui'de gösterirken kolaylık, ayrıca aramayı strcmp ile yapabiliyoruz
char *
strcapdup (char *word)
{
	static wchar_t wbuf[128];
	static char buf[512];
	size_t size;
	int i;

	size = strlen (word);
	size = mbstowcs (wbuf, word, size + 1);
	if (size == (size_t) -1) return NULL;
	if (size) wbuf[0] = towupper (wbuf[0]);
	for (i = 1; i < size; i++)
		wbuf[i] = towlower (wbuf[i]);
	size = wcstombs (buf, wbuf, 511);
	if (size == (size_t) -1) return NULL;
	return strdup (buf);
}

// verilen indekste sözcüğü bulur, sırasını döndürür
static int
index_find (struct dict_index *index, char *word)
{
	int min, max, i, cmp;

	min = 0;
	max = index->count - 1;
	if (strcoll (word, index->words[min]) < 0) return -1;
	if (strcoll (word, index->words[max]) > 0) return -1;
	while (1) {
		i = min + (max - min) / 2;
		cmp = strcmp (word, index->words[i]);
		if (cmp == 0) return i;
		cmp = strcoll (word, index->words[i]);
		if (cmp < 0) max = i;
		if (cmp > 0) min = i;
		if (max - min < 2) {
			if (strcmp (word, index->words[min]) == 0) return min;
			if (strcmp (word, index->words[max]) == 0) return max;
			return -1;
		}
	}
}

// verilen sözcüğü belirtilen indekse ekler
static void
index_add (struct dict_index *index, char *word, struct dict_term *t)
{
	int i;

	if (index->size == 0) {
		// indeks boş, hazırlayalım
		index->size = 8192;
		index->words = malloc (sizeof (char *) * index->size);
		memset (index->words, 0, sizeof (char *) * index->size);
		index->terms = malloc (sizeof (struct dict_term *) * index->size);
		memset (index->terms, 0, sizeof (struct dict_term *) * index->size);
		// ilk sözcük olarak ekle
		index->words[0] = word;
		index->terms[0] = t;
		index->count = 1;
		return;
	}
	if (index->count + 1 >= index->size) {
		// indeks yetmiyor, duple yap
		char **words;
		struct dict_term **terms;

		words = malloc (sizeof (char *) * index->size * 2);
		memset (words, 0, sizeof (char *) * index->size * 2);
		memcpy (words, index->words, sizeof (char *) * index->size);
		terms = malloc (sizeof (struct dict_term *) * index->size * 2);
		memset (terms, 0, sizeof (struct dict_term *) * index->size * 2);
		memcpy (terms, index->terms, sizeof (struct dict_term *) * index->size);
		free (index->words);
		free (index->terms);
		index->words = words;
		index->terms = terms;
		index->size *= 2;
	}

	for (i = 0; i < index->count; i++) {
		if (strcoll (word, index->words[i]) < 0) break;
	}
	if (i < index->count) {
		memmove (&index->words[i+1], &index->words[i], sizeof (char *) * (index->count - i));
		memmove (&index->terms[i+1], &index->terms[i], sizeof (struct dict_term *) * (index->count - i));
	}
	index->words[i] = word;
	index->terms[i] = t;
	index->count++;
}

// verilen yabancı sözcüğü arar
struct dict_term *
dict_find (char *word)
{
	int i;
	char *word2;

	if (dict_yb_index.size == 0) return NULL;
	setlocale (LC_ALL, "en_US.UTF-8");
	word2 = strcapdup (word);
	i = -1;
	if (word2) {
		i = index_find (&dict_yb_index, word2);
		free (word2);
	}
	setlocale (LC_ALL, "tr_TR.UTF-8");
	if (i >= 0) return dict_yb_index.terms[i];
	return NULL;
}

// verilen türkçe sözcüğü arar
struct dict_term *
dict_tr_find (char *word)
{
	int i;
	char *word2;

	if (dict_tr_index.size == 0) return NULL;
	word2 = strcapdup (word);
	if (word2) {
		i = index_find (&dict_tr_index, word2);
		free (word2);
		if (i >= 0) return dict_tr_index.terms[i];
	}
	return NULL;
}

// terime eşanlamlı ekler
static void
add_synonym (struct dict_dict *dd, struct dict_term *t, char *yb_word)
{
	struct dict_word *w;

	setlocale (LC_ALL, "en_US.UTF-8");
	w = malloc (sizeof (struct dict_word));
	memset (w, 0, sizeof (struct dict_word));
	w->word = strcapdup (yb_word);
	if (!w->word) {
		free (w);
		setlocale (LC_ALL, "tr_TR.UTF-8");
		return;
	}
	w->source = dd;

	if (!t->synonyms) t->synonyms = w;
	if (t->last_synonym) {
		t->last_synonym->next = w;
		w->prev = t->last_synonym;
	}
	t->last_synonym = w;

	index_add (&dict_yb_index, w->word, t);
	setlocale (LC_ALL, "tr_TR.UTF-8");
}

// verilen sözlükteki bir çeviriyi ekleyip indeksler
void
dict_add_translation (struct dict_dict *dd, char *yb_word, char *tr_word)
{
	struct dict_term *t;
	struct dict_word *w;

	if (!yb_word || !tr_word) return;

	w = malloc (sizeof (struct dict_word));
	memset (w, 0, sizeof (struct dict_word));
	w->word = strcapdup (tr_word);
	if (!w->word) {
		free (w);
		return;
	}
	w->source = dd;

	t = dict_find (yb_word);
	if (!t) {
		t = malloc (sizeof (struct dict_term));
		memset (t, 0, sizeof (struct dict_term));
		if (dict_terms) {
			dict_terms->prev = t;
			t->next = dict_terms;
		}
		dict_terms = t;
		add_synonym (dd, t, yb_word);
	}

	if (!t->translations) t->translations = w;
	if (t->last_translation) {
		t->last_translation->next = w;
		w->prev = t->last_translation;
	}
	t->last_translation = w;

	dd->count++;

	index_add (&dict_tr_index, w->word, t);
}

// verilen sözlükteki bir eşanlamlıyı ekleyip indeksler
void
dict_add_synonym (struct dict_dict *dd, char *yb_word1, char *yb_word2)
{
	struct dict_term *t;

	if (!yb_word1 || !yb_word2) return;

	dd->count++;

	t = dict_find (yb_word1);
	if (t) {
		add_synonym (dd, t, yb_word2);
		return;
	}
	t = dict_find (yb_word2);
	if (t) {
		add_synonym (dd, t, yb_word1);
		return;
	}

	t = malloc (sizeof (struct dict_term));
	memset (t, 0, sizeof (struct dict_term));
	if (dict_terms) {
		dict_terms->prev = t;
		t->next = dict_terms;
	}
	dict_terms = t;

	add_synonym (dd, t, yb_word1);
	add_synonym (dd, t, yb_word2);
}

// verilen sözlükteki bir açıklamayı ekler
void
dict_add_description (struct dict_dict *dd, char *yb_word, char *desc)
{
	struct dict_term *t;

	if (!yb_word || !desc) return;

	t = dict_find (yb_word);
	if (!t) {
		t = malloc (sizeof (struct dict_term));
		memset (t, 0, sizeof (struct dict_term));
		if (dict_terms) {
			dict_terms->prev = t;
			t->next = dict_terms;
		}
		dict_terms = t;
	}

	if (t->description) free (t->description);
	t->description = strdup (desc);
}

// verilen UDS biçimindeki sözlüğü yükler
int
dict_load (char *file_name)
{
	iks *x, *y, *z;
	struct dict_dict *dd;
	char *a;
	int e;

	e = iks_load (file_name, &x);
	if (e) return e;

	if (iks_strcmp (iks_name (x), "ud_sözlük") != 0) {
		iks_delete (x);
		return -1;
	}
	dd = dict_add (iks_strdup (iks_find_cdata (x, "short")),
		iks_strdup (iks_find_cdata (x, "copyright")));

	for (y = iks_find (x, "term"); y; y = iks_next_tag (y)) {
		if (iks_strcmp (iks_name (y), "term") == 0) {
			a = iks_find_cdata (y, "s");
			if (!a) continue;
			for (z = iks_find (y, "t"); z; z = iks_next_tag (z)) {
				if (iks_strcmp (iks_name (z), "t") == 0)
					dict_add_translation (dd, a, iks_cdata (iks_child (z)));
			}
			z = iks_find (y, "s");
			for (z = iks_next_tag (z); z; z = iks_next_tag (z)) {
				if (iks_strcmp (iks_name (z), "s") == 0)
					dict_add_synonym (dd, a, iks_cdata (iks_child (z)));
			}
			dict_add_description (dd, a, iks_find_cdata (y, "d"));
		}
	}

	iks_delete (x);
	return 0;
}

// sözlüğü UDS biçiminde kaydeder
int
dict_save (char *file_name)
{
	struct dict_term *t;
	struct dict_word *w;
	iks *x, *y;
	int e;

	x = iks_new ("ud_sözlük");
	iks_insert_cdata (x, "\n", 1);
	iks_insert_cdata (iks_insert (x, "short"), "Uludağ", 0);
	iks_insert_cdata (x, "\n", 1);
	iks_insert_cdata (iks_insert (x, "copyright"), "http://www.uludag.org.tr", 0);
	iks_insert_cdata (x, "\n", 1);

	for (t = dict_terms; t; t = t->next) {
		y = iks_insert (x, "term");
		iks_insert_cdata (y, "\n", 1);
		for (w = t->synonyms; w; w = w->next) {
			iks_insert_cdata (iks_insert (y, "s"), w->word, 0);
		}
		iks_insert_cdata (y, "\n", 1);
		for (w = t->translations; w; w = w->next) {
			iks_insert_cdata (iks_insert (y, "t"), w->word, 0);
		}
		iks_insert_cdata (y, "\n", 1);
		iks_insert_cdata (iks_insert (y, "d"), t->description, 0);
		iks_insert_cdata (y, "\n", 1);
	}
	iks_insert_cdata (x, "\n", 1);

	e = iks_save (file_name, x);
	iks_delete (x);
	return e;
}
