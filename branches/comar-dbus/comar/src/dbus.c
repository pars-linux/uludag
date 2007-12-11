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
#include <unistd.h>
#include <Python.h>

#include "cfg.h"
#include "csl.h"
#include "iksemel.h"
#include "log.h"
#include "model.h"
#include "process.h"
#include "utility.h"
#include "xml.h"

void
dbus_send(DBusMessage *reply)
{
    dbus_uint32_t serial = 0;

    if (!dbus_connection_send(my_proc.bus_conn, reply, &serial)) {
        log_error("Out Of Memory!\n");
        exit(1);
    }

    dbus_connection_flush(my_proc.bus_conn);
    dbus_message_unref(reply);
}

void
dbus_signal(const char *path, const char *interface, const char *name, PyObject *obj)
{
    DBusMessage *msg;
    DBusMessageIter iter;
    dbus_uint32_t serial = 0;

    msg = dbus_message_new_signal(path, interface, name);
    dbus_message_iter_init_append(msg, &iter);
    dbus_py_export(&iter, obj);

    dbus_send(msg);
}

static void
dbus_reply_error(char *str)
{
    if (dbus_message_get_no_reply(my_proc.bus_msg)) return;

    DBusMessage *reply = dbus_message_new_error(my_proc.bus_msg, DBUS_ERROR_FAILED, str);
    dbus_send(reply);
}

static void
log_exception()
{
    PyObject *pType;
    PyObject *pValue;
    PyObject *pTrace;
    char *eStr;
    char *vStr = "";
    long lineno = 0;

    PyErr_Fetch(&pType, &pValue, &pTrace);
    if (!pType) {
        log_error("log_exception() called when there isn't an exception\n");
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

    log_error("Python Exception [%s] in (%s,%s,%ld): %s\n", eStr, dbus_message_get_interface(my_proc.bus_msg), dbus_message_get_path(my_proc.bus_msg), lineno, vStr);

    dbus_reply_error(vStr);
}

static void
dbus_reply_object(PyObject *obj)
{
    if (dbus_message_get_no_reply(my_proc.bus_msg)) return;

    DBusMessage *reply;
    DBusMessageIter iter;

    reply = dbus_message_new_method_return(my_proc.bus_msg);
    dbus_message_iter_init_append(reply, &iter);
    if (!dbus_py_export(&iter, obj)) {
        log_exception();
    }
    dbus_send(reply);
}

static void
dbus_reply_str(char *str)
{
    if (dbus_message_get_no_reply(my_proc.bus_msg)) return;

    DBusMessage *reply;
    DBusMessageIter iter;
    reply = dbus_message_new_method_return(my_proc.bus_msg);
    dbus_message_iter_init_append(reply, &iter);
    dbus_message_iter_append_basic(&iter, DBUS_TYPE_STRING, &str);
    dbus_send(reply);
}

static void
dbus_introspection_methods(const char *path)
{
    char *intros, *app;

    if (strcmp(path, "/") == 0) {
        xml_export_nodes("system|package", &intros);
        dbus_reply_str(intros);
        free(intros);
    }
    else if (strcmp(path, "/system") == 0) {
        xml_export_system(&intros);
        dbus_reply_str(intros);
        free(intros);
    }
    else if (strcmp(path, "/package") == 0) {
        xml_export_apps(&intros);
        dbus_reply_str(intros);
        free(intros);
    }
    else if (strncmp(path, "/package/", strlen("/package/")) == 0) {
        app = (char *) strsub(path, strlen("/package/"), 0);
        if (!db_check_app(app)) {
            log_error("No such application: '%s'\n", app);
            dbus_reply_error("No such application");
        }
        else {
            xml_export_interfaces(app, &intros);
            dbus_reply_str(intros);
            free(intros);
        }
        free(app);
    }
    else {
        log_error("Invalid object path '%s'\n", path);
        dbus_reply_error("Invalid object path");
    }
}

static void
dbus_comar_methods(const char *method)
{
    PyObject *args, *result, *list;
    char *app, *model, *script, *apps, *models, *code;
    int i;

    if (strcmp(method, "listApplications") == 0) {
        db_get_apps(&apps);
        result = py_str_split(apps, '|');
        dbus_reply_object(result);
    }
    else if (strcmp(method, "listModels") == 0) {
        result = py_str_split(model_list, '|');
        dbus_reply_object(result);
    }
    else if (strcmp(method, "listApplicationModels") == 0) {
        args = dbus_py_import(my_proc.bus_msg);
        app = PyString_AsString(PyList_GetItem(args, 0));
        db_get_models(app, &models);
        if (models == NULL) {
            log_error("No such application: '%s'\n", app);
            dbus_reply_error("No such application");
        }
        else {
            result = py_str_split(models, '|');
            dbus_reply_object(result);
        }
    }
    else if (strcmp(method, "register") == 0) {
        args = dbus_py_import(my_proc.bus_msg);
        app = PyString_AsString(PyList_GetItem(args, 0));
        model = PyString_AsString(PyList_GetItem(args, 1));
        script = PyString_AsString(PyList_GetItem(args, 2));

        if (!str_in_list(model, '|', model_list) != 0) {
            log_error("No such model: '%s'\n", model);
            dbus_reply_error("No such model.");
        }
        else {
            if (py_compile(script) != 0) {
                log_error("Not a valid Python script: '%s'\n", script);
                dbus_reply_error("Not a valid Python script.");
            }
            else {
                code = load_file(script, NULL);
                save_file(get_script_path(app, model), code, strlen(code));
                db_register_model(app, model);
                dbus_reply_object(Py_True);
            }
        }
    }
    else if (strcmp(method, "remove") == 0) {
        args = dbus_py_import(my_proc.bus_msg);
        app = PyString_AsString(PyList_GetItem(args, 0));
        db_get_models(app, &models);

        if (models == NULL) {
            log_error("No such application: '%s'\n", app);
            dbus_reply_error("No such application");
        }
        else {
            db_remove_app(app);

            list = py_str_split(models, '|');
            for (i = 0; i < PyList_Size(list); i++) {
                script = get_script_path(app, PyString_AsString(PyList_GetItem(list, i)));
                unlink(script);
            }
            dbus_reply_object(Py_True);
        }
    }
    else {
        log_error("Unknown method: '%s'\n", method);
        dbus_reply_error("Unknown method");
    }
}

void
dbus_app_methods(const char *interface, const char *path, const char *method)
{
    DBusMessage *reply;
    DBusMessageIter iter;
    PyObject *args, *result;
    int ret;

    char *app = (char *) strsub(path, strlen("/package/"), 0);
    char *model = (char *) strsub(interface, strlen(cfg_bus_name) + 1, 0);

    if (db_check_model(app, model)) {
        args = PyList_AsTuple(dbus_py_import(my_proc.bus_msg));
        ret = py_call_method(app, model, method, args, &result);

        if (ret == 1) {
            log_error("Unable to find code for '%s/%s'\n", model, app);
            dbus_reply_error("Internal error, unable to find script.");
        }
        else if (ret == 2) {
            log_exception();
        }
        else {
            dbus_reply_object(result);
        }
    }
    else {
        log_error("Invalid application or model '%s/%s'\n", model, app);
        dbus_reply_error("Invalid application or model");
    }
    free(app);
    free(model);
}

static void
dbus_method_call()
{
    char *app, *model;

    struct timeval time_start, time_end;
    unsigned long msec;

    const char *interface = dbus_message_get_interface(my_proc.bus_msg);
    const char *path = dbus_message_get_path(my_proc.bus_msg);
    const char *method = dbus_message_get_member(my_proc.bus_msg);

    gettimeofday(&time_start, NULL);

    csl_init();

    if (strcmp(interface, "org.freedesktop.DBus.Introspectable") == 0) {
        dbus_introspection_methods(path);
    }
    else if (strcmp(interface, "org.freedesktop.DBus.Peer") == 0) {
        // dbus_peer_methods(path);
    }
    else if (strncmp(interface, cfg_bus_name, strlen(cfg_bus_name)) == 0) {
        if (strcmp(path, "/system") == 0 && strcmp(interface, cfg_bus_name) == 0) {
            dbus_comar_methods(method);
        }
        else if (strncmp(path, "/package/", strlen("/package/")) == 0) {
            dbus_app_methods(interface, path, method);
        }
        else {
            log_error("Invalid object path '%s'\n", path);
            dbus_reply_error("Invalid object path");
        }
    }
    else {
        dbus_reply_error("Invalid interface");
    }

    gettimeofday(&time_end, NULL);
    msec = time_diff(&time_start, &time_end);
    if (msec / 1000 > 60) {
        log_info("Execution of %s.%s (%s) took %.3f seconds\n", interface, method, path, (float) msec / 1000);
    }
    else {
        log_debug(LOG_PERF, "Execution of %s.%s (%s) took %.3f seconds\n", interface, method, path, (float) msec / 1000);
    }

    csl_end();
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

    ret = dbus_bus_request_name(conn, cfg_bus_name, DBUS_NAME_FLAG_REPLACE_EXISTING, &err);
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

        const char *sender = dbus_message_get_sender(msg);
        const char *interface = dbus_message_get_interface(msg);
        const char *path = dbus_message_get_path(msg);
        const char *method = dbus_message_get_member(msg);

        switch (dbus_message_get_type(msg)) {
            case DBUS_MESSAGE_TYPE_METHOD_CALL:
                log_debug(LOG_DBUS, "DBus method call [%s.%s] from [%s]\n", interface, method, sender);
                proc_fork(dbus_method_call, "ComarDBusJob", conn, msg);
                break;
            case DBUS_MESSAGE_TYPE_SIGNAL:
                log_debug(LOG_DBUS, "DBus signal [%s.%s] from [%s]\n", interface, method, sender);
                break;
        }
    }
}
