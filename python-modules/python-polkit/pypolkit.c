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
#include <time.h>
#include <datetime.h>

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

//! Init policy cache
PolKitPolicyCache *
pk_init()
{
    PolKitError *pk_error;
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
    PolKitPolicyCache *pk_cache = pk_init();
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

    PolKitPolicyCache *pk_cache = pk_init();
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

//! pypolkit methods
static PyMethodDef polkit_methods[] = {
    {"action_list", (PyCFunction) pk_action_list, METH_NOARGS, "Lists all actions."},
    {"action_info", (PyCFunction) pk_action_info, METH_VARARGS, "Get action details."},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC
initpypolkit(void)
{
    PyObject *m = Py_InitModule("pypolkit", polkit_methods);

    PK_Error = PyErr_NewException("pypolkit.error", NULL, NULL);
    Py_INCREF(PK_Error);
    PyModule_AddObject(m, "error", PK_Error);
}
