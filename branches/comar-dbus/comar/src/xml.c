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
    t = strdup(nodes);
    for (; t; t = s) {
        s = strchr(t, '|');
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
    char *models, *model_xml, *xml_path;

    db_get_models(app, &models);

    size = strlen("<node></node>") + 1;
    *intros = malloc(size);
    snprintf(*intros, 7, "<node>\0");

    char *t, *s;
    t = strdup(models);
    for (; t; t = s) {
        s = strchr(t, '|');
        if (s) {
            *s = '\0';
            ++s;
        }

        xml_path = get_xml_path(t);
        model_xml = (char*) load_file(xml_path, NULL);
        free(xml_path);

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

int
xml_export_system(char **intros)
{
    int size;
    char *model_xml, *xml_path;

    size = strlen("<node></node>") + 1;
    *intros = malloc(size);
    snprintf(*intros, 7, "<node>\0");

    xml_path = get_xml_path("Comar");
    model_xml = (char*) load_file(xml_path, NULL);
    free(xml_path);

    if (model_xml == NULL) {
        log_error("Missing introspection data for 'Comar'\n");
        return 1;
    }

    size = size + strlen(model_xml);
    *intros = (char *) realloc(*intros, size);
    strncat(*intros, model_xml, strlen(model_xml));
    free(model_xml);

    strncat(*intros, "</node>", 7);

    return 0;
}
