/*
* Copyright (c) 2005, TUBITAK/UEKAE
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License as published by the
* Free Software Foundation; either version 2 of the License, or (at your
* option) any later version. Please read the COPYING file.
*/

#include <Python.h>
#include <dbus/dbus.h>
#include <time.h>

#include "trans.h"


DBusConnection *conn = NULL;
DBusMessage *msg = NULL;
PyObject *signalHooks = NULL;
PyObject *methodHooks = NULL;

PyObject *
light_init(PyObject *self, PyObject *args)
{
    DBusError err;

    signalHooks = PyList_New(0);
    methodHooks = PyDict_New();

    dbus_error_init(&err);
    conn = dbus_bus_get(DBUS_BUS_SYSTEM, &err);
    msg = NULL;

    if (dbus_error_is_set(&err)) {
        PyErr_SetString(PyExc_Exception, err.message);
        dbus_error_free(&err);
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *
light_registerSignal(PyObject *self, PyObject *args)
{
    char *rule;
    PyObject *callback;
    DBusError err;

    if (!PyArg_ParseTuple(args, "sO", &rule, &callback)) {
        return NULL;
    }

    if (!conn) {
        PyErr_SetString(PyExc_Exception, "run init() first.");
        return NULL;
    }

    PyList_Append(signalHooks, callback);

    dbus_error_init(&err);
    dbus_bus_add_match(conn, rule, &err);
    if (dbus_error_is_set(&err)) {
        PyErr_SetString(PyExc_Exception, err.message);
        dbus_error_free(&err);
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *
light_call(PyObject *self, PyObject *args)
{
    char *dest, *path, *interface, *method;
    PyObject *obj, *callback;
    DBusMessage *msg;
    dbus_uint32_t serial = 0;

    if (!PyArg_ParseTuple(args, "ssssOO", &dest, &path, &interface, &method, &obj, &callback)) {
        return NULL;
    }

    if (!conn) {
        PyErr_SetString(PyExc_Exception, "run init() first.");
        return NULL;
    }

    msg = dbus_message_new_method_call(dest, path, interface, method);
    if (PyTuple_Check(obj)) {
        if (PyTuple_Size(obj) > 0) {
            DBusMessageIter iter;
            dbus_message_iter_init_append(msg, &iter);
            if (dbus_py_export(&iter, obj) != 0) {
                return NULL;
            }
        }
    }
    else {
        PyErr_SetString(PyExc_Exception, "Arguments must be passed as a tuple.");
        return NULL;
    }

    if (!dbus_connection_send(conn, msg, &serial)) {
        PyErr_SetString(PyExc_Exception, "out of memory");
        return NULL;
    }

    PyDict_SetItem(methodHooks, PyLong_FromLong((long) serial), callback);

    dbus_connection_flush(conn);
    dbus_message_unref(msg);

    return PyLong_FromLong((long) serial);
}

PyObject *
light_fetch(PyObject *self, PyObject *args)
{
    int i;
    PyObject *obj;

    if (!conn) {
        PyErr_SetString(PyExc_Exception, "run init() first.");
        return NULL;
    }

    dbus_connection_read_write(conn, 0);
    msg = dbus_connection_pop_message(conn);

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *
light_exec(PyObject *self, PyObject *args)
{
    PyObject *obj;

    if (!conn) {
        PyErr_SetString(PyExc_Exception, "run init() first.");
        return NULL;
    }

    if (!msg) goto out;

    dbus_uint32_t serial = dbus_message_get_reply_serial(msg);

    switch (dbus_message_get_type(msg)) {
        case DBUS_MESSAGE_TYPE_METHOD_RETURN:
            obj = PyList_AsTuple(dbus_py_import(msg));
            if (PyDict_GetItem(methodHooks, PyLong_FromLong((long) serial))) {
                PyObject_CallObject(PyDict_GetItem(methodHooks, PyLong_FromLong((long) serial)), obj);
                PyDict_DelItem(methodHooks, PyLong_FromLong((long) serial));
            }
            Py_DECREF(obj);
            break;
        case DBUS_MESSAGE_TYPE_SIGNAL:
            obj = PyList_AsTuple(dbus_py_import(msg));
            int i;
            for (i = 0; i < PyList_Size(signalHooks); i++) {
                PyObject_CallObject(PyList_GetItem(signalHooks, i), obj);
            }
            Py_DECREF(obj);
            break;
    }

    dbus_message_unref(msg);

out:
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef light_methods[] = {
    {"init",  (PyCFunction)light_init, METH_NOARGS, "init()\n  Initializes d_light."},
    {"fetch",  (PyCFunction)light_fetch, METH_NOARGS, "fetch()\n  Fetches a message from DBus message queue."},
    {"exec_",  (PyCFunction)light_exec, METH_NOARGS, "exec_()\n  Processes fetched message."},
    {"registerSignal",  (PyCFunction)light_registerSignal, METH_VARARGS, "registerSignal(rule, callbackFunc)\n  Registers a new signal callback function."},
    {"call",  (PyCFunction)light_call, METH_VARARGS, "call(dest, path, iface, method, args_tuple, callbackFunc)\n  Makes an asynchronous method call"},
    {NULL, NULL}
};

PyMODINIT_FUNC
initd_light(void)
{
    PyObject *m;

    m = Py_InitModule("d_light", light_methods);

    return;
}

