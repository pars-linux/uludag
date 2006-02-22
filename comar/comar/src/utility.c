/*
** Copyright (c) 2005-2006, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include "utility.h"

int
utf8_is_valid(const char *str, size_t size)
{
	int i;
	int len = 0;
	int max = 0;
	unsigned char c;
	unsigned char mask;

	for (i = 0; i < size; i++) {
		c = str[i];

		// those are not allowed at any point
		if (0 == c || 0xFE == c || 0xFF == c) return 0;

		if (max) {
			// we are in a multi byte char

			// against the invalid long form char attack, i.e. 0xC0 0x80
			if ((c & 0xC0) != 0x80) return 0;

			len++;
			if (len == max) max = 0;

		} else {
			if (c & 0x80) {
				// multi byte char started
				if ((c & 0x60)  == 0x40) {
					max = 2;
					mask = 0x1F;
				} else if ((c & 0x70) == 0x60) {
					max = 3;
					mask = 0x0F;
				} else if ((c & 0x78) == 0x70) {
					max = 4;
					mask = 0x07;
				} else if ((c & 0x7C) == 0x78) {
					max = 5;
					mask = 0x03;
				} else if ((c & 0x7E) == 0x7C) {
					max = 6;
					mask = 0x01;
				} else {
					return 0;
				}
				// first byte of a multi byte char must contain some data
				if ((c & mask) == 0) return 0;
				len = 1;
			}
		}
	}
	// string must not end with half of a multi byte char
	if (max) return 0;

	return 1;
}

/* returns in miliseconds (1/1000 second) */
unsigned long
time_diff(struct timeval *start, struct timeval *end)
{
	unsigned long msec;

	msec = (end->tv_sec * 1000) + (end->tv_usec / 1000);
	msec -= (start->tv_sec * 1000) + (start->tv_usec / 1000);
	return msec;
}

struct pack *
pack_new(size_t min_size)
{
	struct pack *p;

	p = calloc(sizeof(struct pack), 1);
	if (!p) return NULL;
	if (min_size < 256) min_size = 256;
	p->max = min_size;
	p->buffer = malloc(p->max);
	if (!p->buffer) {
		free(p);
		return NULL;
	}
	return p;
}

struct pack *
pack_wrap(char *buffer, size_t size)
{
	struct pack *p;

	p = calloc(sizeof(struct pack), 1);
	if (!p) return NULL;
	p->buffer = buffer;
	p->max = size;
	p->used = size;
	return p;
}

struct pack *
pack_dup(struct pack *oldpak)
{
	struct pack *p;

	p = calloc(sizeof(struct pack), 1);
	if (!p) return NULL;
	p->buffer = malloc(oldpak->max);
	if (!p->buffer) {
		free(p);
		return NULL;
	}
	p->max = oldpak->max;
	p->used = oldpak->used - oldpak->pos;
	memcpy(p->buffer, oldpak->buffer + oldpak->pos, oldpak->used - oldpak->pos);

	return p;
}

void
pack_delete(struct pack *p)
{
	free(p->buffer);
	free(p);
}

void
pack_reset(struct pack *p)
{
	p->used = 0;
	p->pos = 0;
}

void
pack_ensure_size(struct pack *p, size_t need)
{
	if (need >= p->max) {
		while (need >= p->max) p->max *= 2;
		p->buffer = realloc(p->buffer, p->max);
	}
}

void
pack_put(struct pack *p, const char *arg, size_t size)
{
	unsigned char *ptr;
	size_t need;

	need = p->used + size + 3;
	pack_ensure_size(p, need);

	ptr = p->buffer + p->used;
	*ptr++ = (size & 0xff);
	*ptr++ = (size & 0xff00) >> 8;
	memcpy(ptr, arg, size);
	ptr += size;
	*ptr = '\0';

	p->used += size + 3;
}

int
pack_get(struct pack *p, char **argp, size_t *sizep)
{
	unsigned char *ptr;
	size_t size;

	if (p->pos >= p->used) {
		if (sizep) *sizep = 0;
		*argp = NULL;
		return 0;
	}

	ptr = p->buffer + p->pos;
	size = ptr[0] + (ptr[1] << 8);
	if (sizep) *sizep = size;
	if (size) *argp = ptr + 2; else *argp = NULL;
	p->pos += 2 + size + 1;

	return 1;
}

void
pack_replace(struct pack *p, const char *arg, const char *value, size_t size)
{
	unsigned char *ptr;
	char *t;
	size_t ts;
	size_t old_size;
	size_t diff;

	p->pos = 0;
	while (pack_get(p, &t, &ts)) {
		if (strcmp(t, arg) == 0) {
			// found it, replace the old value
			ptr = p->buffer + p->pos;
			old_size =  ptr[0] + (ptr[1] << 8);
			diff = size - old_size;
			if (old_size < size && p->max - p->used < diff) {
				pack_ensure_size(p, p->max + diff);
				ptr = p->buffer + p->pos;
			}
			if (diff) {
				size_t len = p->used - (p->pos + old_size + 3);
				memmove(ptr + old_size + 3 + diff, ptr + old_size + 3, len);
			}
			*ptr++ = (size & 0xff);
			*ptr++ = (size & 0xff00) >> 8;
			memcpy(ptr, value, size);
			ptr += size;
			*ptr = '\0';
			p->used += diff;
			return;
		}
		// skip the argument's value
		pack_get(p, &t, &ts);
	}
	// no old value, append as new
	pack_put(p, arg, strlen(arg));
	pack_put(p, value, size);
}
