/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdlib.h>
#include <Python.h>
#include <dirent.h>

#include "cfg.h"
#include "utility.h"

char *model_list;

int
model_init()
{
    DIR *pDIR;
    struct dirent *pDirEnt;

    char *model_dir, *model, *extension;
    int size;

    size = strlen(cfg_config_dir) + 1 + strlen("introspections/") + 1;
    model_dir = malloc(size);
    snprintf(model_dir, size, "%s/introspections/\0", cfg_config_dir);

    pDIR = opendir(model_dir);
    free(model_dir);
    if (pDIR == NULL) {
        return 1;
    }

    size = 1;
    model_list = malloc(size);
    snprintf(model_list, 1, "\0");

    pDirEnt = readdir(pDIR);
    while (pDirEnt != NULL) {
        model = strsub(pDirEnt->d_name, 0, -4);
        extension = strsub(pDirEnt->d_name, -4, 0);
        if (strcmp(model, "Comar") != 0 && strcmp(extension, ".xml") == 0) {
            size = size + strlen(model) + 1;
            model_list = realloc(model_list, size);
            strncat(model_list, "|", 1);
            strncat(model_list, model, strlen(model));
        }
        free(model);
        free(extension);
        pDirEnt = readdir(pDIR);
    }

    closedir(pDIR);

    return 0;
}
