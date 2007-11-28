/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <dbus/dbus.h>
#include <Python.h>
#include <node.h>

#include "cfg.h"
#include "log.h"
#include "utility.h"

int
py_in_tuple(PyObject *tuple, PyObject *item)
{
    int i;
    for (i = 0; i < PyTuple_Size(tuple); i++) {
        if (strcmp(PyString_AsString(item), PyString_AsString(PyTuple_GetItem(tuple, i))) == 0) {
            return 1;
        }
    }
    return 0;
}

//! Call model's method with given arguments
PyObject *
py_call_method(const char *model, const char *path, const char *method, PyObject *args)
{
    /*!
    Call model's method with given arguments.
    @return Returns PyObject returned by model's method.
    */
    PyObject *pCode, *pModule, *pDict, *pFunc, *pReturn, *pStr;
    PyObject *argNames, *pArgs, *pkArgs;
    PyObject *pKey, *pValue, *pItem;
    PyObject *pFuncCode;
    node *n;
    int arg_count;
    int i;

    char *script_path = get_script_path(model, path);
    char *code = load_file(script_path, NULL);
    free(script_path);

    n = PyParser_SimpleParseString(code, Py_file_input);
    free(code);
    if (!n) {
        return NULL;
    }

    pCode = (PyObject *) PyNode_Compile(n, "lala");
    PyNode_Free(n);
    if (!pCode) {
        return NULL;
    }

    pModule = PyImport_ExecCodeModule("csl", pCode);
    Py_DECREF(pCode);

    if (!pModule || !PyModule_Check(pModule)) {
        return NULL;
    }

    pDict = PyModule_GetDict(pModule);
    if (!pDict) {
        Py_DECREF(pModule);
        return NULL;
    }

    pFunc = PyDict_GetItemString(pDict, method);
    if (!pFunc || !PyCallable_Check(pFunc)) {
        Py_DECREF(pModule);
        return NULL;
    }

    pFuncCode = PyObject_GetAttrString(pFunc, "func_code");
    arg_count = PyInt_AsLong(PyObject_GetAttrString(pFuncCode, "co_argcount"));
    argNames = PyObject_GetAttrString(pFuncCode, "co_varnames");
    argNames = PyTuple_GetSlice(argNames, 0, arg_count);

    pArgs = PyTuple_New(0);
    pkArgs = PyDict_New();

    for (i = 0; i < PyTuple_Size(args); i++) {
        pKey = PyTuple_GetItem(PyTuple_GetItem(args, i), 0);
        pValue = PyTuple_GetItem(PyTuple_GetItem(args, i), 1);
        if (!py_in_tuple(argNames, pKey)) {
            continue;
        }
        PyDict_SetItem(pkArgs, pKey, pValue);
    }

    pReturn = PyObject_Call(pFunc, pArgs, pkArgs);

    if (!pReturn) {
        Py_DECREF(pModule);
        return NULL;
    }
    Py_DECREF(pModule);
    return pReturn;
}

// PyObject -> DBusMessage translation
static char
dbus_py_get_signature(PyObject *obj)
{
    if (PyString_Check(obj)) {
        return 's';
    }
    else if (PyBool_Check(obj)) {
        return 'b';
    }
    else if (PyInt_Check(obj)) {
        return 'i';
    }
    else if (PyLong_Check(obj)) {
        return 'l';
    }
    else if (PyFloat_Check(obj)) {
        return 'd';
    }
    else if (PyTuple_Check(obj)) {
        return 'v';
    }
    else if (PyList_Check(obj)) {
        return 'a';
    }
    else if (PyDict_Check(obj)) {
        return 'D';
    }
    return '?';
}

void
dbus_py_export(DBusMessageIter *iter, PyObject *obj)
{
    union {
        const char *s;
        unsigned char y;
        dbus_bool_t b;
        double d;
        dbus_int16_t i16;
        dbus_int32_t i32;
        dbus_uint64_t u64;
        dbus_int64_t i64;
    } p;

    int e;
    DBusMessageIter sub, sub2;
    PyObject *item;
    PyObject *key, *value;
    const char sign = dbus_py_get_signature(obj);
    char sign_sub[5];
    int size;
    int i = 0;

    const dbus_int32_t array[] = {};
    const dbus_int32_t *v_ARRAY = array;

    switch (sign) {
        case 's':
            p.s = PyString_AsString(obj);
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_STRING, &p.s);
            break;
        case 'b':
            p.b = (long)PyInt_AsLong(obj);
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_BOOLEAN, &p.b);
            break;
        case 'i':
            p.i32 = PyInt_AsLong(obj);
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_INT32, &p.i32);
            break;
        case 'l':
            p.i64 = PyLong_AsLong(obj);
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_INT64, &p.i64);
            break;
        case 'd':
            p.d = PyFloat_AsDouble(obj);
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_DOUBLE, &p.d);
            break;
        case 'a':
            size = PyList_Size(obj);
            // Find content signature
            if (size == 0) {
                snprintf(sign_sub, 2, "s\0");
            }
            else {
                item = PyList_GetItem(obj, 0);
                snprintf(sign_sub, 2, "%c\0", dbus_py_get_signature(item));
            }
            e = dbus_message_iter_open_container(iter, DBUS_TYPE_ARRAY, sign_sub, &sub);
            if (!e) break;
            for (i = 0; i < size; i++) {
                item = PyList_GetItem(obj, i);
                dbus_py_export(&sub, item);
            }
            dbus_message_iter_close_container(iter, &sub);
            break;
        case 'v':
            size = PyTuple_Size(obj);
            e = dbus_message_iter_open_container(iter, DBUS_TYPE_STRUCT, NULL, &sub);
            if (!e) break;
            for (i = 0; i < size; i++) {
                item = PyTuple_GetItem(obj, i);
                dbus_py_export(&sub, item);
            }
            dbus_message_iter_close_container(iter, &sub);
            break;
        case 'D':
            size = PyDict_Size(obj);
            // Find content signature
            if (size == 0) {
                snprintf(sign_sub, 5, "{ss}\0");
            }
            else {
                i = 0; // Go to first index
                PyDict_Next(obj, &i, &key, &value);
                snprintf(sign_sub, 5, "{%c%c}\0", dbus_py_get_signature(key), dbus_py_get_signature(value));
            }
            e = dbus_message_iter_open_container(iter, DBUS_TYPE_ARRAY, sign_sub, &sub);
            if (!e) break;
            i = 0; // Go to first index
            while (PyDict_Next(obj, &i, &key, &value)) {
                dbus_message_iter_open_container(&sub, DBUS_TYPE_DICT_ENTRY, NULL, &sub2);
                dbus_py_export(&sub2, key);
                dbus_py_export(&sub2, value);
                dbus_message_iter_close_container(&sub, &sub2);
            }
            dbus_message_iter_close_container(iter, &sub);
            break;
        default:
            log_error("Unknown data type returned by function: %s\n", sign);
    }
    // FIXME - cleanup?
    if (!e) {
        log_error("DBus: Out Of Memory!\n");
        exit(1);
    }
}


// DBusMessageIter -> PyObject translation
PyObject *
dbus_py_get_list(DBusMessageIter *iter);

PyObject *
dbus_py_get_dict(DBusMessageIter *iter);

PyObject *
dbus_py_get_item(DBusMessageIter* iter)
{
    union {
        const char *s;
        unsigned char y;
        dbus_bool_t b;
        double d;
        dbus_uint16_t u16;
        dbus_int16_t i16;
        dbus_uint32_t u32;
        dbus_int32_t i32;
        dbus_uint64_t u64;
        dbus_int64_t i64;
    } obj;

    PyObject *ret;
    DBusMessageIter sub, entries;
    int type = dbus_message_iter_get_arg_type(iter);

    switch (type) {
        case DBUS_TYPE_STRING:
            dbus_message_iter_get_basic(iter, &obj.s);
            ret = Py_BuildValue("s", obj.s);
            // ret = Py_BuildValue("N", PyUnicode_DecodeUTF8(obj.s, strlen(obj.s), NULL));
            break;
        case DBUS_TYPE_DOUBLE:
            dbus_message_iter_get_basic(iter, &obj.d);
            ret = Py_BuildValue("f", obj.d);
            break;
        case DBUS_TYPE_INT16:
            dbus_message_iter_get_basic(iter, &obj.i16);
            ret = Py_BuildValue("i", (int)obj.i16);
            break;
        case DBUS_TYPE_UINT16:
            dbus_message_iter_get_basic(iter, &obj.u16);
            ret = Py_BuildValue("i", (int)obj.u16);
            break;
        case DBUS_TYPE_INT32:
            dbus_message_iter_get_basic(iter, &obj.i32);
            ret = Py_BuildValue("l", (long)obj.i32);
            break;
        case DBUS_TYPE_UINT32:
            dbus_message_iter_get_basic(iter, &obj.u32);
            ret = Py_BuildValue("k", (unsigned long)obj.u32);
            break;
        case DBUS_TYPE_INT64:
            dbus_message_iter_get_basic(iter, &obj.i64);
            ret = Py_BuildValue("L", (PY_LONG_LONG)obj.i64);
            break;
        case DBUS_TYPE_UINT64:
            dbus_message_iter_get_basic(iter, &obj.u64);
            ret = Py_BuildValue("K", (PY_LONG_LONG)obj.u64);
            break;
        case DBUS_TYPE_BOOLEAN:
            dbus_message_iter_get_basic(iter, &obj.b);
            ret = (long)obj.b == 1 ? Py_True : Py_False;
            break;
        case DBUS_TYPE_BYTE:
        case DBUS_TYPE_SIGNATURE:
        case DBUS_TYPE_OBJECT_PATH:
            // FIXME
            break;
        case DBUS_TYPE_DICT_ENTRY:
            break;
        case DBUS_TYPE_ARRAY:
            type = dbus_message_iter_get_element_type(iter);
            if (type == DBUS_TYPE_DICT_ENTRY) {
                dbus_message_iter_recurse(iter, &sub);
                ret = dbus_py_get_dict(&sub);
            }
            else if (type == DBUS_TYPE_BYTE) {
                // FIXME
            }
            else {
                dbus_message_iter_recurse(iter, &sub);
                ret = dbus_py_get_list(&sub);
            }
            break;
        case DBUS_TYPE_STRUCT:
            dbus_message_iter_recurse(iter, &sub);
            ret = PyList_AsTuple(dbus_py_get_list(&sub));
            break;
        case DBUS_TYPE_VARIANT:
            dbus_message_iter_recurse(iter, &sub);
            dbus_message_iter_recurse(&sub, &sub);
            ret = PyList_AsTuple(dbus_py_get_list(&sub));
            break;
    }
    return ret;
}

PyObject *
dbus_py_get_dict(DBusMessageIter *iter)
{
    int type;
    PyObject *ret = PyDict_New();
    while (dbus_message_iter_get_arg_type(iter) == DBUS_TYPE_DICT_ENTRY) {
        PyObject *key = NULL;
        PyObject *value = NULL;
        DBusMessageIter kv;

        dbus_message_iter_recurse(iter, &kv);

        key = dbus_py_get_item(&kv);
        if (!key) {
            Py_DECREF(ret);
            return NULL;
        }
        dbus_message_iter_next(&kv);

        value = dbus_py_get_item(&kv);
        if (!value) {
            Py_DECREF(ret);
            Py_DECREF(key);
            return NULL;
        }

        PyDict_SetItem(ret, key, value);
        Py_DECREF(key);
        Py_DECREF(value);

        dbus_message_iter_next(iter);
    }
    return ret;
}

PyObject *
dbus_py_get_list(DBusMessageIter *iter)
{
    int type;
    PyObject *ret = PyList_New(0);

    while ((type = dbus_message_iter_get_arg_type(iter)) != DBUS_TYPE_INVALID) {
        PyList_Append(ret, dbus_py_get_item(iter));
        dbus_message_iter_next(iter);
    }
    return ret;
}

PyObject *
dbus_py_import(DBusMessage *msg)
{
    DBusMessageIter iter;
    dbus_message_iter_init(msg, &iter);
    return dbus_py_get_list(&iter);
}
