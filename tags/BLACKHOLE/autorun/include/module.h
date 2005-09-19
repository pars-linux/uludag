/**
 * @file module.h
 * @brief Definition file containing all information required for a module.
 *
 * File containing module definitions.
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
 *
 */

#ifndef __MODULE_H
#define __MODULE_H

#include "device.h"

//typedef (char *) volume;

struct _autorun_module
{
	char *type;                     	/* Module name (eg:  "cdrom") */
	DISK_TYPE (*check)(device_map *);	/* Routine to check a device */
	int (*verify)(device_map *);		/* Routine to validate device type */
	char *(*volumeLabel)(const device_map *const);	/* Routine to retrieve the volume label from a device. */
};

/*
 * Load modules and resolv dependencies.
 */
extern int loadModules();

#endif /* __MODULE_H */
