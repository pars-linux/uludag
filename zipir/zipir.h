/*
  Copyright (c) 2005-2007 TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#define UNX_IFMT       0170000     /* Unix file type mask */
#define UNX_IFREG      0100000     /* Unix regular file */
#define UNX_IFSOCK     0140000     /* Unix socket (BSD, not SysV or Amiga) */
#define UNX_IFLNK      0120000     /* Unix symbolic link (not SysV, Amiga) */
#define UNX_IFBLK      0060000     /* Unix block special       (not Amiga) */
#define UNX_IFDIR      0040000     /* Unix directory */
#define UNX_IFCHR      0020000     /* Unix character special   (not Amiga) */
#define UNX_IFIFO      0010000     /* Unix fifo    (BCC, not MSC or Amiga) */
#define UNX_ISUID      04000       /* Unix set user id on execution */
#define UNX_ISGID      02000       /* Unix set group id on execution */
#define UNX_ISVTX      01000       /* Unix directory permissions control */
#define UNX_ENFMT      UNX_ISGID   /* Unix record locking enforcement flag */
#define UNX_IRWXU      00700       /* Unix read, write, execute: owner */
#define UNX_IRUSR      00400       /* Unix read permission: owner */
#define UNX_IWUSR      00200       /* Unix write permission: owner */
#define UNX_IXUSR      00100       /* Unix execute permission: owner */
#define UNX_IRWXG      00070       /* Unix read, write, execute: group */
#define UNX_IRGRP      00040       /* Unix read permission: group */
#define UNX_IWGRP      00020       /* Unix write permission: group */
#define UNX_IXGRP      00010       /* Unix execute permission: group */
#define UNX_IRWXO      00007       /* Unix read, write, execute: other */
#define UNX_IROTH      00004       /* Unix read permission: other */
#define UNX_IWOTH      00002       /* Unix write permission: other */
#define UNX_IXOTH      00001       /* Unix execute permission: other */

enum {
        ZIP_OK = 0,
        ZIP_NOMEM,
        ZIP_NOSIG,
        ZIP_BADZIP,
        ZIP_NOMULTI,
        ZIP_EOPEN,
        ZIP_EREAD,
        ZIP_EWRITE,
        ZIP_NOFILE
};

enum {
        AC_READ = 0,
        AC_APPEND
};

struct zipfile {
    struct zipfile *next;
    char *name;
    ulong os_made_by;
    ulong crc;
        ulong zip_size;
        ulong real_size;
    ulong pos;
    long mtime;
    long atime;
    long ctime;
    uid_t uid;
    gid_t gid;
    ulong xattr;
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

typedef struct zip_struct zip;

char *zip_error (int err);

zip *zip_open (const char *fname, int *err, int action);
void zip_close (zip *z);

unsigned long zip_get_size (zip *z, const char *name);
int unzip_file (zip *z, const char *name);

