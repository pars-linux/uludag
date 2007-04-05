/*
** Copyright (c) 2006, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <Python.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

static char *
get_cwd(pid_t pid)
{
	// FIXME: lame function
	char buf[256];
	static char buf2[1024];
	int i;

	sprintf(buf, "/proc/%d/cwd", pid);
	i = readlink(buf, buf2, 1020);
	if (i == -1) {
		return NULL;
	}
	buf2[i] = '\0';
	return buf2;
}

char *
canonical_path(pid_t pid, char *path, int dont_follow)
{
	// FIXME: spaghetti code ahead
	char *canonical = NULL;
	char *pwd = NULL;
	size_t len;
	int flag = 0;

	len = strlen(path);
	// strip last character if it is a dir separator
	if (path[len-1] == '/') {
		path[len-1] = '\0';
	}

	// Special case for very special /proc/self symlink
	// This link resolves to the /proc/1234 (pid number)
	// since we are parent process, we get a diffent view
	// of filesystem if we let realpath to resolve this.
	if (strncmp(path, "/proc/self", 10) == 0) {
		char *tmp;
		tmp = malloc(strlen(path) + 20);
		if (!tmp) return NULL;
		sprintf(tmp, "/proc/%d/%s", pid, path + 10);
		pwd = tmp;
		path = tmp;
	}

	// prepend current dir to the relative paths
	if (path[0] != '/') {
		char *tmp;
		pwd = get_cwd(pid);
		if (!pwd) return NULL;
		tmp = malloc(strlen(path) + 2 + strlen(pwd));
		if (!tmp) return NULL;
		sprintf(tmp, "%s/%s", pwd, path);
		path = tmp;
	}

	// resolve symlinks in the path
	if (!dont_follow) {
		canonical = realpath(path, NULL);
		if (!canonical && errno == ENAMETOOLONG) {
			if (pwd) free(path);
			return NULL;
		}
	}
	if (!canonical) {
		if (dont_follow || errno == ENOENT) {
			char *t;
			t = strrchr(path, '/');
			if (t && t[1] != '\0') {
				++t;
				*t = '\0';
				flag = 1;
				canonical = realpath(path, NULL);
			}
		}
	}

	if (pwd) free(path);

	return canonical;
}

int
path_writable(char **pathlist, pid_t pid, char *path, int dont_follow)
{
	char *canonical = NULL;
	int ret = 0;
	int i;

	if (!pathlist) return 0;

	canonical = canonical_path(pid, path, dont_follow);
	if (!canonical) return -1;

	for (i = 0; pathlist[i]; i++) {
		size_t size = strlen(pathlist[i]);
		//if (flag == 1 && pathlist[i][size-1] == '/') --size;
		if (strncmp(pathlist[i], canonical, size) == 0) {
			ret = 1;
			break;
		}
	}

	if (canonical) free(canonical);

	return ret;
}

void
free_pathlist(char **pathlist)
{
	int i;

	for (i = 0; pathlist[i]; i++)
		free(pathlist[i]);
	free(pathlist);
}

char **
make_pathlist(PyObject *paths)
{
	PyObject *item;
	char **pathlist;
	char *str;
	unsigned int count;
	unsigned int i;

	if (PyList_Check(paths) == 0 && PyTuple_Check(paths) == 0) {
		PyErr_SetString(PyExc_TypeError, "writable_paths should be a list or tuple object");
		return NULL;
	}

	count = PySequence_Size(paths);
	pathlist = calloc(count + 1, sizeof(char *));
	if (!pathlist) return NULL;

	for (i = 0; i < count; i++) {
		item = PySequence_GetItem(paths, i);
		if (!item) {
			free_pathlist(pathlist);
			return NULL;
		}
		str = PyString_AsString(item);
		if (!str) {
			Py_DECREF(item);
			free_pathlist(pathlist);
			return NULL;
		}
		if (str[0] != '/') {
			Py_DECREF(item);
			free_pathlist(pathlist);
			PyErr_SetString(PyExc_TypeError, "paths should be absolute");
			return NULL;
		}
		pathlist[i] = strdup(str);
		Py_DECREF(item);
		if (!pathlist[i]) {
			free_pathlist(pathlist);
			return NULL;
		}
	}

	return pathlist;
}
