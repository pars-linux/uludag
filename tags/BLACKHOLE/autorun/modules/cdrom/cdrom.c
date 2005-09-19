/**
 * @file cdrom.c
 * @brief CDROM module for autorun.
 *
 * All routines for CDROM
 *
 * Copyright (c) 2005, TUBITAK/UEKAE
 * @author S.Çağlar Onur <caglar@uludag.org.tr>
 *
 * Copyright 2002 Xandros Corporation.  All rights reserved.
 * @author Richard Rak
 *
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 *
 */

#include <sys/types.h>
#include <sys/stat.h>
#include <linux/cdrom.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include "module.h"
#include "autorun.h"

DISK_TYPE checkDevice(device_map *device);
char *getISOVolume(const device_map *const device);
int verifyDevice(device_map *device);

autorun_module moduleMapping =
{
    type: "cdrom",
    check: checkDevice,
    verify: verifyDevice,
    volumeLabel: getISOVolume,
};

DISK_TYPE checkDevice(device_map *device)
{
    int status = 0;
    dvd_struct dvd;


    if (device->fd == -1)
    {
        device->fd = open(device->device, O_RDONLY | O_NONBLOCK);
        if (device->fd == -1)
        {
            return UNKNOWN;
        }
    }

    /* Query the drive status */
    if (ioctl(device->fd, CDROM_DRIVE_STATUS) != CDS_DISC_OK)
    {
        return UNKNOWN;
    }

    if ((status = ioctl(device->fd, CDROM_DISC_STATUS)) < 0)
    {
        return UNKNOWN;
    }

    //Assume the default is DVDs have copyrights 
    device->copyright = 1;  //This info only gets passed to DVD handler, not CD
    if (ioctl(device->fd, DVD_READ_STRUCT, &dvd) == 0)
    {
        if ((dvd.copyright.cpst != 0) || (dvd.copyright.rmi != 0))
            device->copyright = 1;
        else
            device->copyright = 0;
        //No error if this call fails
    }

    switch (status)
    {
        /* No valid data disc */
        case CDS_NO_DISC:
        case CDS_NO_INFO:
        {
            return UNKNOWN;
        }
        case CDS_AUDIO:
        {
            close(device->fd);
            device->fd = -1;
            return AUDIO;
        }
        /* A disk was found... but what type? */
        case CDS_DATA_1:
        case CDS_DATA_2:
        {
            close(device->fd);
            device->fd = -1;
            return DATA;
        }
        case CDS_MIXED:
          {
            close(device->fd);
            device->fd = -1;
            return MIXED;
        }
        /* Unknown or unsupported drive state (XA?) */
        default:
        {
            return UNKNOWN;
        }
    }
}

/*
 * Verify that the device node requested is a valid CDROM device.
 *
 * @param device The device_map to check.
 *
 * @return 0 if the device node is not valid.
 */
int verifyDevice(device_map *device)
{
    int fd;

    fd = open(device->device, O_RDONLY | O_NONBLOCK);
    if (fd == -1)
    {
        return 0;
    }
    if (ioctl(fd, CDROM_DRIVE_STATUS) < 0)
    {
        close(fd);
        return 0;
    }
    close(fd);
    return -1;
}

/*
 * Retrieve an ISO 9660 volume label from a device and return it.
 *
 * @param device The device_map to retrieve the volume label for.
 *
 * @return A malloc()'d string containing the volume label for the device.
 */
char *getISOVolume(const device_map *const device)
{
    int fd = 0;
    int status = 0;
    char *buffer = malloc(sizeof(char)*33);
    if (!buffer)
    {
        return "";
    }
    memset(buffer, 0, sizeof(char)*33);

    fd = open(device->device, O_RDONLY | O_NONBLOCK);
    if (fd == -1)
    {
        free(buffer);
        return "";
    }

    status = lseek(fd, 32808, SEEK_SET);
    if (status == -1)
    {
        free(buffer);
        close(fd);
        return "";
    }

    status = read(fd, buffer, 32);
    if (status == -1)
    {
        free(buffer);
        close(fd);
        return "";
    }

    DPRINTF("Volume label for %s is %s.\n", device->device, buffer);
    close(fd);
    return buffer;
}
