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
#include <time.h>
#include <sys/stat.h>

#include "cfg.h"
#include "utility.h"

const char *valid_app_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-+";
const char *valid_model_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.";

char *
strsub(char *str, int start, int end)
{
    if (start < 0) {
        start = strlen(str) + start;
    }
    else if (start > strlen(str)) {
        end = strlen(str);
    }
    if (end == 0) {
        end = strlen(str);
    }
    else if (end < 0) {
        end = strlen(str) + end;
    }
    else if (end > strlen(str)) {
        end = strlen(str);
    }

    char *new_src, *t;
    new_src = malloc(end - start + 2);
    for (t = str + start; t < str + end; t++) {
        new_src[t - (str + start)] = *t;
    }
    new_src[t - (str + start)] = '\0';
    return new_src;
}

char *
strrep(char *str, char old, char new)
{
    char *new_str, *t;

    new_str = strdup(str);

    for (t = new_str; *t != '\0'; t++) {
        if (*t == old) {
            *t = new;
        }
    }

    return new_str;
}

int
check_file(const char *fname)
{
    struct stat fs;
    return (stat(fname, &fs) == 0);
}

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
save_file(const char *fname, const char *buffer, size_t size)
{
    /*!
    @return Returns -1 if file could not be opened for binary writing \n
    Returns -2 if file could not be written to disc or buffer is empty \n
    Returns 0 on success
    */

    FILE *f;

    f = fopen(fname, "wb");
    if (!f) return -1;
    if (fwrite(buffer, size, 1, f) < 1) {
        fclose(f);
        return -2;
    }
    fclose(f);
    return 0;
}

int
check_model_name(const char *model)
{
    int i;

    if (model == NULL) {
        return 0;
    }

    for (i = 0; i < strlen(model); i++) {
        if (strchr(valid_model_chars, model[i]) == NULL) {
            return 0;
        }
    }
    return 1;
}

int
check_app_name(const char *app)
{
    int i;

    if (app == NULL) {
        return 0;
    }

    for (i = 0; i < strlen(app); i++) {
        if (strchr(valid_model_chars, app[i]) == NULL) {
            return 0;
        }
    }
    return 1;
}

char *
get_xml_path(const char *model)
{
    char *realpath, *model_escaped, *t, *t2;
    int size;

    size = strlen(cfg_config_dir) + 1 + strlen("introspections") + 1 + strlen(model) + 5;
    realpath = malloc(size);

    model_escaped = (char *) strrep(model, '.', '_');

    // Generate script path
    snprintf(realpath, size, "%s/introspections/%s.xml\0", cfg_config_dir, model_escaped);
    free(model_escaped);
    return realpath;
}

char *
get_script_path(const char *app, const char *model)
{
    char *realpath, *model_escaped, *t, *t2;
    int size;

    size = strlen(cfg_data_dir) + 1 + strlen("code") + 1 + strlen(model) + 1 + strlen(app) + 4;
    realpath = malloc(size);

    model_escaped = (char *) strrep(model, '.', '_');

    // Generate script path
    snprintf(realpath, size, "%s/code/%s_%s.py\0", cfg_data_dir, model_escaped, app);
    free(model_escaped);
    return realpath;
}

unsigned long
time_diff(struct timeval *start, struct timeval *end)
{
    unsigned long msec;

    msec = (end->tv_sec * 1000) + (end->tv_usec / 1000);
    msec -= (start->tv_sec * 1000) + (start->tv_usec / 1000);
    return msec;
}
