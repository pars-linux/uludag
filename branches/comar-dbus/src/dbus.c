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
#include <Python.h>

#include "cfg.h"
#include "csl.h"
#include "log.h"
#include "process.h"
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
dbus_method_call()
{
    DBusMessage *reply;
    DBusMessageIter iter;
    dbus_uint32_t serial = 0;
    PyObject *obj, *ret;

    const char *interface = dbus_message_get_interface(my_proc.bus_msg);
    const char *path = dbus_message_get_path(my_proc.bus_msg);
    const char *method = dbus_message_get_member(my_proc.bus_msg);

    if (!check_interface_format(interface)) {
        log_error("Invalid interface: %s\n", interface);
        reply = dbus_message_new_error(my_proc.bus_msg, DBUS_ERROR_FAILED, "Invalid interface");
    }
    else if (!check_path_format(path)) {
        log_error("Invalid application\n");
        reply = dbus_message_new_error(my_proc.bus_msg, DBUS_ERROR_FAILED, "Invalid application");
    }
    else {
        reply = dbus_message_new_error(my_proc.bus_msg, DBUS_ERROR_FAILED, "done");
        Py_Initialize();

        obj = dbus_py_import(my_proc.bus_msg);
        log_debug(LOG_JOB, "Calling %s.%s (%s)\n", interface, method, path);
        ret = py_call_method(interface, path, method, obj);

        if (ret == NULL) {
            reply = log_exception(my_proc.bus_msg, my_proc.bus_conn);
        }
        else {
            reply = dbus_message_new_method_return(my_proc.bus_msg);
            dbus_message_iter_init_append(reply, &iter);
            dbus_py_export(&iter, ret);
        }
        Py_Finalize();
    }

    if (!dbus_connection_send(my_proc.bus_conn, reply, &serial)) {
        log_error("Out Of Memory!\n");
        exit(1);
    }

    dbus_connection_flush(my_proc.bus_conn);

    dbus_message_unref(reply);
}

void
dbus_listen()
{
    struct ProcChild *p;
    int size;

    DBusConnection *conn;
    DBusMessage *msg;
    DBusError err;
    int ret;
    const char *unique_name;

    dbus_error_init(&err);
    conn = dbus_bus_get(cfg_bus_type, &err);
    if (dbus_error_is_set(&err)) {
        log_error("Connection Error (%s)\n", err.message);
        dbus_error_free(&err);
    }
    if (NULL == conn) {
        log_error("Connection Null\n");
        exit(1);
    }

    ret = dbus_bus_request_name(conn, cfg_bus_name, DBUS_NAME_FLAG_REPLACE_EXISTING , &err);
    if (dbus_error_is_set(&err)) {
        log_error("Name Error (%s)\n", err.message);
        dbus_error_free(&err);
    }
    if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != ret) {
        log_error("Not Primary Owner (%d)\n", ret);
        exit(1);
    }

    unique_name = dbus_bus_get_unique_name(conn);
    log_info("Listening on %s (%s)...\n", cfg_bus_name, unique_name);

    while (1) {
        dbus_connection_read_write(conn, 0);
        msg = dbus_connection_pop_message(conn);

        if (proc_check_idle() == 1) {
            log_info("Service was idle for %d second(s), closing daemon...\n", cfg_idle_shutdown);
            break;
        }

        if (NULL == msg) {
            proc_listen(&p, &size, 0, 500);
            continue;
        }

        log_debug(LOG_ALL, "Destination: %s\n", dbus_message_get_destination(msg));
        log_debug(LOG_ALL, "Interface: %s\n", dbus_message_get_interface(msg));
        log_debug(LOG_ALL, "Method: %s\n", dbus_message_get_member(msg));

        if (dbus_message_has_interface(msg, "org.freedesktop.DBus")) {
            // Do nothing
        }
        else if (dbus_message_has_interface(msg, "org.freedesktop.DBus.Introspectable")) {
            if (dbus_message_has_member(msg, "Introspect")) {
                // Give introspection
            }
        }
        else {
            proc_fork(dbus_method_call, "ComarDBusJob", conn, msg);
        }
    }
}
