/*
** Copyright (c) 2006-2010 TUBITAK/UEKAE
**
** Coldplug program for initramfs
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <unistd.h>
#include "common.h"

int cfg_debug = 0;
int cfg_drm = 0;

int main(int argc, char *argv[])
{
    struct list *modules, *item;
    int has_scsi_storage = 0, i = 0;

    /* Parse command line arguments */
    for (i = 1; i < argc; ++i) {
        cfg_drm   = !strcmp(argv[i], "--drm")   ? 1 : cfg_drm;
        cfg_debug = !strcmp(argv[i], "--debug") ? 1 : cfg_debug;
    }

    /* First, load PCI modules. Load DRM ones only if cfg_drm is set */
    probe_pci_modules(cfg_drm);

    if (!cfg_drm) {

        /* Second, load USB modules */
        probe_usb_modules(&has_scsi_storage);

        /* Then, check if there is a need for scsi disk/cdrom drivers
         * If these are on usb bus, they need some time to properly
         * setup, so we wait a little bit.
         */
        if (has_scsi_storage) {
            debug("has_scsi_storage is true, sleeping for 2 seconds..");
            sleep(2);
        }
        modules = scsi_get_list();
        for (item = modules; item; item = item->next)
            module_probe(item->data);

        /* Populate /dev directory for probed disk/cdrom devices
         * Again, wait a bit for devices to settle.
         */
        if (has_scsi_storage) {
            debug("has_scsi_storage is true, sleeping for 1 second..");
            sleep(1);
        }
        devnode_populate();
    }

    return 0;
}
