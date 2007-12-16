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


DBusConnection *conn_sys = NULL;
PyObject *signalHooks_sys = NULL;
PyObject *methodHooks_sys = NULL;
DBusMessage *msg_sys = NULL;

DBusConnection *conn_ses = NULL;
PyObject *signalHooks_ses = NULL;
PyObject *methodHooks_ses = NULL;
DBusMessage *msg_ses = NULL;

PyObject *
light_init(PyObject *self, PyObject *args)
{
    DBusError err;

    methodHooks_sys = PyDict_New();
    signalHooks_sys = PyList_New(0);

    methodHooks_ses = PyDict_New();
    signalHooks_ses = PyList_New(0);

    dbus_error_init(&err);
    conn_sys = dbus_bus_get(DBUS_BUS_SYSTEM, &err);
    if (dbus_error_is_set(&err)) {
        PyErr_SetString(PyExc_Exception, err.message);
        dbus_error_free(&err);
        return NULL;
    }

    conn_ses = dbus_bus_get(DBUS_BUS_SESSION, &err);
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
    int bustype;
    DBusError err;

    if (!PyArg_ParseTuple(args, "sOi", &rule, &callback, &bustype)) {
        return NULL;
    }

    if (!conn_sys) {
        PyErr_SetString(PyExc_Exception, "run init() first.");
        return NULL;
    }

    if (bustype == 0) {
        PyList_Append(signalHooks_sys, callback);
    }
    else {
        PyList_Append(signalHooks_ses, callback);
    }

    dbus_error_init(&err);
    if (bustype == 0) {
        dbus_bus_add_match(conn_sys, rule, &err);
    }
    else {
        dbus_bus_add_match(conn_ses, rule, &err);
    }
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
    int bustype, i;
    DBusMessage *msg;
    dbus_uint32_t serial = 0;
    dbus_bool_t sent;

    if (!PyArg_ParseTuple(args, "ssssOOi", &dest, &path, &interface, &method, &obj, &callback, &bustype)) {
        return NULL;
    }

    if (!conn_sys) {
        PyErr_SetString(PyExc_Exception, "run init() first.");
        return NULL;
    }

    msg = dbus_message_new_method_call(dest, path, interface, method);
    if (PyTuple_Check(obj)) {
        if (PyTuple_Size(obj) > 0) {
            DBusMessageIter iter;
            dbus_message_iter_init_append(msg, &iter);
            for (i = 0; i < PyTuple_Size(obj); i++) {
                if (dbus_py_export(&iter, PyTuple_GetItem(obj, i)) != 0) {
                    return NULL;
                }
            }
        }
    }
    else {
        PyErr_SetString(PyExc_Exception, "Arguments must be passed as a tuple.");
        return NULL;
    }

    if (bustype == 0) {
        sent = dbus_connection_send(conn_sys, msg, &serial);
    }
    else {
        sent = dbus_connection_send(conn_ses, msg, &serial);
    }
    if (!sent) {
        PyErr_SetString(PyExc_Exception, "out of memory");
        return NULL;
    }


    if (bustype == 0) {
       PyDict_SetItem(methodHooks_sys, PyLong_FromLong((long) serial), callback);
       dbus_connection_flush(conn_sys);
    }
    else {
       PyDict_SetItem(methodHooks_ses, PyLong_FromLong((long) serial), callback);
       dbus_connection_flush(conn_ses);
    }
    dbus_message_unref(msg);

    return PyLong_FromLong((long) serial);
}

PyObject *
light_fetch(PyObject *self, PyObject *args)
{
    int i;
    PyObject *obj;

    if (!conn_sys) {
        PyErr_SetString(PyExc_Exception, "run init() first.");
        return NULL;
    }

    dbus_connection_read_write(conn_sys, 0);
    msg_sys = dbus_connection_pop_message(conn_sys);

    dbus_connection_read_write(conn_ses, 0);
    msg_ses = dbus_connection_pop_message(conn_ses);

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject *
light_exec(PyObject *self, PyObject *args)
{
    PyObject *obj;
    dbus_uint32_t serial;
    int i;

    if (!conn_sys) {
        PyErr_SetString(PyExc_Exception, "run init() first.");
        return NULL;
    }

    if (msg_sys) {
        serial = dbus_message_get_reply_serial(msg_sys);

        switch (dbus_message_get_type(msg_sys)) {
            case DBUS_MESSAGE_TYPE_METHOD_RETURN:
                obj = PyList_AsTuple(dbus_py_import(msg_sys));
                if (PyDict_GetItem(methodHooks_sys, PyLong_FromLong((long) serial))) {
                    PyObject_CallObject(PyDict_GetItem(methodHooks_sys, PyLong_FromLong((long) serial)), obj);
                    PyDict_DelItem(methodHooks_sys, PyLong_FromLong((long) serial));
                }
                Py_DECREF(obj);
                break;
            case DBUS_MESSAGE_TYPE_SIGNAL:
                obj = PyList_AsTuple(dbus_py_import(msg_sys));
                for (i = 0; i < PyList_Size(signalHooks_sys); i++) {
                    PyObject_CallObject(PyList_GetItem(signalHooks_sys, i), obj);
                }
                Py_DECREF(obj);
                break;
        }

        dbus_message_unref(msg_sys);
    }

    if (msg_ses) {
        serial = dbus_message_get_reply_serial(msg_ses);

        switch (dbus_message_get_type(msg_ses)) {
            case DBUS_MESSAGE_TYPE_METHOD_RETURN:
                obj = PyList_AsTuple(dbus_py_import(msg_ses));
                if (PyDict_GetItem(methodHooks_ses, PyLong_FromLong((long) serial))) {
                    PyObject_CallObject(PyDict_GetItem(methodHooks_ses, PyLong_FromLong((long) serial)), obj);
                    PyDict_DelItem(methodHooks_ses, PyLong_FromLong((long) serial));
                }
                Py_DECREF(obj);
                break;
            case DBUS_MESSAGE_TYPE_SIGNAL:
                obj = PyList_AsTuple(dbus_py_import(msg_ses));
                for (i = 0; i < PyList_Size(signalHooks_ses); i++) {
                    PyObject_CallObject(PyList_GetItem(signalHooks_ses, i), obj);
                }
                Py_DECREF(obj);
                break;
        }

        dbus_message_unref(msg_ses);
    }

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef light_methods[] = {
    {"init",  (PyCFunction)light_init, METH_NOARGS, "init()\n  Initializes d_light."},
    {"fetch",  (PyCFunction)light_fetch, METH_NOARGS, "fetch()\n  Fetches a message from DBus message queue."},
    {"exec_",  (PyCFunction)light_exec, METH_NOARGS, "exec_()\n  Processes fetched message."},
    {"registerSignal",  (PyCFunction)light_registerSignal, METH_VARARGS, "registerSignal(rule, callbackFunc, bustype)\n  Registers a new signal callback function.\n bustype can be BUS_SESSION or BUS_SYSTEM"},
    {"call",  (PyCFunction)light_call, METH_VARARGS, "call(dest, path, iface, method, args_tuple, callbackFunc, bustype)\n  Makes an asynchronous method call\n bustype can be BUS_SESSION or BUS_SYSTEM"},
    {NULL, NULL}
};


PyMODINIT_FUNC
initd_light(void)
{
    PyObject *m;

    m = Py_InitModule("d_light", light_methods);
    PyModule_AddObject(m, "BUS_SYSTEM", PyInt_FromLong((long) 0));
    PyModule_AddObject(m, "BUS_SESSION", PyInt_FromLong((long) 1));

    return;
}
