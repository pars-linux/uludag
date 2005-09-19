/**
 * @file device.c
 * @brief Functions that perform manipulation of device_map entries.
 *
 * Functions that perform manipulation of device_map entries.
 *
 * Copyright (c) 2005, TUBITAK/UEKAE
 * @author S.Çağlar Onur <caglar@uludag.org.tr>
 *
 * Copyright 2001 Xandros Corporation.  All rights reserved.
 * @author Richard Rak
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
 */

#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include "device.h"
#include "autorun.h"

/**
 * Free a device entry and return a pointer to the next device in the list.
 *
 * @param device A pointer to the device to free.
 *
 * @return A pointer to the next device in the list or NULL if it is the last
 *         device.
 */
device_map *freeDevice(device_map *device)
{
    device_map *retVal = (device_map *)device->next;
    program_map *program = 0;
    if (device->device)
    {
        free(device->device);
        device->device = 0;
    }
    if (device->fd != -1)
    {
        close(device->fd);
        device->fd = -1;
    }
    if (device->volume)
    {
        free(device->volume);
        device->volume = 0;
    }
    if (device->deviceType)
    {
        free(device->deviceType);
        device->deviceType = 0;
    }
    if (device->mountPoint)
    {
        free(device->mountPoint);
        device->mountPoint = 0;
    }
    program = device->programs;
    while (program)
    {
        program_map *nextProgram = (program_map *)program->next;
        int i = 0;
        if (program->script)
        {
            free(program->script);
            program->script = 0;
        }
        program->enabled = 0;
        program->diskType = UNKNOWN;
        while (program->options[i])
        {
            free(program->options[i]);
            program->options[i++] = 0;
        }
        free(program);
        program = nextProgram;
    }
    free(device);
    return retVal;
}

/**
 * Find a device entry based upon the device name.
 *
 * @param top The top of the device list to search.
 * @param device The device node to return a pointer to.
 *
 * @return A pointer to the device found, or NULL if the device does not exist.
 */
device_map *findDevice(const device_map *const top,
                       const char *const device)
{
    const device_map *pDevice = (device_map *)top;
    while (pDevice)
    {
        if (0 == strcmp(device, pDevice->device))
        {
            return (device_map *)pDevice;
        }
        pDevice = (device_map *)pDevice->next;
    }
    return NULL;
}

/**
 * Allocate a device and add it to the end of a list.
 *
 * @param top A pointer to the top of the list to add the device to.
 * @param device A string containing the new device node to add.
 *
 * @return A pointer to the newly added device, or NULL if an error occured.
 */
device_map *allocDevice(device_map *top, const char *const device)
{
    device_map *pDevice = top;
    device_map *pNewDevice = 0;

    if (pDevice != 0)
    {
        while (pDevice->next)
        {
            pDevice = (device_map *)pDevice->next;
        }
    }

    pNewDevice = malloc(sizeof(device_map));
    if (pNewDevice == NULL)
    {
        return NULL;
    }
    memset(pNewDevice, 0, sizeof(device_map));
    if (pDevice != 0)
    {
        pDevice->next = pNewDevice;
    }
    pNewDevice->device = strdup(device);
    if (!pNewDevice->device)
    {
        free(pNewDevice);
        return NULL;
    }
    pNewDevice->fd = -1;
    return pNewDevice;
}

/**
 * Update a device entry using the options specified.
 *
 * @param device A pointer to the device map to modify.
 * @param key The option to set.
 * @param value The option value to use.
 * @param option Any extra command line options to add.
 */
int updateDevice(device_map *const device, const char *const key,
                 const char *const value, const char *const option)
{
    device_map *pDevice = (device_map *)device;
    int retVal = 0;
    if (!strcmp(key, "user-config-enabled"))
    {
        if (!strcasecmp(value, "no"))
        {
            bUserConfig = 0;
        }
        retVal = 1;
    }
    else if (!strcmp(key, "wine-script"))
    {
        program_map *pProgram = allocProgram(pDevice, WINE);
        if (pProgram)
        {
            if (bInUserConfig && !option)
            {
                int i = 0;
                if (pProgram->script)
                {
                    free(pProgram->script);
                    pProgram->script = 0;
                }
                while (pProgram->options[i])
                {
                    free(pProgram->options[i]);
                    pProgram->options[i++] = 0;
                }
            }
            if (updateProgram(pProgram, WINE, value, option))
            {
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "wine-office-script"))
    {
        program_map *pProgram = allocProgram(pDevice, WINE_OFFICE);
        if (pProgram)
        {
            if (bInUserConfig && !option)
            {
                int i = 0;
                if (pProgram->script)
                {
                    free(pProgram->script);
                    pProgram->script = 0;
                }
                while (pProgram->options[i])
                {
                    free(pProgram->options[i]);
                    pProgram->options[i++] = 0;
                }
            }
            if (updateProgram(pProgram, WINE_OFFICE, value, option))
            {
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "dvd-video"))
    {
        program_map *pProgram = allocProgram(pDevice, VIDEO);
        if (pProgram)
        {
            if (bInUserConfig && !option)
            {
                int i = 0;
                if (pProgram->script)
                {
                    free(pProgram->script);
                    pProgram->script = 0;
                }
                while (pProgram->options[i])
                {
                    free(pProgram->options[i]);
                    pProgram->options[i++] = 0;
                }
            }
            if (updateProgram(pProgram, VIDEO, value, option))
            {
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "vcd-video"))
    {
        program_map *pProgram = allocProgram(pDevice, VCDVIDEO);
        if (pProgram)
        {
            if (bInUserConfig && !option)
            {
                int i = 0;
                if (pProgram->script)
                {
                    free(pProgram->script);
                    pProgram->script = 0;
                }
                while (pProgram->options[i])
                {
                    free(pProgram->options[i]);
                    pProgram->options[i++] = 0;
                }
            }
            if (updateProgram(pProgram, VCDVIDEO, value, option))
            {
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "cd-audio"))
    {
        program_map *pProgram = allocProgram(pDevice, AUDIO);
        if (pProgram)
        {
            if (bInUserConfig && !option)
            {
                int i = 0;
                if (pProgram->script)
                {
                    free(pProgram->script);
                    pProgram->script = 0;
                }
                while (pProgram->options[i])
                {
                    free(pProgram->options[i]);
                    pProgram->options[i++] = 0;
                }
            }
            if (updateProgram(pProgram, AUDIO, value, option))
            {
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "cd-data"))
    {
        program_map *pProgram = allocProgram(pDevice, DATA);
        if (pProgram)
        {
            if (bInUserConfig && !option)
            {
                int i = 0;
                if (pProgram->script)
                {
                    free(pProgram->script);
                    pProgram->script = 0;
                }
                while (pProgram->options[i])
                {
                    free(pProgram->options[i]);
                    pProgram->options[i++] = 0;
                }
            }
            if (updateProgram(pProgram, DATA, value, option))
            {
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "cd-mixed"))
    {
        program_map *pProgram = allocProgram(pDevice, MIXED);
        if (pProgram)
        {
            if (bInUserConfig && !option)
            {
                int i = 0;
                if (pProgram->script)
                {
                    free(pProgram->script);
                    pProgram->script = 0;
                }
                while (pProgram->options[i])
                {
                    free(pProgram->options[i]);
                    pProgram->options[i++] = 0;
                }
            }
            if (updateProgram(pProgram, MIXED, value, option))
            {
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "mount-point"))
    {
       if (!device->mountPoint)
        {
            device->mountPoint = strdup(value);
            retVal = 1;
        }
        else
        {
            free(device->mountPoint);
            device->mountPoint = strdup(value);
            retVal = 1;
        }
    }
    else if (!strcmp(key, "autorun-wine"))
    {
        program_map *pProgram1 = allocProgram(pDevice, WINE);
        program_map *pProgram2 = allocProgram(pDevice, WINE_OFFICE);
        if (pProgram1 && pProgram2)
        {
            if (!strcasecmp(value, "yes"))
            {
                pProgram1->enabled = 1;
                pProgram2->enabled = 1;
                retVal = 1;
            }
            else
            {
                pProgram1->enabled = 0;
                pProgram2->enabled = 0;
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "autorun-loki"))
    {
        program_map *pProgram = allocProgram(pDevice, LOKI);
        if (pProgram)
        {
            if (!strcasecmp(value, "yes"))
            {
                pProgram->enabled = 1;
                retVal = 1;
            }
            else
            {
                pProgram->enabled = 0;
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "autorun-audio"))
    {
        program_map *pProgram = allocProgram(pDevice, AUDIO);
        if (pProgram)
        {
            if (!strcasecmp(value, "yes"))
            {
                pProgram->enabled = 1;
                retVal = 1;
            }
            else
            {
                pProgram->enabled = 0;
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "autorun-video"))
    {
        program_map *pProgram = allocProgram(pDevice, VIDEO);
        if (pProgram)
        {
            if (!strcasecmp(value, "yes"))
            {
                pProgram->enabled = 1;
                retVal = 1;
            }
            else
            {
                pProgram->enabled = 0;
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "autorun-vcd"))
    {
        program_map *pProgram = allocProgram(pDevice, VCDVIDEO);
        if (pProgram)
        {
            if (!strcasecmp(value, "yes"))
            {
                pProgram->enabled = 1;
                retVal = 1;
            }
            else
            {
                pProgram->enabled = 0;
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "autorun-data"))
    {
        program_map *pProgram = allocProgram(pDevice, DATA);
        if (pProgram)
        {
            if (!strcasecmp(value, "yes"))
            {
                pProgram->enabled = 1;
                retVal = 1;
            }
            else
            {
                pProgram->enabled = 0;
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "autorun-mixed"))
    {
        program_map *pProgram = allocProgram(pDevice, MIXED);
        if (pProgram)
        {
            if (!strcasecmp(value, "yes"))
            {
                pProgram->enabled = 1;
                retVal = 1;
            }
            else
            {
                pProgram->enabled = 0;
                retVal = 1;
            }
        }
    }
    else if (!strcmp(key, "type"))
    {
        if (device)
        {
            device->deviceType = strdup(value);
            retVal = 1;
        }
    }

    return retVal;
}

/**
 * Update a program_map entry with the given information.
 *
 * @param pProgram The top-level of the program tree to search for.
 * @param disk The type of entry to edit (see device.h).
 * @param script The name of the program to call.
 * @param option Any options to add to the script command line.
 * @param enable Enable or disable this entry.
 *
 * @return Non-zero on success.
 */
int updateProgram(program_map *program, const DISK_TYPE disk,
                  const char *const script, const char *const option)
{
    int retVal = 0;
    program_map *pProgram = program;
    if (pProgram)
    {
        while (pProgram)
        {
            if (pProgram->diskType == disk)
            {
                if (pProgram->script)
                {
                    free(pProgram->script);
                }
                pProgram->script = strdup(script);
                if (!pProgram->script)
                {
                    fprintf(stderr, "Memory allocation error.\n");
                    return 0;
                }
                if (option)
                {
                    int i = 0;
                    while (pProgram->options[i] && i < MAXOPTIONS)
                    {
                        i++;
                    }
                    if (i != MAXOPTIONS)
                    {
                        pProgram->options[i] = strdup(option);
                        if (!pProgram->options[i])
                        {
                            fprintf(stderr, "Memory allocation error.\n");
                            return 0;
                        }
                    }
                }
                retVal = 1;
                break;
            }
            pProgram = (program_map *)pProgram->next;
        }
        if (retVal == 0)
        {
            pProgram = program;
            while (pProgram->next)
            {
                pProgram = (program_map *)pProgram->next;
            }
            pProgram->next = malloc(sizeof(program_map));
            if (!pProgram->next)
            {
                fprintf(stderr, "Memory allocation error.\n");
                return 0;
            }
            memset((void *)pProgram->next, 0, sizeof(program_map));
            pProgram->next->script = strdup(script);
            if (!pProgram->next->script)
            {
                fprintf(stderr, "Memory allocation error.\n");
                return 0;
            }
            pProgram->next->diskType = disk;
            if (option)
            {
                pProgram->next->options[0] = strdup(option);
                if (!pProgram->next->options[0])
                {
                    fprintf(stderr, "Memory allocation error.\n");
                    return 0;
                }
            }
            retVal = 1;
        }
    }
    return retVal;
}

/**
 * Allocate a new program_map entry and append it to the device specified.
 *
 * @param device A pointer to a device_map to add the entry to.
 * @param disk The type of entry to add.
 *
 * @return Non-zero on success.
 */
program_map *allocProgram(device_map *device, const DISK_TYPE disk)
{
    program_map *retVal = 0;
    if (device)
    {
        if (device->programs)
        {
            program_map *pProgram = device->programs;
            while (pProgram->next)
            {
                /* Hmm... already exists..  return happily */
                if (pProgram->diskType == disk)
                {
                    return pProgram;
                }
                pProgram = (program_map *)pProgram->next;
            }
            /* Hmm... already exists..  return happily */
            if (pProgram->diskType == disk)
            {
                return pProgram;
            }
            pProgram->next = malloc(sizeof(program_map));
            if (!pProgram->next)
            {
                fprintf(stderr, "Memory allocation error.\n");
                return 0;
            }
            memset((void *)pProgram->next, 0, sizeof(program_map));
            pProgram->next->diskType = disk;
            retVal = (program_map *)pProgram->next;
        }
        else
        {
            device->programs = malloc(sizeof(program_map));
            if (!device->programs)
            {
                fprintf(stderr, "Memory allocation error.\n");
                return 0;
            }
            memset(device->programs, 0, sizeof(program_map));
            device->programs->diskType = disk;
            retVal = device->programs;
        }
    }
    return retVal;
}
