/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <dbus/dbus.h>
#include <Python.h>

void csl_init();
void csl_end();

int py_compile(const char *script_path);
int py_call_method(const char *app, const char *model, const char *method, PyObject *args, PyObject **result);
PyObject *dbus_py_import(DBusMessage *msg);
int dbus_py_export(DBusMessageIter *iter, PyObject *obj);
PyObject *py_str_split(char *str, char delimiter);

PyObject *dbus_py_get_list(DBusMessageIter *iter);
PyObject *dbus_py_get_dict(DBusMessageIter *iter);
PyObject *dbus_py_get_item(DBusMessageIter* iter);
char *dbus_py_get_object_signature(PyObject *obj);
