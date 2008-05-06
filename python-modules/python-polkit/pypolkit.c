/*
* Copyright (c) 2008, TUBITAK/UEKAE
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License as published by the
* Free Software Foundation; either version 2 of the License, or (at your
* option) any later version. Please read the COPYING file.
*/

#include <Python.h>
#include <polkit-grant/polkit-grant.h>
#include <datetime.h>
#include <time.h>
#include <unistd.h>
#include <grp.h>

//! Standard exception for pypolkit
static PyObject *PK_Error;

//! Sets key of dictionary if value is not null
void
dict_set_unless_null(PyObject *dict, const char *key, const char *value)
{
    if (value != NULL) {
        PyDict_SetItemString(dict, key, PyString_FromString(value));
    }
}

//! Creates action object from action id
PolKitAction *
pk_make_action(const char *action_id)
{
    PolKitAction *pk_action = polkit_action_new();
    polkit_action_set_action_id(pk_action, action_id);
    return pk_action;
}

//! Creates caller object from uid
PolKitCaller *
pk_make_caller_from_uid(int uid)
{
    PolKitCaller *pk_caller = polkit_caller_new();
    polkit_caller_set_uid(pk_caller, (uid_t) uid);
    return pk_caller;
}

//! Creates caller object from pid
PolKitCaller *
pk_make_caller_from_pid(int pid)
{
    PolKitCaller *pk_caller = polkit_caller_new();
    polkit_caller_set_pid(pk_caller, (pid_t) pid);
    return pk_caller;
}

//! Init policy cache
PolKitPolicyCache *
pk_init_cache()
{
    PolKitError *pk_error = NULL;
    PolKitContext *pk_context = polkit_context_new();

    // Init context
    if (!polkit_context_init(pk_context, &pk_error)) {
        polkit_context_unref(pk_context);
        PyErr_SetString(PK_Error, polkit_error_get_error_name(pk_error));
        return NULL;
    }

    // Load descriptions
    polkit_context_set_load_descriptions(pk_context);

    // Get policy cache
    PolKitPolicyCache *pk_cache = polkit_context_get_policy_cache(pk_context);
    if (pk_cache == NULL) {
        polkit_context_unref(pk_context);
        PyErr_SetString(PK_Error, polkit_error_get_error_name(pk_error));
        return NULL;
    }

    return pk_cache;
}

//! Init auth db
PolKitAuthorizationDB *
pk_init_authdb()
{
    PolKitContext *pk_context = polkit_context_new();

    // Get auth db
    PolKitAuthorizationDB *pk_auth = polkit_context_get_authorization_db(pk_context);

    return pk_auth;
}

//! Callback function that fills action list.
static polkit_bool_t
pk_action_list_cb(PolKitPolicyCache *policy_cache, PolKitPolicyFileEntry *entry, void *user_data)
{
    // Append entry to the list
    PyList_Append((PyObject*) user_data, PyString_FromString(polkit_policy_file_entry_get_id(entry)));

    // Continue to iterate
    return FALSE;
}

//! Returns a list of actions
static PyObject *
pk_action_list(PyObject *self, PyObject *args)
{
    PolKitPolicyCache *pk_cache = pk_init_cache();
    if (pk_cache == NULL) {
        return NULL;
    }

    PyObject *list = PyList_New(0);
    polkit_policy_cache_foreach(pk_cache, pk_action_list_cb, list);
    return list;
}

//! Callback function that fills annotation list
static polkit_bool_t
pk_action_info_cb(PolKitPolicyFileEntry *policy_file_entry, const char *key, const char *value, void *user_data)
{
    // Append (key, value) tuple to the list
    PyObject *tuple = PyTuple_New(2);
    PyTuple_SetItem(tuple, 0, PyString_FromString(key));
    PyTuple_SetItem(tuple, 1, PyString_FromString(value));
    PyList_Append((PyObject*) user_data, tuple);

    // Continue to iterate
    return FALSE;
}

//! Returns action details
static PyObject *
pk_action_info(PyObject *self, PyObject *args)
{
    const char* action_id;
    if (!PyArg_ParseTuple(args, "s", &action_id)) {
        return NULL;
    }

    PolKitPolicyCache *pk_cache = pk_init_cache();
    if (pk_cache == NULL) {
        return NULL;
    }

    // Get entry
    PolKitPolicyFileEntry* pk_entry = polkit_policy_cache_get_entry_by_id(pk_cache, action_id);

    PyObject *dict = PyDict_New();

    // Description
    dict_set_unless_null(dict, "description", polkit_policy_file_entry_get_action_description(pk_entry));

    // Message
    dict_set_unless_null(dict, "message", polkit_policy_file_entry_get_action_message(pk_entry));

    // Vendor
    dict_set_unless_null(dict, "vendor", polkit_policy_file_entry_get_action_vendor(pk_entry));

    // Vendor URL
    dict_set_unless_null(dict, "vendor_url", polkit_policy_file_entry_get_action_vendor_url(pk_entry));

    // Icon
    dict_set_unless_null(dict, "icon", polkit_policy_file_entry_get_action_icon_name(pk_entry));

    // Annotations
    PyObject *list = PyList_New(0);
    polkit_policy_file_entry_annotations_foreach(pk_entry, pk_action_info_cb, list);
    PyDict_SetItemString(dict, "annotations", list);

    return dict;
}

//! Callback function that fills auth list.
static polkit_bool_t
pk_auth_list_cb(PolKitAuthorizationDB *authdb, PolKitAuthorization *auth, void *user_data)
{
    PyObject *dict = PyDict_New();

    // Authorization type
    PyDict_SetItemString(dict, "type", PyInt_FromLong((long) polkit_authorization_type(auth)));

    // UID
    PyDict_SetItemString(dict, "uid", PyInt_FromLong((long) polkit_authorization_get_uid(auth)));

    // Action ID
    PyDict_SetItemString(dict, "action_id", PyString_FromString(polkit_authorization_get_action_id(auth)));

    // Time of grant
    PyDateTime_IMPORT;
    time_t rawtime = polkit_authorization_get_time_of_grant(auth);
    struct tm *timeinfo = localtime(&rawtime);
    PyDict_SetItemString(dict, "date", PyDateTime_FromDateAndTime(1900 + timeinfo->tm_year, timeinfo->tm_mon, timeinfo->tm_mday, timeinfo->tm_hour, timeinfo->tm_min, timeinfo->tm_sec, 0));

    // Append tuple to userlist
    PyList_Append((PyObject*)user_data, dict);

    // Continue to iterate
    return FALSE;
}

//! Returns granted authorizations
static PyObject *
pk_auth_list_uid(PyObject *self, PyObject *args)
{
    int uid;
    if (!PyArg_ParseTuple(args, "i", &uid)) {
        return NULL;
    }

    PolKitAuthorizationDB *pk_auth = pk_init_authdb();
    PolKitError *pk_error = NULL;

    PyObject *list = PyList_New(0);
    polkit_authorization_db_foreach_for_uid(pk_auth, uid, pk_auth_list_cb, list, &pk_error);

    if (polkit_error_is_set(pk_error)) {
        PyErr_SetString(PK_Error, polkit_error_get_error_name(pk_error));
        polkit_error_free(pk_error);
        return NULL;
    }

    return list;
}

//! Returns granted authorizations
static PyObject *
pk_auth_list_all(PyObject *self, PyObject *args)
{
    PolKitAuthorizationDB *pk_auth = pk_init_authdb();
    PolKitError *pk_error = NULL;

    PyObject *list = PyList_New(0);
    polkit_authorization_db_foreach(pk_auth, pk_auth_list_cb, list, &pk_error);

    if (polkit_error_is_set(pk_error)) {
        PyErr_SetString(PK_Error, polkit_error_get_error_name(pk_error));
        polkit_error_free(pk_error);
        return NULL;
    }
    return list;
}

//! Authorize user for the given action a single time
static PyObject *
pk_auth_add(PyObject *self, PyObject *args)
{
    const char* action_id;
    int pid, uid, type;

    if (!PyArg_ParseTuple(args, "siii", &action_id, &pid, &uid, &type)) {
        return NULL;
    }

    struct group *gr = getgrnam("polkit");
    if (gr->gr_gid != getegid()) {
        PyErr_SetString(PK_Error, "Effective GID must be 'polkit'");
        return NULL;
    }

    PolKitAuthorizationDB *pk_auth = pk_init_authdb();
    PolKitError *pk_error = NULL;

    PolKitAction *pk_action = pk_make_action(action_id);
    PolKitCaller *pk_caller = pk_make_caller_from_pid(pid);

    polkit_bool_t pk_status;

    switch (type) {
        case POLKIT_AUTHORIZATION_SCOPE_PROCESS_ONE_SHOT:
            polkit_authorization_db_add_entry_process_one_shot(pk_auth, pk_action, pk_caller, uid);
            break;
        case POLKIT_AUTHORIZATION_SCOPE_PROCESS:
            polkit_authorization_db_add_entry_process(pk_auth, pk_action, pk_caller, uid);
            break;
        case POLKIT_AUTHORIZATION_SCOPE_SESSION:
            polkit_authorization_db_add_entry_session(pk_auth, pk_action, pk_caller, uid);
            break;
        case POLKIT_AUTHORIZATION_SCOPE_ALWAYS:
            polkit_authorization_db_add_entry_always(pk_auth, pk_action, pk_caller, uid);
            break;
        default:
            PyErr_SetString(PK_Error, "Unknown authorization type.");
            return NULL;
    }

    if (pk_status) {
        Py_INCREF(Py_True);
        return Py_True;
    }
    else {
        Py_INCREF(Py_False);
        return Py_False;
    }
}

//! pypolkit methods
static PyMethodDef polkit_methods[] = {
    {"action_list", (PyCFunction) pk_action_list, METH_NOARGS, "Lists all actions."},
    {"action_info", (PyCFunction) pk_action_info, METH_VARARGS, "Get action details."},
    {"auth_list_uid", (PyCFunction) pk_auth_list_uid, METH_VARARGS, "List granted authorizations for specified UID."},
    {"auth_list_all", (PyCFunction) pk_auth_list_all, METH_NOARGS, "List granted authorizations."},
    {"auth_add", (PyCFunction) pk_auth_add, METH_VARARGS, "Authorize user for the given action."},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC
initpypolkit(void)
{
    PyObject *m = Py_InitModule("pypolkit", polkit_methods);

    PyModule_AddObject(m, "SCOPE_ONE_SHOT", PyInt_FromLong((long) POLKIT_AUTHORIZATION_SCOPE_PROCESS_ONE_SHOT));
    PyModule_AddObject(m, "SCOPE_PROCESS", PyInt_FromLong((long) POLKIT_AUTHORIZATION_SCOPE_PROCESS));
    PyModule_AddObject(m, "SCOPE_SESSION", PyInt_FromLong((long) POLKIT_AUTHORIZATION_SCOPE_SESSION));
    PyModule_AddObject(m, "SCOPE_ALWAYS", PyInt_FromLong((long) POLKIT_AUTHORIZATION_SCOPE_ALWAYS));

    PyModule_AddObject(m, "TYPE_UID", PyInt_FromLong((long) POLKIT_AUTHORIZATION_TYPE_UID));

    PyModule_AddObject(m, "DB_CAPABILITY_CAN_OBTAIN", PyInt_FromLong((long) POLKIT_AUTHORIZATION_DB_CAPABILITY_CAN_OBTAIN));

    PK_Error = PyErr_NewException("pypolkit.error", NULL, NULL);
    Py_INCREF(PK_Error);
    PyModule_AddObject(m, "error", PK_Error);
}
