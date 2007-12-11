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

int py_call_method(const char *app, const char *model, const char *method, PyObject *args, PyObject **result);
PyObject *dbus_py_import(DBusMessage *msg);
int dbus_py_export(DBusMessageIter *iter, PyObject *obj);
