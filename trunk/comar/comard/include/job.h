/*
** Copyright (c) 2005, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#ifndef JOB_H
#define JOB_H 1

int job_start_register(int node_no, const char *app, const char *csl_file);
int job_start_execute(int node_no, const char *app);


#endif /*JOB_H */
