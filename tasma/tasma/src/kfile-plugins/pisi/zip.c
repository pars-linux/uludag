/* imposter (OO.org Impress viewer)
** Copyright (C) 2003 Gurer Ozen <madcat@e-kolay.net>
** This code is free software; you can redistribute it and/or
** modify it under the terms of GNU General Public License.
*/

#include <sys/types.h>
#include <stdio.h>

#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <errno.h>

#include <zlib.h>
#include <iksemel.h>

#include "zip.h"


enum {
	ZIP_OK = 0,
	ZIP_NOMEM,
	ZIP_NOSIG,
	ZIP_BADZIP,
	ZIP_NOMULTI,
	ZIP_EOPEN,
	ZIP_EREAD,
	ZIP_NOFILE
};

struct zipfile {
	struct zipfile *next;
	char *name;
	ulong crc;
	ulong zip_size;
	ulong real_size;
	ulong pos;
};

struct zip_struct {
	FILE *f;
	struct zipfile *files;
	ulong cd_pos;
	ulong cd_size;
	ulong cd_offset;
	ulong head_size;
	ulong rem_size;
	ulong nr_files;
};

static int
find_cd (zip *z)
{
	FILE *f;
	char *buf;
	ulong size, pos, i, flag;

	f = z->f;
	if (fseek (f, 0, SEEK_END) != 0) return 1;
	size = ftell (f);
	if (size < 0xffff) pos = 0; else pos = size - 0xffff;
	buf = malloc (size - pos + 1);
	if (!buf) return 1;
	if (fseek (f, (long)pos, SEEK_SET) != 0) {
		free (buf);
		return 1;
	}
	if (fread (buf, size - pos, 1, f) != 1) {
		free (buf);
		return 1;
	}
	flag = 0;
	for (i = size - pos - 3; i > 0; i--) {
		if (buf[i] == 0x50 && buf[i+1] == 0x4b && buf[i+2] == 0x05 && buf[i+3] == 0x06) {
			z->cd_pos = i + pos;
			flag = 1;
			break;
		}
	}
	free (buf);
	if (flag != 1) return 1;
	return 0;
}

static unsigned long
get_long (unsigned char *buf)
{
	return buf[0] + (buf[1] << 8) + (buf[2] << 16) + (buf[3] << 24);
}

static unsigned long
get_word (unsigned char *buf)
{
	return buf[0] + (buf[1] << 8);
}

static int
list_files (zip *z)
{
	unsigned char buf[46];
	struct zipfile *zfile;
	ulong pat, fn_size;
	uint nr = 0;

	pat = z->cd_offset;
	while (nr < z->nr_files) {
          fseek (z->f, (long)(pat + z->head_size), SEEK_SET);

		if (fread (buf, 46, 1, z->f) != 1) return ZIP_EREAD;
		if (get_long (buf) != 0x02014b50) return ZIP_BADZIP;

		zfile = malloc (sizeof (struct zipfile));
		if (!zfile) return ZIP_NOMEM;
		memset (zfile, 0, sizeof (struct zipfile));

		zfile->crc = get_long (buf + 16);
		zfile->zip_size = get_long (buf + 20);
		zfile->real_size = get_long (buf + 24);
		fn_size = get_word (buf + 28);
		zfile->pos = get_long (buf + 42);

		zfile->name = malloc (fn_size + 1);
		if (!zfile->name) {
			free (zfile);
			return ZIP_NOMEM;
		}
		fread (zfile->name, fn_size, 1, z->f);
		zfile->name[fn_size] = '\0';

		zfile->next = z->files;
		z->files = zfile;

		pat += 0x2e + fn_size + get_word (buf + 30) + get_word (buf + 32);
		nr++;
	}
	return ZIP_OK;
}

zip *
zip_open (const char *fname, int *err)
{
	unsigned char buf[22];
	zip *z;
	FILE *f;

	f = fopen (fname, "rb");
	if (NULL == f) {
		*err = ZIP_EOPEN;
		return NULL;
	}

	z = malloc (sizeof (zip));
	memset (z, 0, sizeof (zip));
	z->f = f;

	if (find_cd (z)) {
		zip_close (z);
		*err = ZIP_NOSIG;
		return NULL;
	}

	fseek (f, (long)z->cd_pos, SEEK_SET);
	if (fread (buf, 22, 1, f) != 1) {
		zip_close (z);
		*err = ZIP_EREAD;
		return NULL;
	}
	z->nr_files = get_word (buf + 10);
	if (get_word (buf + 8) != z->nr_files) {
		zip_close (z);
		*err =  ZIP_NOMULTI;
		return NULL;
	}
	z->cd_size = get_long (buf + 12);
	z->cd_offset = get_long (buf + 16);
	z->rem_size = get_word (buf + 20);
	z->head_size = z->cd_pos - (z->cd_offset + z->cd_size);

	*err = list_files (z);
	if (*err != ZIP_OK) {
		zip_close (z);
		return NULL;
	}

	*err = ZIP_OK;
	return z;
}

void
zip_close (zip *z)
{
	struct zipfile *zfile, *tmp;

	zfile = z->files;
	while (zfile) {
		tmp = zfile->next;
		if (zfile->name) free (zfile->name);
		free (zfile);
		zfile = tmp;
	}
	z->files = NULL;
	if (z->f) fclose (z->f);
	z->f = NULL;
}

static struct zipfile *
find_file (zip *z, const char *name)
{
	struct zipfile *zfile;

	zfile = z->files;
	while (zfile) {
		if (strcmp (zfile->name, name) == 0) return zfile;
		zfile = zfile->next;
	}
	return NULL;
}

static int
seek_file (zip *z, struct zipfile *zfile)
{
	unsigned char buf[30];

	fseek (z->f, (long)(zfile->pos + z->head_size), SEEK_SET);
	if (fread (buf, 30, 1, z->f) != 1) return ZIP_EREAD;
	if (get_long (buf) != 0x04034b50) return ZIP_BADZIP;
	fseek (z->f, (long)(get_word (buf + 26) + get_word (buf + 28)), SEEK_CUR);
	return ZIP_OK;
}

iks *
zip_load_xml (zip *z, const char *name, int *err)
{
	iksparser *prs;
	char *real_buf;
	iks *x;
	struct zipfile *zfile;

	*err = ZIP_OK;

	zfile = find_file (z, name);
	if (!zfile) {
		*err = ZIP_NOFILE;
		return NULL;
	}

	*err = seek_file (z, zfile);
	if (*err != ZIP_OK) return NULL;

	real_buf = malloc (zfile->real_size + 1);
	if (!real_buf) {
		*err = ZIP_NOMEM;
		return NULL;
	}
	if (zfile->zip_size < zfile->real_size) {
		char *zip_buf;
		z_stream zs;
		zs.zalloc = NULL;
		zs.zfree = NULL;
		zs.opaque = NULL;
		zip_buf = malloc (zfile->zip_size);
		if (!zip_buf) {
			*err = ZIP_NOMEM;
			free(real_buf);
			return NULL;
		}
		if (1 != fread (zip_buf, zfile->zip_size, 1, z->f)) {
			*err = ZIP_EREAD;
			free(zip_buf);
			free(real_buf);
			return NULL;
		}
		zs.next_in = zip_buf;
		zs.avail_in = zfile->zip_size;
		zs.next_out = real_buf;
		zs.avail_out = zfile->real_size;
		inflateInit2 (&zs, -MAX_WBITS);
		if (inflate (&zs, Z_FINISH) < 0) {
			*err = ZIP_BADZIP;
			free(zip_buf);
			free(real_buf);
			return NULL;
		}
		inflateEnd (&zs);
		free (zip_buf);
	} else {
		if (1 != fread (real_buf, zfile->real_size, 1, z->f)) {
			*err = ZIP_EREAD;
			free(real_buf);
			return NULL;
		}
	}

	real_buf[zfile->real_size] = '\0';
	prs = iks_dom_new (&x);
	if (IKS_OK != iks_parse (prs, real_buf, zfile->real_size, 1)) {
		*err = ZIP_BADZIP;
		iks_parser_delete(prs);
		free(real_buf);
		return NULL;
	}
	iks_parser_delete (prs);
	free (real_buf);
	return x;
}

unsigned long zip_get_size (zip *z, const char *name)
{
	struct zipfile *zf;

	zf = find_file (z, name);
	if (!zf) return 0;
	return zf->real_size;
}

int zip_load (zip *z, const char *name, char *buf)
{
	struct zipfile *zfile;

	zfile = find_file (z, name);
	if (!zfile) return ZIP_NOFILE;

	seek_file (z, zfile);

	if (zfile->zip_size < zfile->real_size) {
		char *zip_buf;
		z_stream zs;
		zs.zalloc = NULL;
		zs.zfree = NULL;
		zs.opaque = NULL;
		zip_buf = malloc (zfile->zip_size);
		fread (zip_buf, zfile->zip_size, 1, z->f);
		zs.next_in = zip_buf;
		zs.avail_in = zfile->zip_size;
		zs.next_out = buf;
		zs.avail_out = zfile->real_size;
		inflateInit2 (&zs, -MAX_WBITS);
		inflate (&zs, Z_FINISH);
		inflateEnd (&zs);
		free (zip_buf);
	} else {
		fread (buf, zfile->real_size, 1, z->f);
	}

	return ZIP_OK;
}
