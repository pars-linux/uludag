/**
 * @file module.c
 * @brief Helper routines for loading modules and mapping devices to modules.
 *
 * File containing code to glue modules and devices together, as well as load
 * modules from the default directory location.
 *
 * Copyright (c) 2005, TUBITAK/UEKAE
 * @author S.Çağlar Onur <caglar@uludag.org.tr>
 *
 * Copyright 2001 Xandros Corporation.  All rights reserved.
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

#include <sys/types.h>
#include <dirent.h>
#include <dlfcn.h>
#include <unistd.h>
#include "autorun.h"

/*
 * Load all modules in LIBDIR and resolv mappings between devices and modules.
 *
 * @return 0 if an error occured, otherwise -1.
 */
int loadModules()
{
    DIR *dir = opendir(LIBDIR);
    struct dirent *entry = 0;
    if (!dir)
    {
        return 0;
    }
    entry = readdir(dir);
    while (entry)
    {
        if (!strncmp(entry->d_name, "libautorun_", 11))
        {
            char *lib = malloc(sizeof(char) * (strlen(LIBDIR) + strlen(entry->d_name) + 2));
            device_map *device = deviceSettings;
            void *handle = 0;
            autorun_module *module = 0;
            if (!lib)
            {
                closedir(dir);
                return 0;
            }
            sprintf(lib, "%s/%s", LIBDIR, entry->d_name);
            handle = dlopen(lib, RTLD_NOW);
            if (!handle)
            {
                fprintf(stderr, "Could not resolve symbols in %s.\n", lib);
                fprintf(stderr, "The symbol that failed was %s.\n", dlerror());
                closedir(dir);
                free(lib);
                return 0;
            }
            module = dlsym(handle, "moduleMapping");
            if (!module)
            {
                fprintf(stderr, "Could not resolve requried symbol \"moduleMapping\" in %s.\n", entry->d_name);
                closedir(dir);
                free(lib);
                return 0;
            }
            while (device)
            {
                if (!strcmp(device->deviceType, module->type))
                {
                    DPRINTF("Mapping for device type \"%s\" found in \"%s\".\n", device->deviceType, lib);
                    //ASW possibly put copyright info here then insert into device data structure
                    device->module = module;
                }
                device = (device_map *)device->next;
            }
            free(lib);
        }
        entry = readdir(dir);
    }
    closedir(dir);
    return -1;
}

