/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

unsigned char *load_file(const char *fname, int *sizeptr);
int check_model_format(const char *model);
int check_path_format(const char *path);
char *get_script_path(const char *model, const char *path);
