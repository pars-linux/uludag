/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <Python.h>
#include <stdlib.h>
#include <sys/time.h>
#include <dbus/dbus.h>
#include <unistd.h>

#include "cfg.h"
#include "csl.h"
#include "data.h"
#include "iksemel.h"
#include "log.h"
#include "model.h"
#include "process.h"
#include "pydbus.h"
#include "utility.h"

#ifdef HAVE_POLICYKIT
#include "policy.h"
#endif

//! Sends message to client
void
dbus_send(DBusMessage *reply)
{
    /*
     * Sends DBus message to client.
     *
     * @reply DBus message to be sent
     */

    dbus_uint32_t serial = 0;

    if (!dbus_connection_send(my_proc.bus_conn, reply, &serial)) {
        log_error("Out Of Memory!\n");
        proc_finish();
    }

    dbus_connection_flush(my_proc.bus_conn);
    dbus_message_unref(reply);
}

//! Emits a signal
void
dbus_signal(const char *path, const char *interface, const char *name, PyObject *obj)
{
    /*
     * Emits a DBus signal.
     * 
     * @path Object path
     * @interface Interface
     * @name Signal name
     * @obj Arguments (Python object)
     */

    DBusMessage *msg;
    DBusMessageIter iter;
    dbus_uint32_t serial = 0;

    msg = dbus_message_new_signal(path, interface, name);
    dbus_message_iter_init_append(msg, &iter);
    dbus_py_export(&iter, obj);

    dbus_send(msg);
}

//! Creates an error message and sends
static void
dbus_reply_error(char *class, char *name, char *str)
{
    /*
     * Creates an error message and sends to client. Does nothing if client
     * ignores reply.
     *
     * @str Message
     */

    if (dbus_message_get_no_reply(my_proc.bus_msg)) return;

    char *err_name;
    int size;

    size = strlen(cfg_bus_name) + 1 + strlen(class) + 1 + strlen(name) + 1;
    err_name = malloc(size);
    snprintf(err_name, size, "%s.%s.%s\0", cfg_bus_name, class, name);

    DBusMessage *reply = dbus_message_new_error(my_proc.bus_msg, err_name, str);
    dbus_send(reply);
    free(err_name);
}

//! Logs a Python exception
static void
log_exception()
{
    /*
     * Logs a Python exception and sends reply to the client.
     */

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

    dbus_reply_error("python", eStr, vStr);
}

//! Creates a message from Python object and sends
static void
dbus_reply_object(PyObject *obj)
{
    /*
     * Creates a DBus message from Python object and sends to client. 
     * Does nothing if client ignores reply.
     *
     * @obj Python object
     */

    if (dbus_message_get_no_reply(my_proc.bus_msg)) return;

    DBusMessage *reply;
    DBusMessageIter iter;

    reply = dbus_message_new_method_return(my_proc.bus_msg);
    dbus_message_iter_init_append(reply, &iter);
    if (dbus_py_export(&iter, obj) != 0) {
        log_exception();
    }
    dbus_send(reply);
}

//! Creates a message and sends
static void
dbus_reply_str(char *str)
{
    /*
     * Creates a DBus message from string and sends to client.
     * Does nothing if client ignores reply.
     *
     * @str Message
     */

    if (dbus_message_get_no_reply(my_proc.bus_msg)) return;

    DBusMessage *reply;
    DBusMessageIter iter;
    reply = dbus_message_new_method_return(my_proc.bus_msg);
    dbus_message_iter_init_append(reply, &iter);
    dbus_message_iter_append_basic(&iter, DBUS_TYPE_STRING, &str);
    dbus_send(reply);
}

//! Creates introspection for given object path
static void
dbus_introspection_methods(const char *path)
{
    /*
     * Creates introspection XML for given object path and sends to client.
     *
     * @path Object path
     */

    if (strcmp(path, "/") == 0) {
        iks *xml = iks_new("node");

        // package node contains applications and models
        iks_insert_attrib(iks_insert(xml, "node"), "name", "package");

        // add standard interfaces
        model_get_iks("org.freedesktop.DBus.Introspectable", &xml);

        // add core interface
        model_get_iks("Comar", &xml);

        dbus_reply_str(iks_string(NULL, xml));
        iks_delete(xml);
    }
    else if (strcmp(path, "/package") == 0) {
        char *apps;
        db_get_apps(&apps);
        if (apps == NULL) {
            iks *xml = iks_new("node");

            // add standard interfaces
            model_get_iks("org.freedesktop.DBus.Introspectable", &xml);

            dbus_reply_str(iks_string(NULL, xml));
            iks_delete(xml);
        }
        else {
            iks *xml = iks_new("node");
            char *pch = strtok(apps, "|");
            while (pch != NULL) {
                if (strlen(pch) > 0) {
                    iks_insert_attrib(iks_insert(xml, "node"), "name", pch);
                }
                pch = strtok(NULL, "|");
            }

            // add standard interfaces
            model_get_iks("org.freedesktop.DBus.Introspectable", &xml);

            dbus_reply_str(iks_string(NULL, xml));
            iks_delete(xml);
            free(apps);
        }
    }
    else if (strncmp(path, "/package/", strlen("/package/")) == 0) {
        char *app = (char *) strsub(path, strlen("/package/"), 0);
        if (!db_check_app(app)) {
            log_error("No such application: '%s'\n", app);
            dbus_reply_error("db", "noapp", "No such application.");
        }
        else {
            char *models;
            db_get_app_models(app, &models);
            if (models == NULL) {
                iks *xml = iks_new("node");

                // add standard interfaces
                model_get_iks("org.freedesktop.DBus.Introspectable", &xml);

                dbus_reply_str(iks_string(NULL, xml));
                iks_delete(xml);
            }
            else {
                iks *xml = iks_new("node");
                char *pch = strtok(models, "|");
                while (pch != NULL) {
                    if (strlen(pch) > 0) {
                        model_get_iks(pch, &xml);
                    }
                    pch = strtok(NULL, "|");
                }

                // add standard interfaces
                model_get_iks("org.freedesktop.DBus.Introspectable", &xml);

                dbus_reply_str(iks_string(NULL, xml));
                iks_delete(xml);
                free(models);
            }
        }
        free(app);
    }
    else {
        log_error("Unknown object path '%s'\n", path);
        dbus_reply_error("dbus", "unknownpath", "Object path unknown.");
    }
}

//! Replies messages made to COMAR core interface
static void
dbus_comar_methods(const char *method)
{
    /*
     * Replies messages made to COMAR core interface.
     * Methods in COMAR core are:
     *     listApplications()
     *     listModels()
     *     listApplicationModels(app)
     *     register(app, model, script)
     *     remove(app)
     *
     * @method Method
     */

    PyObject *args, *result;
    char *app, *model, *script, *apps, *models, *code;
    int i;

    if (strcmp(method, "listApplications") == 0) {
        db_get_apps(&apps);
        result = PyList_New(0);
        if (apps != NULL) {
            char *pch = strtok(apps, "|");
            while (pch != NULL) {
                if (strlen(pch) > 0) {
                    PyList_Append(result, PyString_FromString(pch));
                }
                pch = strtok(NULL, "|");
            }
            free(apps);
        }
        dbus_reply_object(result);
    }
    else if (strcmp(method, "listModels") == 0) {
        result = PyList_New(0);
        iks *obj;
        for (obj = iks_first_tag(model_xml); obj; obj = iks_next_tag(obj)) {
            if (iks_strcmp(iks_find_attrib(obj, "name"), "Comar") == 0 || iks_strncmp(iks_find_attrib(obj, "name"), "org.freedesktop.", strlen("org.freedesktop.")) == 0) {
                continue;
            }
            PyList_Append(result, PyString_FromString(iks_find_attrib(obj, "name")));
        }
        dbus_reply_object(result);
    }
    else if (strcmp(method, "listModelApplications") == 0) {
        args = dbus_py_import(my_proc.bus_msg);
        model = PyString_AsString(PyList_GetItem(args, 0));
        db_get_model_apps(model, &apps);
        if (apps != NULL) {
            result = PyList_New(0);
            char *pch = strtok(apps, "|");
            while (pch != NULL) {
                if (strlen(pch) > 0) {
                    PyList_Append(result, PyString_FromString(pch));
                }
                pch = strtok(NULL, "|");
            }
            dbus_reply_object(result);
            free(apps);
        }
        else {
            log_error("Unknown model: '%s'\n", model);
            dbus_reply_error("db", "nomodel", "Model unknown.");
        }
    }
    else if (strcmp(method, "listApplicationModels") == 0) {
        args = dbus_py_import(my_proc.bus_msg);
        app = PyString_AsString(PyList_GetItem(args, 0));
        db_get_app_models(app, &models);
        if (models != NULL) {
            result = PyList_New(0);
            char *pch = strtok(models, "|");
            while (pch != NULL) {
                if (strlen(pch) > 0) {
                    PyList_Append(result, PyString_FromString(pch));
                }
                pch = strtok(NULL, "|");
            }
            dbus_reply_object(result);
            free(models);
        }
        else {
            log_error("Unknown application: '%s'\n", app);
            dbus_reply_error("db", "noapp", "Application unknown.");
        }
    }
    else if (strcmp(method, "register") == 0) {
        args = dbus_py_import(my_proc.bus_msg);
        app = PyString_AsString(PyList_GetItem(args, 0));
        model = PyString_AsString(PyList_GetItem(args, 1));
        script = PyString_AsString(PyList_GetItem(args, 2));

        if (model_lookup_interface(model) == -1) {
            log_error("No such model: '%s'\n", model);
            dbus_reply_error("db", "nomodel", "No such model.");
        }
        else {
            if (py_compile(script) != 0) {
                log_error("Not a valid Python script: '%s'\n", script);
                dbus_reply_error("python", "SyntaxError", "Not a valid Python script.");
            }
            else {
                code = load_file(script, NULL);
                script = get_script_path(app, model);
                save_file(script, code, strlen(code));
                free(script);
                db_register_model(app, model);
                dbus_reply_object(Py_True);
            }
        }
    }
    else if (strcmp(method, "remove") == 0) {
        args = dbus_py_import(my_proc.bus_msg);
        app = PyString_AsString(PyList_GetItem(args, 0));
        db_get_app_models(app, &models);

        if (models == NULL) {
            log_error("Unknown application: '%s'\n", app);
            dbus_reply_error("db", "noapp", "Unknown application");
        }
        else {
            db_remove_app(app);

            char *pch = strtok(models, "|");
            while (pch != NULL) {
                if (strlen(pch) > 0) {
                    script = get_script_path(app, pch);
                    unlink(script);
                    //free(script);
                }
                pch = strtok(NULL, "|");
            }

            dbus_reply_object(Py_True);
        }
    }
    else {
        log_error("Unknown method: '%s'\n", method);
        dbus_reply_error("dbus", "unknownmethod", "Unknown method");
    }
}

//! Replies messages made to registered application models
void
dbus_app_methods(const char *interface, const char *path, const char *method)
{
    /*
     * Replies messages made to registered application models.
     * Extracts method arguments from DBus Message (reachable via my_proc.bus_msg)
     *
     * @interface Interface
     * @path Object path
     * @method Method
     */

    DBusMessage *reply;
    DBusMessageIter iter;
    PyObject *args, *result;
    int ret;

    char *app = (char *) strsub(path, strlen("/package/"), 0);
    char *model = (char *) strsub(interface, strlen(cfg_bus_name) + 1, 0);

    if (!db_check_model(app, model)) {
        log_error("Application interface doesn't exist: %s (%s)\n", model, app);
        dbus_reply_error("dbus", "unknownmodel", "Application interface doesn't exist.");
    }
    else if (model_lookup_method(model, method) == -1) {
        log_error("Unknown method: %s.%s\n", model, method);
        dbus_reply_error("dbus", "unknownmethod", "Unknown method.");
    }
    else {
        args = PyList_AsTuple(dbus_py_import(my_proc.bus_msg));
        ret = py_call_method(app, model, method, args, &result);

        if (ret == 1) {
            log_error("Unable to find: %s (%s)\n", model, app);
            dbus_reply_error("core", "internal", "Unable to find script.");
        }
        else if (ret == 2) {
            log_exception();
        }
        else {
            dbus_reply_object(result);
        }
    }
    free(app);
    free(model);
}

#ifdef HAVE_POLICYKIT
//! Checks if sender is allowed to call specified method
static int
dbus_policy_check(const char *sender, const char *interface, const char *method)
{
    /*!
     *
     * @sener Bus name of the sender
     * @interface Interface
     * @method Method
     * @return 1 if access granted, 0 if access denied
     */

    PolKitResult polkit_result;

    if (policy_check(sender, interface, method, &polkit_result)) {
        log_debug(LOG_PLCY, "PolicyKit: %s [%s.%s] = %s\n", sender, interface, method, polkit_result_to_string_representation(polkit_result));
        switch (polkit_result) {
            case POLKIT_RESULT_YES:
                return 1;
            case POLKIT_RESULT_NO:
                dbus_reply_error("policy", "no", "Access denied.");
                return 0;
            case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH:
            case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_SESSION:
            case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_KEEP_ALWAYS:
            case POLKIT_RESULT_ONLY_VIA_ADMIN_AUTH_ONE_SHOT:
                dbus_reply_error("policy", "auth_admin", "Access denied, but can be granted via admin auth.");
                return 0;
            case POLKIT_RESULT_ONLY_VIA_SELF_AUTH:
            case POLKIT_RESULT_ONLY_VIA_SELF_AUTH_KEEP_SESSION:
            case POLKIT_RESULT_ONLY_VIA_SELF_AUTH_KEEP_ALWAYS:
            case POLKIT_RESULT_ONLY_VIA_SELF_AUTH_ONE_SHOT:
                dbus_reply_error("policy", "auth_self", "Access denied, but can be granted via self auth.");
                return 0;
        }
    }
    else {
        dbus_reply_error("core", "internal", "Unable to query PolicyKit");
        return 0;
    }
}
#endif

//! Forked function that handles method calls
static void
dbus_method_call()
{
    /*
     * This function handles method calls.
     *
     * DBus connection is reacable via my_proc.bus_conn
     * DBus message is reacable via my_proc.bus_msg
     *
     */

    char *app, *model;

    struct timeval time_start, time_end;
    unsigned long msec;

    const char *interface = dbus_message_get_interface(my_proc.bus_msg);
    const char *path = dbus_message_get_path(my_proc.bus_msg);
    const char *method = dbus_message_get_member(my_proc.bus_msg);
    const char *sender = dbus_message_get_sender(my_proc.bus_msg);

    gettimeofday(&time_start, NULL);

    csl_init();

    if (strcmp(interface, "org.freedesktop.DBus.Introspectable") == 0) {
        dbus_introspection_methods(path);
    }
    else if (strcmp(interface, "org.freedesktop.DBus.Peer") == 0) {
        // dbus_peer_methods(path);
    }
    else if (strncmp(interface, cfg_bus_name, strlen(cfg_bus_name)) == 0) {
        #ifdef HAVE_POLICYKIT
        if (dbus_policy_check(sender, interface, method)) {
        #endif
            if (strcmp(path, "/") == 0 && strcmp(interface, cfg_bus_name) == 0) {
                dbus_comar_methods(method);
            }
            else if (strncmp(path, "/package/", strlen("/package/")) == 0) {
                dbus_app_methods(interface, path, method);
            }
            else {
                log_error("Unknown object path '%s'\n", path);
                dbus_reply_error("dbus", "unknownpath", "Unknown object path");
            }
        #ifdef HAVE_POLICYKIT
        }
        #endif
    }
    else {
        dbus_reply_error("dbus", "unknownmodel", "Unknown interface");
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

//! Starts a server and listens for calls/signals
void
dbus_listen()
{
    /*
     * Starts a DBus server and listens for calls and signals.
     * Forks "dbus_method_call" when a method call is fetched.
     */

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
        proc_finish();
    }

    ret = dbus_bus_request_name(conn, cfg_bus_name, DBUS_NAME_FLAG_REPLACE_EXISTING, &err);
    if (dbus_error_is_set(&err)) {
        log_error("Name Error (%s)\n", err.message);
        dbus_error_free(&err);
        proc_finish();
    }

    unique_name = dbus_bus_get_unique_name(conn);
    log_info("Listening on %s (%s)...\n", cfg_bus_name, unique_name);

    while (1) {
        dbus_connection_read_write(conn, 0);
        msg = dbus_connection_pop_message(conn);

        if (proc_check_idle() == 1) {
            log_info("Service was idle for %d second(s), closing daemon...\n", cfg_idle_shutdown);
            return;
        }

        if (shutdown_activated) {
            log_info("Shutdown requested.\n");
            return;
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
