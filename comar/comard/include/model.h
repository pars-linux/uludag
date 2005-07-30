/*
** Copyright (c) 2005, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#ifndef MODEL_H
#define MODEL_H 1

int model_init(void);
int model_lookup_class(const char *path);
int model_lookup_method(const char *path);
int model_parent(int node_no);
const char *model_get_method(int node_no);
const char *model_get_path(int node_no);


#endif /* MODEL_H */
