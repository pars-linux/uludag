/*
** Copyright (c) 2006-2009 TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <string.h>

#define BUS_PCI                 0x01
#define BUS_USB                 0x02
#define DEVICE_PRIMARY_VGA      0x04
#define DEVICE_MASS_STORAGE     0x08

extern int cfg_debug;

struct list {
    struct list *next;
    char *data;
    int type;
};


int list_has(struct list *listptr, const char *data);
struct list *list_add(struct list *listptr, const char *data, int type);

void debug(const char *msg);
void *zalloc(size_t size);
char *concat(const char *str, const char *append);
char *my_readlink(const char *path);
char *sys_value(const char *path, const char *value);
int fnmatch(const char *p, const char *s);

struct list *module_get_list(int bustype);
int module_probe(const char *name);

int probe_pci_modules(void);
int probe_drm_modules(void);
int probe_usb_modules(int *has_scsi_storage);

int devnode_mknod(const char *name, int major, int minor);
int create_block_devnodes(void);

/*struct list *scsi_get_list(void);*/
