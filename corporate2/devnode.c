/*
** Copyright (c) 2006-2009, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "common.h"

static void ensure_path(char *path)
{
    struct stat fs;
    char *t, *cur;

    path = strdup(path);
    cur = path;
    if (path[0] == '/') ++cur;
    while (1)
    {
        t = strchr(cur, '/');
        if (!t) break;
        *t = '\0';
        if (stat(path, &fs) != 0) {
            mkdir(path, 0755);
        }
        *t = '/';
        cur = t + 1;
    }
}

int devnode_mknod(const char *name, int major, int minor)
{
    char *path, *t;
    int ret;

    /* Construct devpath */
    path = concat("/dev/", name);

    /* Normalize path */
    for (t=path; *t != '\0'; t++) {
         if (*t == '!') *t = '/';
    }

    /* Create device node */
    ensure_path(path);
    debug(concat("Calling mknod for ", path));
    if ((ret = mknod(path, S_IFBLK, makedev(major, minor))) < 0)
        perror("devnode_mknod");

    return ret;
}

static int mknod_disk_partitions(char *dev)
{
    char *path;
    DIR *dir;
    struct dirent *dirent;
    char *tmp, *minor;
    int major;

    /* e.g. /sys/block/sda */
    path = concat("/sys/block/", dev);
    dir = opendir(path);
    if (!dir)
        return -1;

    while((dirent = readdir(dir))) {
        char *name = dirent->d_name; /* sdax */
        if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0)
            continue;
        if (strncmp(name, dev, strlen(dev)) != 0)
            continue;
        tmp = concat(concat(path, "/"), name);
        tmp = sys_value(tmp, "dev");
        major = atoi(strtok(tmp, ":"));
        minor = strtok(NULL, "");
        if (minor)
            /* A minor is available, create /dev/sdxy */
            devnode_mknod(name, major, atoi(minor));
        free(tmp);
    }
    closedir(dir);
    return 0;
}

int create_block_devnodes(void)
{
    DIR *dir;
    struct dirent *dirent;
    char *path, *dev, *name, *minor;
    int major;

    dir = opendir("/sys/block");
    if (!dir) return -1;
    while((dirent = readdir(dir))) {
        name = dirent->d_name;
        if (strcmp(name, ".") == 0 || strcmp(name, "..") == 0)
            continue;

        path = concat("/sys/block/", name);
        dev = sys_value(path, "dev");
        major = atoi(strtok(dev, ":"));
        minor = strtok(NULL, "");
        if (minor) {
            /* A minor is available, create /dev/sdx and relevant partitions */
            devnode_mknod(name, major, atoi(minor));
            mknod_disk_partitions(name);
        }
        free(dev);
    }
    closedir(dir);

    return 0;
}

