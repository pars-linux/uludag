/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <string.h>

#include "data.h"
#include "iksemel.h"
#include "utility.h"

int
xml_export_nodes(char *nodes, char **bufferp)
{
    iks *xml = NULL, *item;
    xml = iks_new("node");

    char *t, *s;
    for (t = nodes; t; t = s) {
        s = strchr(t, '/');
        if (s) {
            *s = '\0';
            ++s;
        }
        item = iks_insert(xml, "node");
        iks_insert_attrib(item, "name", t);
    }

    *bufferp = iks_string(NULL, xml);

    return 0;
}

int
xml_export_apps(char **bufferp)
{
    char *apps;
    db_get_apps(&apps);
    return xml_export_nodes(apps, bufferp);
}

int
xml_export_interfaces(char *app, char **intros)
{
    int size;
    char *models;
    char *model_xml;
    db_get_models(app, &models);

    size = strlen("<node></node>") + 1;
    *intros = malloc(size);
    snprintf(*intros, 7, "<node>\0");

    char *t, *s;
    for (t = models; t; t = s) {
        s = strchr(t, '/');
        if (s) {
            *s = '\0';
            ++s;
        }

        model_xml = (char*) load_file(get_xml_path(t), NULL);

        if (model_xml == NULL) {
            log_error("Missing introspection data for '%s'\n", t);
            continue;
        }

        size = size + strlen(model_xml);
        *intros = (char *) realloc(*intros, size);
        strncat(*intros, model_xml, strlen(model_xml));
        free(model_xml);
    }

    free(models);
    strncat(*intros, "</node>", 7);

    return 0;
}
