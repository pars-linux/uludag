/*
** Copyright (c) 2005-2006, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#ifndef MODEL_H
#define MODEL_H 1

#define P_GLOBAL 1
#define P_PACKAGE 2
#define P_DELETE 4
#define P_STARTUP 8

#define ACL_DENY 0
#define ACL_GUEST 1
#define ACL_USER 2
#define ACL_ADMIN 4

extern int model_max_notifications;
extern int model_nr_nodes;

int model_init(void);
int model_lookup_class(const char *path);
int model_lookup_method(const char *path);
int model_lookup_notify(const char *path);
int model_parent(int node_no);
const char *model_get_method(int node_no);
const char *model_get_path(int node_no);

int model_has_argument(int node_no, const char *argname);
int model_flags(int node_no);
int model_has_instances(int node_no);
int model_is_instance(int node_no, const char *argname);
const char *model_instance_key(int node_no);

int model_next_class(int *class_nop);
void model_acl_set(int node_no, void *acldata);
void model_acl_get(int node_no, void **acldatap, unsigned int *levelp);


#endif /* MODEL_H */
