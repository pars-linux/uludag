#include <dbus/dbus.h>
#include <Python.h>

PyObject *dbus_py_get_list(DBusMessageIter *iter);
PyObject *dbus_py_get_dict(DBusMessageIter *iter);
PyObject *dbus_py_get_item(DBusMessageIter* iter);
char *dbus_py_get_object_signature(PyObject *obj);
