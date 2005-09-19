/**
 * @file autorun.h
 * @brief Header file containing type definitions for autorun.
 *
 * File containing common definitions and data structures for autorun.
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

#ifndef __AUTORUN_H
#define __AUTORUN_H

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <sys/mount.h>
#include <sys/dir.h>
#include <linux/cdrom.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <syslog.h>
#include <fcntl.h>
#include <signal.h>
#include <wait.h>
#include <ctype.h>
#include <errno.h>
#define _GNU_SOURCE
#include <getopt.h>
#include "module.h"
#include "device.h"
#include "config.h"
#include "utils.h"

#define MAXLINE 2048
#define CHECK_INTERVAL 2

extern device_map *globalSettings;
extern device_map *deviceSettings;
extern int debug;
extern uid_t UID;
extern gid_t GID;
extern pid_t bindPID;
extern int bUserConfig;
extern int bInUserConfig;

#ifdef DEBUG
#define DPRINTF(fmt, args...) fprintf(stderr, fmt, ##args)
#else
#define DPRINTF(...)
#endif

#endif /* __AUTORUN_H */
