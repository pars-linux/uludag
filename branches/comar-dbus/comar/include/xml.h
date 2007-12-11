/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

int xml_export_nodes(char *nodes, char **bufferp);
int xml_export_apps(char **bufferp);
int xml_export_interfaces(char *app, char **intros);
int xml_export_system(char **intros);
