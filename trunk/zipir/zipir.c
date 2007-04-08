/*
  Copyright (c) 2005-2007 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <string.h>

#include <zlib.h>
#include "zipir.h"


char *
zip_error (int err)
{
    char *ret;

    switch (err) {
        case ZIP_OK:
            ret = "No error";
            break;
        case ZIP_NOMEM:
            ret = "Not enough memory";
            break;
        case ZIP_NOSIG:
            ret = "Cannot find zip signature";
            break;
        case ZIP_BADZIP:
            ret = "Invalid zip file";
            break;
        case ZIP_NOMULTI:
            ret = "Multi file zips are not supported";
            break;
        case ZIP_EOPEN:
            ret = "Cannot open the file";
            break;
        case ZIP_EREAD:
            ret = "Cannot read data from file";
            break;
        case ZIP_EWRITE:
            ret = "Cannot write to file";
            break;
        case ZIP_NOFILE:
            ret = "Cannot find file in the zip archive";
            break;
        default:
            ret = "Unknown error";
            break;
    }
    return ret;
}

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
    if (fseek (f, pos, SEEK_SET) != 0) {
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
    int nr = 0;

    pat = z->cd_offset;
    while (nr < z->nr_files) {
        fseek (z->f, pat + z->head_size, SEEK_SET);

        if (fread (buf, 46, 1, z->f) != 1) return ZIP_EREAD;
        if (get_long (buf) != 0x02014b50) return ZIP_BADZIP;

        zfile = malloc (sizeof (struct zipfile));
        if (!zfile) return ZIP_NOMEM;
        memset (zfile, 0, sizeof (struct zipfile));

        zfile->os_made_by = buf[5];
        zfile->crc = get_long (buf + 16);
        zfile->zip_size = get_long (buf + 20);
        zfile->real_size = get_long (buf + 24);
        fn_size = get_word (buf + 28);
        // zfile->xattr = get_long (buf + 38);
        zfile->xattr = get_word (buf + 40);
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
zip_open (const char *fname, int *err, int action)
{
    unsigned char buf[22];
    zip *z;
    FILE *f;

    if (action == AC_APPEND){
        f = fopen (fname, "r+b");
    } else {
        f = fopen (fname, "rb");
    }

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

    fseek (f, z->cd_pos, SEEK_SET);
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

    fseek (z->f, zfile->pos + z->head_size, SEEK_SET);
    if (fread (buf, 30, 1, z->f) != 1) return ZIP_EREAD;
    if (get_long (buf) != 0x04034b50) return ZIP_BADZIP;
    fseek (z->f, get_word (buf + 26) + get_word (buf + 28), SEEK_CUR);
    return ZIP_OK;
}

unsigned long 
zip_get_size (zip *z, const char *name)
{
    struct zipfile *zf;

    zf = find_file (z, name);
    if (!zf) return 0;
    return zf->real_size;
}

int
parse_xattr (mode_t xattr, char *attribs)
{
    switch ((unsigned)(xattr & UNX_IFMT)) {
        case (unsigned)UNX_IFDIR:   attribs[0] = 'd';  break;
        case (unsigned)UNX_IFREG:   attribs[0] = '-';  break;
        case (unsigned)UNX_IFLNK:   attribs[0] = 'l';  break;
        case (unsigned)UNX_IFBLK:   attribs[0] = 'b';  break;
        case (unsigned)UNX_IFCHR:   attribs[0] = 'c';  break;
        case (unsigned)UNX_IFIFO:   attribs[0] = 'p';  break;
        case (unsigned)UNX_IFSOCK:  attribs[0] = 's';  break;
        default:                    attribs[0] = '?';  break;
        }

    attribs[1] = (xattr & UNX_IRUSR)? 'r' : '-';
    attribs[4] = (xattr & UNX_IRGRP)? 'r' : '-';
    attribs[7] = (xattr & UNX_IROTH)? 'r' : '-';

    attribs[2] = (xattr & UNX_IWUSR)? 'w' : '-';
    attribs[5] = (xattr & UNX_IWGRP)? 'w' : '-';
    attribs[8] = (xattr & UNX_IWOTH)? 'w' : '-';

    if (xattr & UNX_IXUSR)
        attribs[3] = (xattr & UNX_ISUID)? 's' : 'x';
    else
        attribs[3] = (xattr & UNX_ISUID)? 'S' : '-';   /* S = undefined */
    if (xattr & UNX_IXGRP)
        attribs[6] = (xattr & UNX_ISGID)? 's' : 'x';   /* == UNX_ENFMT */
    else
        attribs[6] = (xattr & UNX_ISGID)? 'l' : '-';
    if (xattr & UNX_IXOTH)
        attribs[9] = (xattr & UNX_ISVTX)? 't' : 'x';   /* "sticky bit" */
    else
        attribs[9] = (xattr & UNX_ISVTX)? 'T' : '-';   /* T = undefined */

    attribs[10] = 0; /* End of attributes */

    return 0;

}

int
zip_get_attrib (zip *z, char *name)
{
    struct zipfile *zfile;
    unsigned char buf[30];
    unsigned char *extra_data;
    unsigned long len_extra, hpos = 0, data_type;

    zfile = find_file (z, name);
    if (!zfile) return ZIP_NOFILE;

    fseek (z->f, zfile->pos + z->head_size, SEEK_SET);
    if (fread (buf, 30, 1, z->f) != 1) return ZIP_EREAD;
    if (get_long (buf) != 0x04034b50) return ZIP_BADZIP;

    len_extra = get_word (buf + 28);
    fseek (z->f, zfile->pos + get_word (buf + 26) + 30, SEEK_SET);

    // printf (" len_extra = %lu\t hpos = %lu\n", len_extra, hpos);

    extra_data = malloc (len_extra);
    fread (extra_data, len_extra, 1, z->f);

    while (hpos < len_extra) {
        data_type = get_word (extra_data + hpos);
        // printf (" data type = %lu\t", data_type);

        switch (data_type) {
            case 0x7855:
                printf ("   has Unix UID/GID\n");

                zfile->uid = get_word (extra_data + hpos + 4);
                zfile->gid = get_word (extra_data + hpos + 6);
                printf ("      uid = %i\n      gid = %i\n", zfile->uid, zfile->gid);
                hpos = hpos + 4 + get_word (extra_data + hpos + 2);
                break;

            case 0x5455:
                printf ("   has Universal Time\n");

                int i = 5;
                int tmp;
                tmp = *(extra_data + 4);

                if (tmp & 1) {
                    zfile->mtime = get_long (extra_data + hpos + i);
                    printf ("      mtime = %s", ctime(&zfile->mtime));
                    i = i + 4;
                }

                if (tmp & 2) {
                    zfile->atime = get_long (extra_data + hpos + i);
                    printf ("      atime = %s", ctime(&zfile->atime));
                    i = i + 4;
                }

                if (tmp & 4) {
                    zfile->ctime = get_long (extra_data + hpos + i);
                    printf ("      ctime = %s", ctime(&zfile->ctime));
                    i = i + 4;
                }

                hpos = hpos + 4 + get_word (extra_data + hpos + 2);
                break;

            case 0x5855:
                printf ("   has old Info-ZIP Unix/OS2/NT data\n");

                zfile->atime = get_long (extra_data + hpos + 4);
                printf ("      atime = %s", ctime(&zfile->mtime));
                zfile->mtime = get_long (extra_data + hpos + 8);
                printf ("      mtime = %s", ctime(&zfile->atime));

                if ((get_word (extra_data + hpos + 2)) > 8) {
                    zfile->uid = get_word (extra_data + hpos + 12);
                    printf ("      uid = %i\n", zfile->uid);
                }

                if ((get_word (extra_data + hpos + 2)) > 10) {
                    zfile->gid = get_word (extra_data + hpos + 14);
                    printf ("      gid = %i\n", zfile->gid);
                }

                hpos = hpos + 4 + get_word (extra_data + hpos + 2);
                break;

            default:
                printf ("   Unknown data type = %lu\n", data_type);
                hpos = hpos + 4 + get_word (extra_data + hpos + 2);
                break;
        }
    }

    free (extra_data);
    return 0;
}

int
unzip_file (zip *z, const char *name)
{
    struct zipfile *zfile;
    FILE *file_to_write;
    char *fbuf;

    zfile = find_file (z, name);
    if (!zfile) return ZIP_NOFILE;

    seek_file (z, zfile);

    file_to_write = fopen (name, "wb");

    if (file_to_write) {
        fbuf = malloc (zfile->real_size);

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
            zs.next_out = fbuf;
            zs.avail_out = zfile->real_size;
            inflateInit2 (&zs, -MAX_WBITS);
            inflate (&zs, Z_FINISH);
            inflateEnd (&zs);
            free (zip_buf);
        } else {
            fread (fbuf, zfile->real_size, 1, z->f);
        }

        printf (" writing: %s with size: %lu byte\n", name, zfile->real_size);
        fwrite (fbuf, zfile->real_size, 1, file_to_write);
        fclose(file_to_write);
        free(fbuf);

    } else {
        printf (" Could not open %s to write\n", name);
    }

    return 0;
}

int
get_zip_info (zip *z)
{
    printf(" cd_pos = %lu\n cd_size = %lu\n cd_offset = %lu\n head_size = %lu\n rem_size = %lu\n nr_files = %lu\n", \
            z->cd_pos, \
            z->cd_size, \
            z->cd_offset, \
            z->head_size, \
            z->rem_size, \
            z->nr_files );

    return 0;
}

int add_time_comment (zip *z)
{
    unsigned long endof_cdsize = 22; // endof_cdsize is till comment size starts
    unsigned long comment_size = 32;
    char comment_data[2];
    time_t ttmp;

    char comment[comment_size];

    comment_data[1] = comment_size >> 8;
    comment_data[0] = comment_size - comment_data[1] * 256;

    ttmp = time(NULL);
    memset(comment, 0, sizeof(comment));
    sprintf(comment, "%s", ctime(&ttmp));

    // write comment size
    fseek (z->f, z->cd_pos + endof_cdsize, SEEK_SET);
    if (fwrite (comment_data, 2, 1, z->f) != 1) return ZIP_EWRITE;

    // and the comment
    fseek (z->f, 2, SEEK_CUR);
    if (fwrite (comment, comment_size, 1, z->f) != 1) return ZIP_EWRITE;

    return 0;
}


int
main (int argc, char *argv[])
{
    int e,i;
    zip *z;
    char attribs[11];

    if (argc > 1) {
        if (argv[2] == NULL) {
            printf (" You must enter the ZIP file name\n");
            return 1;
        }

        if (strcmp(argv[1], "list") == 0) {
            z = zip_open (argv[2], &e, AC_READ);
            if (e) {
                printf ("%s\n", zip_error(e));
                return 1;
            }

            printf (" %lu files\n", z->nr_files);

            for (i=0; i < z->nr_files; i++) {
                printf ("\n %s\n", z->files->name);
                zip_get_attrib (z, z->files->name);

                if (z->files->xattr) {
                    parse_xattr (z->files->xattr, attribs);
                }

                printf ("   Real Size = %lu byte\n   Zip Size  = %lu byte\n", 
                        z->files->real_size, z->files->zip_size);

                if (z->files->os_made_by == 3) {
                    printf ("   Has Unix Attribs = %s\n", attribs);
                }

                z->files = z->files->next;
            }

            zip_close (z);
            return 0;
        }

        if (strcmp(argv[1], "get") == 0) {
            z = zip_open (argv[2], &e, AC_READ);
            if (e) {
                printf ("%s\n", zip_error(e));
                return 1;
            }

            if (argc != 4) {
                printf (" Usage : %s get <zip_file> <file_to_extract>\n", argv[0]);
                return 1;
            }

            e = unzip_file (z, argv[3]);

            if (e) {
                printf ("%s\n", zip_error(e));
                return 1;
            }

            zip_close (z);
            return 0;
        }

        if (strcmp(argv[1], "scramble") == 0) {
            z = zip_open (argv[2], &e, AC_APPEND);
            if (e) {
                printf ("%s\n", zip_error(e));
                return 1;
            }

            if (argc != 3) {
                printf (" Usage : %s scramble <zip_file>\n", argv[0]);
                return 1;
            }

            printf ("Scrambling %s \n", argv[2]);
            //const char comment[] = *argv[3];

            e = add_time_comment (z);
            if (e) {
                printf ("%s\n", zip_error(e));
                return 1;
            }

            zip_close (z);
            return 0;
        }

        if (strcmp(argv[1], "info") == 0) {
            z = zip_open (argv[2], &e, AC_APPEND);
            if (e) {
                printf ("%s\n", zip_error(e));
                return 1;
            }

            e = get_zip_info (z);
            if (e) {
                printf ("%s\n", zip_error(e));
                return 1;
            }

            zip_close (z);
            return 0;
        }

    }

    printf (" Usage : %s <list/get/info/scramble> <zip_file> [file_to_extract]\n", argv[0]);
    return 1;
}


