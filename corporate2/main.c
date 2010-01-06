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
#include <stdlib.h>
#include "common.h"

int cfg_debug = 0;
int cfg_drm = 0;
int cfg_wait_storage = 0;

int main(int argc, char *argv[])
{
    int has_scsi_storage = 0, i = 0;

    /* Parse command line arguments */
    for (i = 1; i < argc; ++i) {
        cfg_drm   = !strcmp(argv[i], "--drm")   ? 1 : cfg_drm;
        cfg_debug = !strcmp(argv[i], "--debug") ? 1 : cfg_debug;
        cfg_wait_storage = !strcmp(argv[i], "--wait-for-storage") ? 1 : cfg_wait_storage;
    }

    if (cfg_drm)
        /* Early call for KMS stuff */
        exit(probe_drm_modules());

    /* Probe PCI modules */
    probe_pci_modules();

    /* Second, load USB modules */
    probe_usb_modules(&has_scsi_storage);

    /* Then, check if there is a need for scsi disk/cdrom drivers
     * If these are on usb bus, they need some time to properly
     * setup, so we wait a little bit.
     */
    if (cfg_wait_storage && has_scsi_storage) {
        debug("Waiting 3 seconds for USB mass storage devices to settle...");
        sleep(3);
    }

    /* Create device nodes for disks/partitions */
    create_block_devnodes();

    return 0;
}
