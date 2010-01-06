/*
** Copyright (c) 2006-2009 TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <string.h>

extern int cfg_debug;

struct list {
    struct list *next;
    char *data;
    int priority;
};

int list_has(struct list *listptr, const char *data);
struct list *list_add(struct list *listptr, const char *data, int priority);

void debug(const char *message);
void *zalloc(size_t size);
char *concat(const char *str, const char *append);
char *my_readlink(const char *path);
char *sys_value(const char *path, const char *value);
int fnmatch(const char *p, const char *s);

struct list *module_get_list(const char *syspath);
int module_probe(const char *name);

int probe_pci_modules(void);
int probe_drm_modules(void);
int probe_usb_modules(int *has_scsi_storage);

int devnode_mknod(const char *name, const char *major, const char *minor);
int create_block_devnodes(void);

struct list *scsi_get_list(void);
