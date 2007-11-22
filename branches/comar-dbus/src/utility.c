/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/stat.h>

#include "cfg.h"
#include "utility.h"

const char *valid_app_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-+";
const char *valid_interface_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.";
const char *path_prefix = "/package/";

unsigned char *
load_file(const char *fname, int *sizeptr)
{
    FILE *f;
    struct stat fs;
    size_t size;
    unsigned char *data;

    if (stat(fname, &fs) != 0) return NULL;
    size = fs.st_size;
    if (sizeptr) *sizeptr = size;

    data = malloc(size + 1);
    if (!data) return NULL;
    memset(data, 0, size + 1);

    f = fopen(fname, "rb");
    if (!f) {
        free(data);
        return NULL;
    }
    if (fread(data, size, 1, f) < 1) {
        free(data);
        return NULL;
    }
    fclose(f);

    return data;
}

int
in_str(const char chr, const char *str)
{
    int i;

    for (i = 0; i < strlen(str); i++) {
        if (str[i] == chr) {
            return 1;
        }
    }
    return 0;
}

int
check_interface_format(const char *interface)
{
    int i;

    for (i = 0; i < strlen(interface); i++) {
        if (!in_str(interface[i], valid_interface_chars)) {
            return 0;
        }
    }
    return 1;
}

int
check_path_format(const char *path)
{
    int i;

    if (strncmp(path, path_prefix, strlen(path_prefix))) {
        return 0;
    }

    for (i = strlen(path_prefix); i < strlen(path); i++) {
        if (!in_str(path[i], valid_app_chars)) {
            return 0;
        }
    }
    return 1;
}

char *
str_lshift(const char *str, int num)
{
    char *new_str, *old_str, *t, *t2;
    int size;
    old_str = strdup(str);

    size = strlen(old_str) - num + 1;
    new_str = malloc(size);

    for (t = old_str + num, t2 = new_str; *t != '\0'; t++, t2++) {
        *t2 = *t;
    }
    *t2 = '\0';

    free(old_str);

    return new_str;
}

char *
get_script_path(const char *interface, const char *path)
{
    char *realpath, *model, *app, *t, *t2;
    int size;

    model = strdup(interface);

    // Get application name from object path
    app = str_lshift(path, strlen(path_prefix));

    size = strlen(cfg_data_dir) + 6 + strlen(model) + 1 + strlen(app) + 4;
    realpath = malloc(size);

    // Get model name from interface
    for (t = model; *t != '\0'; t++) {
        if (*t == '.') {
            *t = '_';
        }
    }

    // Generate script path
    snprintf(realpath, size, "%s/code/%s_%s.py", cfg_data_dir, model, app);
    free(app);
    free(model);
    return realpath;
}
