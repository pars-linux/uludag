/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdlib.h>
#include <sys/time.h>
#include <dbus/dbus.h>
#include <libpolkit/libpolkit.h>
#include <Python.h>

#include "csl.h"
#include "log.h"
#include "utility.h"


static DBusMessage *
log_exception(DBusMessage *msg, DBusConnection *conn)
{
    PyObject *pType;
    PyObject *pValue;
    PyObject *pTrace;
    char *eStr;
    char *vStr = "";
    long lineno = 0;

    PyErr_Fetch(&pType, &pValue, &pTrace);
    if (!pType) {
        log_error("csl.c log_exception() called when there isn't an exception\n");
        return;
    }

    eStr = PyString_AsString(PyObject_Str(pType));

    if (pValue) {
        PyObject *tmp;
        tmp = PyObject_Str(pValue);
        if (tmp) vStr = PyString_AsString(tmp);
    }

    if (pTrace) {
        PyObject *tmp;
        tmp = PyObject_GetAttrString(pTrace, "tb_lineno");
        if (tmp) lineno = PyInt_AsLong(tmp);
    }

    log_error("Python Exception [%s] in (%s,%s,%ld): %s\n", eStr, dbus_message_get_interface(msg), dbus_message_get_path(msg), lineno, vStr);
    return dbus_message_new_error(msg, DBUS_ERROR_FAILED, vStr);
}

static void
dbus_method_call(DBusMessage* msg, DBusConnection* conn)
{
    DBusMessage* reply;
    DBusMessageIter iter;
    dbus_uint32_t serial = 0;
    PyObject *obj, *ret;

    const char *model = dbus_message_get_interface(msg);
    const char *path = dbus_message_get_path(msg);
    const char *method = dbus_message_get_member(msg);

    if (!check_model_format(model)) {
        log_error("Invalid model: %s\n", model);
        reply = dbus_message_new_error(msg, DBUS_ERROR_FAILED, "Invalid model");
    }
    else if (!check_path_format(path)) {
        log_error("Invalid application\n");
        reply = dbus_message_new_error(msg, DBUS_ERROR_FAILED, "Invalid application");
    }
    else {
        Py_Initialize();

        obj = dbus_py_import(msg);
        log_debug(LOG_JOB, "Calling %s.%s (%s)\n", model, method, path);
        ret = py_call_method(model, path, method, obj);

        if (ret == NULL) {
            reply = log_exception(msg, conn);
        }
        else {
            reply = dbus_message_new_method_return(msg);
            dbus_message_iter_init_append(reply, &iter);
            dbus_py_export(&iter, ret);
        }
        Py_Finalize();
    }

    if (!dbus_connection_send(conn, reply, &serial)) {
        log_error("DBus: Out Of Memory!\n");
        exit(1);
    }

    dbus_connection_flush(conn);

    dbus_message_unref(reply);
    dbus_message_unref(msg);
}

void
dbus_listen()
{
    struct ProcChild *p;
    int size;

    DBusMessage* msg;
    DBusConnection* conn;
    DBusError err;
    int ret;

    dbus_error_init(&err);
    conn = dbus_bus_get(DBUS_BUS_SYSTEM, &err);
    if (dbus_error_is_set(&err)) {
        log_error("DBus: Connection Error (%s)\n", err.message);
        dbus_error_free(&err);
    }
    if (NULL == conn) {
        log_error("DBus: Connection Null\n");
        exit(1);
    }

    ret = dbus_bus_request_name(conn, "tr.org.pardus.comar", DBUS_NAME_FLAG_REPLACE_EXISTING , &err);
    if (dbus_error_is_set(&err)) {
        log_error("DBus: Name Error (%s)\n", err.message);
        dbus_error_free(&err);
    }
    if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != ret) {
        log_error("DBus: Not Primary Owner (%d)\n", ret);
        exit(1);
    }

    log_info("Listening for DBus method calls\n");

    while (1) {
        dbus_connection_read_write(conn, 0);
        msg = dbus_connection_pop_message(conn);

        if (NULL == msg) {
            proc_listen(&p, &size, 0);
            continue;
        }

        if (dbus_message_has_destination(msg, "tr.org.pardus.comar")) {
            proc_dbus_call(dbus_method_call, msg, conn, "ComarDBusJob");
        }
    }
}
