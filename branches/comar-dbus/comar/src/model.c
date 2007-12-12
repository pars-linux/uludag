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

#include "cfg.h"
#include "iksemel.h"
#include "utility.h"

iks *model_xml;

enum {
    N_INTERFACE,
    N_METHOD,
    N_SIGNAL
};

struct node {
    const char *path;
    const char *method;
    struct node *next;
    int parent_no;
    int type;
    int no;
};

#define TABLE_SIZE 367

static struct node **node_table;
static struct node *nodes;
static char *paths;
int model_nr_nodes;

static int
prepare_tables(int max_nodes, size_t str_size)
{
    nodes = calloc(max_nodes, sizeof(struct node));
    node_table = calloc(TABLE_SIZE, sizeof(struct node *));
    paths = malloc(str_size);
    if (!nodes || !node_table || !paths) return -1;
    return 0;
}

static char *path_ptr = NULL;

static char *
build_path(iks *o, iks *m)
{
    if (path_ptr) {
        path_ptr += strlen(path_ptr) + 1;
    } else {
        path_ptr = paths;
    }

    if (m) {
        sprintf(path_ptr, "%s.%s",
            iks_find_attrib(o, "name"),
            iks_find_attrib(m, "name")
        );
    } else {
        strcpy(path_ptr, iks_find_attrib(o, "name"));
    }

    return path_ptr;
}

static unsigned int
hash_string(const unsigned char *str, int len)
{
    unsigned int h = 0, i;

    for (i = 0; i < len; i++) {
        h = ( h << 5 ) - h + str[i];
    }
    return h;
}

int
model_lookup_interface(const char *iface)
{
    struct node *n;
    int val;

    val = hash_string(iface, strlen(iface)) % TABLE_SIZE;
    for (n = node_table[val]; n; n = n->next) {
        if (N_INTERFACE == n->type && strcmp(n->path, iface) == 0) {
            return n->no;
        }
    }
    return -1;
}

int
model_lookup_method(const char *iface, const char *method)
{
    struct node *n;
    int val, size;
    char *path;

    size = strlen(iface) + 1 + strlen(method) + 1;
    path = malloc(size);
    snprintf(path, size, "%s.%s\0", iface, method);

    val = hash_string(path, strlen(path)) % TABLE_SIZE;
    for (n = node_table[val]; n; n = n->next) {
        if (N_METHOD == n->type && strcmp(n->path, path) == 0) {
            free(path);
            return n->no;
        }
    }
    free(path);
    return -1;
}

int
model_lookup_signal(const char *iface, const char *signal)
{
    struct node *n;
    int val, size;
    char *path;

    size = strlen(iface) + 1 + strlen(signal) + 1;
    path = malloc(size);
    snprintf(path, size, "%s.%s\0", iface, signal);

    val = hash_string(path, strlen(path)) % TABLE_SIZE;
    for (n = node_table[val]; n; n = n->next) {
        if (N_SIGNAL == n->type && strcmp(n->path, path) == 0) {
            free(path);
            return n->no;
        }
    }
    free(path);
    return -1;
}

static int
add_node(int parent_no, const char *path, int type)
{
    /*!
    parent_no is depth of node. adds node with path and type (method)
    to node table
    */

    struct node *n;
    int val;
    int len = strlen(path);

    n = &nodes[model_nr_nodes];
    n->path = path;
    if (type == N_METHOD) {
        n->method = path + len;
        while (n->method[-1] != '.')
            --n->method;
    } else {
        n->method = NULL;
    }
    n->parent_no = parent_no;
    n->type = type;
    n->no = model_nr_nodes++;

    val = hash_string(path, len) % TABLE_SIZE;
    n->next = node_table[val];
    node_table[val] = n;

    return n->no;
}

static int
model_import(const char *model_file)
{
    iks *grp, *obj, *met;
    size_t size = 0;
    size_t obj_size, met_size;
    int obj_no;
    int count = 0;
    int e;

    e = iks_load(model_file, &model_xml);
    if (e != 0) {
        log_error("XML load error.\n");
        return -1;
    }

    if (iks_strcmp(iks_name(model_xml), "comarModel") != 0) {
        log_error("Bad XML: not a Comar model.\n");
        return -1;
    }

    // scan the model
    for (obj = iks_first_tag(model_xml); obj; obj = iks_next_tag(obj)) {
        if (iks_strcmp(iks_name(obj), "interface") == 0) {
            obj_size = iks_strlen(iks_find_attrib(obj, "name"));
            if (!obj_size) {
                log_error("Bad XML: interface has no name.\n");
                return -1;
            }

            size += obj_size + 1;
            ++count;

            for (met = iks_first_tag(obj); met; met = iks_next_tag(met)) {
                if (iks_strcmp(iks_name(met), "method") == 0 || iks_strcmp(iks_name(met), "signal") == 0) {
                    met_size = iks_strlen(iks_find_attrib(met, "name"));
                    if (!met_size) {
                        log_error("Bad XML: method/signal has no name.\n");
                        return -1;
                    }
                    size += obj_size + 1 + met_size + 1;
                    ++count;

                    iks *arg;
                    for (arg = iks_first_tag(met); arg; arg = iks_next_tag(arg)) {
                        if (iks_strcmp(iks_name(arg), "arg") != 0) {
                            log_error("Bad XML: method/signal may contain <arg> only\n");
                            return -1;
                        }
                    }
                }
                else {
                    log_error("Bad XML: interface may contain <method> or <signal> only\n");
                    return -1;
                }
            }
        }
        else {
            log_error("Bad XML: root node may contain <interface> only\n");
            return -1;
        }
    }

    // size is counted to alloc mem for paths
    // prepare data structures
    if (prepare_tables(count, size) != 0) return -1;

    // load model
    for (obj = iks_first_tag(model_xml); obj; obj = iks_next_tag(obj)) {
        if (iks_strcmp(iks_find_attrib(obj, "name"), "Comar") == 0) {
            continue;
        }
        obj_no = add_node(-1, build_path(obj, NULL), N_INTERFACE);
        for (met = iks_first_tag(obj); met; met = iks_next_tag(met)) {
            if (iks_strcmp(iks_name(met), "method") == 0) {
                add_node(obj_no, build_path(obj, met), N_METHOD);
            }
            else if (iks_strcmp(iks_name(met), "signal") == 0) {
                add_node(obj_no, build_path(obj, met), N_SIGNAL);
            }
        }
    }

    // Free xml

    return 0;
}

int
model_get_iks(char *path, iks **parent)
{
    iks *obj, *new;
    for (obj = iks_first_tag(model_xml); obj; obj = iks_next_tag(obj)) {
        if (iks_strcmp(iks_find_attrib(obj, "name"), path) == 0) {
            new = iks_copy(obj);
            if (strcmp(path, "Comar") == 0) {
                iks_insert_attrib(new, "name", cfg_bus_name);
            }
            else {
                int size = strlen(cfg_bus_name) + 1 + strlen(path) + 1;
                char *name = malloc(size);
                snprintf(name, size, "%s.%s\0", cfg_bus_name, path);
                iks_insert_attrib(new, "name", name);
                free(name);
            }
            iks_insert_node(*parent, new);
        }
    }
    return 0;
}

int
model_init()
{
    char *model_file;
    int size, ret;

    size = strlen(cfg_config_dir) + 1 + strlen("model.xml") + 1;
    model_file = malloc(size);
    snprintf(model_file, size, "%s/model.xml\0", cfg_config_dir);

    ret = model_import(model_file);
    free(model_file);

    return ret;
}
