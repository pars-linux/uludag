/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <sys/time.h>

char *strsub(const char *str, int start, int end);
char *strrep(const char *str, char old, char new);

int check_file(const char *fname);
unsigned char *load_file(const char *fname, int *sizeptr);
int save_file(const char *fname, const char *buffer, size_t size);

int check_model_name(const char *model);
int check_app_name(const char *app);
char *get_script_path(const char *interface, const char *path);
char *get_xml_path(const char *model);
unsigned long time_diff(struct timeval *start, struct timeval *end);

int str_in_list(const char *item, char delim, const char *list);
