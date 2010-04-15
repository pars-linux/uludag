/*
* Copyright (c) 2008, TUBITAK/UEKAE
*
* Permission is hereby granted, free of charge, to any person
* obtaining a copy of this software and associated documentation
* files (the "Software"), to deal in the Software without
* restriction, including without limitation the rights to use, copy,
* modify, merge, publish, distribute, sublicense, and/or sell copies
* of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be
* included in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
* EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
* MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
* NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
* HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
* WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
* DEALINGS IN THE SOFTWARE.
*
*/

#include <Python.h>
#include <datetime.h>
#include <unistd.h>
#include <glib.h>
#include <polkit/polkit.h>

//! Standard exception for polkit
static PyObject *PK_Error;

//! Sets key of dictionary if value is not null
static void
dict_set_unless_null(PyObject *dict, const char *key, const char *value)
{
    if (value != NULL) {
        PyDict_SetItemString(dict, key, PyString_FromString(value));
    }
}

//! Returns a list of actions
static PyObject *
pk_action_list(PyObject *self, PyObject *args)
{
    g_type_init();

    GError *error = NULL;
    GList *glist, *gitem;
    PolkitAuthority *authority;
    PyObject *py_list = PyList_New(0);

    authority = polkit_authority_get();

    glist = polkit_authority_enumerate_actions_sync(authority, NULL, &error);
    for (gitem = glist; gitem; gitem = g_list_next(gitem)) {
        gpointer data = gitem->data;
        PyList_Append(py_list, PyString_FromString(polkit_action_description_get_action_id(data)));
    }

    // g_list_free(glist);
    // g_list_free(gitem);

    return py_list;
}

//! Returns action details
static PyObject *
pk_action_info(PyObject *self, PyObject *args)
{
    const char* action_id;
    if (!PyArg_ParseTuple(args, "s", &action_id)) {
        return NULL;
    }

    PyObject *dict = PyDict_New();

    // Description
    dict_set_unless_null(dict, "description", NULL);

    // Message
    dict_set_unless_null(dict, "message", NULL);

    // Vendor
    dict_set_unless_null(dict, "vendor", NULL);

    // Vendor URL
    dict_set_unless_null(dict, "vendor_url", NULL);

    // Icon
    dict_set_unless_null(dict, "icon", NULL);

    // Annotations
    PyObject *list = PyList_New(0);
    PyDict_SetItemString(dict, "annotations", list);

    // Default policy
    PyDict_SetItemString(dict, "policy_any", NULL);
    PyDict_SetItemString(dict, "policy_active", NULL);
    PyDict_SetItemString(dict, "policy_inactive", NULL);

    return dict;
}

//! Returns granted authorizations
static PyObject *
pk_auth_list_uid(PyObject *self, PyObject *args)
{
    int uid;
    if (!PyArg_ParseTuple(args, "i", &uid)) {
        return NULL;
    }

    PyObject *list = PyList_New(0);

    return list;
}

//! Returns granted authorizations
static PyObject *
pk_auth_list_all(PyObject *self, PyObject *args)
{
    PyObject *list = PyList_New(0);
    return list;
}

//! Authorize user for the given action a single time
static PyObject *
pk_auth_add(PyObject *self, PyObject *args)
{
    const char* action_id;
    int pid = -1;
    int uid = -1;
    int type = -1;

    if (!PyArg_ParseTuple(args, "sii|i", &action_id, &type, &uid, &pid)) {
        return NULL;
    }

    Py_INCREF(Py_False);
    return Py_False;
}

//! Revoke all authorizations of given user
static PyObject *
pk_auth_revoke_all(PyObject *self, PyObject *args)
{
    int uid = -1;

    if (!PyArg_ParseTuple(args, "i", &uid)) {
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

//! Revoke authorizations of given user for given action_id
static PyObject *
pk_auth_revoke(PyObject *self, PyObject *args)
{
    int uid = -1;
    const char *action_id;

    if (!PyArg_ParseTuple(args, "is", &uid, &action_id)) {
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

//! Grants a negative authorization to a user for a specific action
static PyObject *
pk_auth_block(PyObject *self, PyObject *args)
{
    int uid = -1;
    const char *action_id;

    if (!PyArg_ParseTuple(args, "is", &uid, &action_id)) {
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

//! polkit methods
static PyMethodDef polkit_methods[] = {
    {"action_list", (PyCFunction) pk_action_list, METH_NOARGS, "Lists all actions."},
    {"action_info", (PyCFunction) pk_action_info, METH_VARARGS, "Get action details."},
    {"auth_list_uid", (PyCFunction) pk_auth_list_uid, METH_VARARGS, "List granted authorizations for specified UID."},
    {"auth_list_all", (PyCFunction) pk_auth_list_all, METH_NOARGS, "List granted authorizations."},
    {"auth_add", (PyCFunction) pk_auth_add, METH_VARARGS, "Authorize user for the given action."},
    {"auth_revoke_all", (PyCFunction) pk_auth_revoke_all, METH_VARARGS, "Revoke all authorizations of given user."},
    {"auth_revoke", (PyCFunction) pk_auth_revoke, METH_VARARGS, "Revoke authorization of given user for the given action."},
    {"auth_block", (PyCFunction) pk_auth_block, METH_VARARGS, "Grant a negative authorization to a user for a specific action."},
    {NULL, NULL, 0, NULL}
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

PyMODINIT_FUNC
init_polkit(void)
{
    PyObject *m = Py_InitModule3("_polkit", polkit_methods, "module for querying system-wide policy");

    if (m == NULL)
      return;

    PyModule_AddObject(m, "SCOPE_ONE_SHOT", PyInt_FromLong((long) 0));
    PyModule_AddObject(m, "SCOPE_PROCESS", PyInt_FromLong((long) 0));
    PyModule_AddObject(m, "SCOPE_SESSION", PyInt_FromLong((long) 0));
    PyModule_AddObject(m, "SCOPE_ALWAYS", PyInt_FromLong((long) 0));

    PyModule_AddObject(m, "TYPE_UID", PyInt_FromLong((long) 0));

    PyModule_AddObject(m, "DB_CAPABILITY_CAN_OBTAIN", PyInt_FromLong((long) 0));

    PyModule_AddObject(m, "CONSTRAINT_TYPE_REQUIRE_LOCAL", PyInt_FromLong((long) 0));
    PyModule_AddObject(m, "CONSTRAINT_TYPE_REQUIRE_ACTIVE", PyInt_FromLong((long) 0));
    PyModule_AddObject(m, "CONSTRAINT_TYPE_REQUIRE_EXE", PyInt_FromLong((long) 0));
    PyModule_AddObject(m, "CONSTRAINT_TYPE_REQUIRE_SELINUX_CONTEXT", PyInt_FromLong((long) 0));

    PK_Error = PyErr_NewException("polkit.error", NULL, NULL);
    Py_INCREF(PK_Error);
    PyModule_AddObject(m, "error", PK_Error);
}
