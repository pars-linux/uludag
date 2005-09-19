/**
 * @file device.h
 * @brief Header file containing function declarations for device handling.
 *
 * File containing common definitions and data structures for autorun devices.
 *
 * Copyright (c) 2005, TUBITAK/UEKAE
 * @author S.Çağlar Onur <caglar@uludag.org.tr>
 *
 * Copyright 2002 Xandros Corporation.  All rights reserved.
 * @author Richard Rak <rakr@xandros.com>
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

#ifndef __DEVICE_H
#define __DEVICE_H

#include <sys/types.h>

typedef struct _autorun_module autorun_module;

#define MAXOPTIONS 16

enum _DISK_TYPE
{
    UNKNOWN = 0,
    DATA,
    WINE,
    WINE_OFFICE,
    LOKI,
    MIXED,
    AUDIO,
    VCDVIDEO,
    VIDEO
};
typedef enum _DISK_TYPE DISK_TYPE;

enum _STATUS
{
    NOT_READY = 0,
    READY
};
typedef enum _STATUS STATUS;

struct _program_map
{
    char *script;
    char *options[MAXOPTIONS + 1];
    int enabled;
    pid_t PID;
    DISK_TYPE diskType;
    volatile struct _program_map *next;
};
typedef struct _program_map program_map;

struct _device_map
{
    char *device;
    char *volume;
    char *deviceType;
    char *mountPoint;
    autorun_module *module;
    int fd;
    int copyright;
    STATUS status;
    struct _program_map *programs;
    volatile struct _device_map *next;
};
typedef struct _device_map device_map;

extern device_map *freeDevice(device_map *device);
extern device_map *findDevice(const device_map *const top, const char *const device);
extern device_map *allocDevice(device_map *top, const char *const device);

extern int updateDevice(device_map *const device, const char *const key, const char *const value, const char *const option);

extern program_map *allocProgram(device_map *device, const DISK_TYPE disk);
extern int updateProgram(program_map *program, const DISK_TYPE disk, const char *const script, const char *const option);

#endif /* __DEVICE_H */
