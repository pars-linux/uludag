/*
** Copyright (c) 2006-2009, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/utsname.h>

#include "common.h"


struct list* module_get_list(int bustype)
{
    DIR *dir;
    struct dirent *dirent;
    struct list *modules = NULL;
    int type = 0;
    char *path, *modalias;
    char *devtype = NULL, *syspath = NULL;

    switch (bustype) {
        case BUS_PCI:
            syspath = "/sys/bus/pci/devices/";
            break;
        case BUS_USB:
            syspath = "/sys/bus/usb/devices/";
            break;
    }

    /* Open sysfs path for traversal */
    dir = opendir(syspath);
    if (!dir)
        return NULL;

    while((dirent = readdir(dir))) {
        char *name = dirent->d_name;
        if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0)
            continue;
        path = concat(syspath, name);

        /* path is now something like /sys/bus/pci/devices/0000\:01\:00.0/ */
        modalias = sys_value(path, "modalias");

        if (modalias) {
            if (bustype == BUS_PCI) {
                devtype = sys_value(path, "boot_vga");
                type = (devtype && atoi(devtype)==1)?DEVICE_PRIMARY_VGA:0;
            }
            else if (bustype == BUS_USB) {
                devtype = sys_value(path, "bInterfaceClass");
                type = (devtype && atoi(devtype)==8)?DEVICE_MASS_STORAGE:0;
            }
            modules = list_add(modules, modalias, type);
            free(modalias);
            free(devtype);
        }
    }
    closedir(dir);

    return modules;

}

int probe_drm_modules()
{
    struct list *modules, *item;
    modules = module_get_list(BUS_PCI);

    for (item = modules; item; item = item->next) {
        if (item->type == DEVICE_PRIMARY_VGA)
            /* Booted VGA adapter, load driver and quit */
            return system(concat("modprobe ", item->data));
    }

    return 1;
}

int probe_pci_modules()
{
    struct list *modules, *item;
    struct stat st;
    int launch = 0;
    char *cmd;

    modules = module_get_list(BUS_PCI);

    /* Modprobes all modules in one call */
    cmd = concat("modprobe ", "-a ");

    for (item = modules; item; item = item->next) {
        if (stat(concat("/sys/module/",item->data), &st) < 0) {
            cmd = concat(cmd, item->data);
            cmd = concat(cmd, " ");
            ++launch;
        }
    }

    return (launch > 0) ? system(cmd):-1;
}

int probe_usb_modules(int *has_scsi_storage)
{
    struct list *modules, *item;
    int launch = 0;
    char *cmd;

    modules = module_get_list(BUS_USB);

    /* Modprobes all modules in one call */
    cmd = concat("modprobe ", "-a ");

    for (item = modules; item; item = item->next, ++launch) {
        *has_scsi_storage += (item->type == DEVICE_MASS_STORAGE);
        cmd = concat(cmd, item->data);
        cmd = concat(cmd, " ");
    }

    return (launch > 0) ? system(cmd):-1;
}
