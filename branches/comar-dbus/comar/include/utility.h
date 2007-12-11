/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <sys/time.h>

int check_file(const char *fname);
unsigned char *load_file(const char *fname, int *sizeptr);
int check_model_name(const char *model);
int check_app_name(const char *app);
char *get_script_path(const char *interface, const char *path);
char *get_xml_path(const char *model);
unsigned long time_diff(struct timeval *start, struct timeval *end);
char *str_replace(const char *str, const char old, const char new);
char *str_lshift(const char *str, int num);
