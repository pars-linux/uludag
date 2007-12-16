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
#include <string.h>
#include <stdlib.h>

#include "trans.h"

char *
strsub(const char *str, int start, int end)
{
    /*!
     * Returns part of a string.
     *
     * @str String
     * @start Where to start
     * @end Where to end
     * @return Requested part
     */

    if (start < 0) {
        start = strlen(str) + start;
    }
    if (start > strlen(str)) {
        start = 0;
    }
    if (end == 0) {
        end = strlen(str);
    }
    else if (end < 0) {
        end = strlen(str) + end;
    }
    if (end > strlen(str)) {
        end = strlen(str);
    }

    char *new_src, *t;
    new_src = malloc(end - start + 2);
    for (t = (char *) str + start; t < str + end; t++) {
        new_src[t - (str + start)] = *t;
    }
    new_src[t - (str + start)] = '\0';
    return new_src;
}

//! Returns DBus signature of a Python object
static char
dbus_py_get_signature(PyObject *obj)
{
    /*!
     * This method can be used to get type of given Python object.
     *
     * @obj Python object
     * @return Signature
     */

    if (obj == Py_None) {
        return 'n';
    }
    else if (PyString_Check(obj)) {
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
        return 'r';
    }
    else if (PyList_Check(obj)) {
        return 'a';
    }
    else if (PyDict_Check(obj)) {
        return 'D';
    }
    return '?';
}

//! Returns DBus signature of a Python object including it's content.
char *
dbus_py_get_object_signature(PyObject *obj)
{
    /*!
     * Returns signature of a Python object including it's content.
     *
     * @obj Python object
     * @return Signature, or NULL on error
     */

    int i;
    int size;
    char *sign_content, *sign_subcontent;
    char sign, sign_sub;
    PyObject *item, *item2;

    sign = dbus_py_get_signature(obj);

    switch (sign) {
        case 's':
        case 'b':
        case 'i':
        case 'l':
        case 'd':
            size = 2;
            sign_content = malloc(size);
            snprintf(sign_content, size, "%c\0", sign);
            return sign_content;
        case 'n':
            size = 2;
            sign_content = malloc(size);
            snprintf(sign_content, size, "s\0");
            return sign_content;
        case 'a':
            if (PyList_Size(obj) > 0) {
                item = PyList_GetItem(obj, 0);
            }
            else {
                item = PyString_FromString("");
            }
            sign_subcontent = dbus_py_get_object_signature(item);
            if (!sign_subcontent) {
                return NULL;
            }
            size = 2 + strlen(sign_subcontent);
            sign_content = malloc(size);
            snprintf(sign_content, size, "a%s\0", sign_subcontent);
            free(sign_subcontent);
            return sign_content;
        case 'r':
            size = 3;
            sign_content = malloc(size);
            snprintf(sign_content, size, "(\0");
            for (i = 0; i < PyTuple_Size(obj); i++) {
                item = PyTuple_GetItem(obj, i);
                sign_subcontent = dbus_py_get_object_signature(item);
                if (!sign_subcontent) {
                    free(sign_content);
                    return NULL;
                }
                size = size + strlen(sign_subcontent);
                sign_content = realloc(sign_content, size);
                strncat(sign_content, sign_subcontent, size);
                free(sign_subcontent);
            }
            strncat(sign_content, ")", 1);
            return sign_content;
        case 'D':
            if (PyDict_Size(obj) > 0) {
            i = 0;
                PyDict_Next(obj, &i, &item, &item2);
            }
            else {
                item = PyString_FromString("");
                item2 = PyString_FromString("");
            }
            sign_subcontent = dbus_py_get_object_signature(item2);
            if (!sign_subcontent) {
                return NULL;
            }
            size = 4 + strlen(sign_subcontent);
            sign_content = malloc(size);
            snprintf(sign_content, size, "{%c%s}\0", dbus_py_get_signature(item), sign_subcontent);
            free(sign_subcontent);
            return sign_content;
        default:
            return NULL;
    }
}

//! Converts a Python object to DBus format.
int
dbus_py_export(DBusMessageIter *iter, PyObject *obj)
{
    /*!
     * Converts a Python object to DBus fotmat.
     *
     * @iter Iterator to append message to
     * @obj Python object
     * @return 0 on success, 1 on error
     */

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
    int size;
    int i = 0;

    char sign;
    char *sign_container, *sign_sub;
    int sign_size;

    const dbus_int32_t array[] = {};
    const dbus_int32_t *v_ARRAY = array;

    sign = dbus_py_get_signature(obj);

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
            sign_container = dbus_py_get_object_signature(obj);
            if (!sign_container) {
                PyErr_SetString(PyExc_TypeError, "Array returned by function contains unknown data type.");
                return 1;
            }
            sign_sub = (char *) strsub(sign_container, 1, 0);
            if (sign_sub[0] == '{') {
                // If content is a dictionary, container signature 'a' must be included.
                e = dbus_message_iter_open_container(iter, DBUS_TYPE_ARRAY, sign_container, &sub);
            }
            else {
                e = dbus_message_iter_open_container(iter, DBUS_TYPE_ARRAY, sign_sub, &sub);
            }
            free(sign_sub);
            free(sign_container);
            if (!e) break;
            for (i = 0; i < PyList_Size(obj); i++) {
                item = PyList_GetItem(obj, i);
                dbus_py_export(&sub, item);
            }
            dbus_message_iter_close_container(iter, &sub);
            break;
        case 'r':
            sign_container = dbus_py_get_object_signature(obj);
            if (!sign_container) {
                PyErr_SetString(PyExc_TypeError, "Tuple returned by function contains unknown data type.");
                return 1;
            }
            // Empty tuples not allowed
            if (PyTuple_Size(obj) > 0) {
                e = dbus_message_iter_open_container(iter, DBUS_TYPE_STRUCT, NULL, &sub);
                if (!e) break;
                for (i = 0; i < PyTuple_Size(obj); i++) {
                    item = PyTuple_GetItem(obj, i);
                    dbus_py_export(&sub, item);
                }
                dbus_message_iter_close_container(iter, &sub);
            }
            break;
        case 'D':
            sign_container = dbus_py_get_object_signature(obj);
            if (!sign_container) {
                PyErr_SetString(PyExc_TypeError, "Dictionary returned by function contains unknown data type.");
                return 1;
            }
            e = dbus_message_iter_open_container(iter, DBUS_TYPE_ARRAY, sign_container, &sub);
            free(sign_container);
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
        case 'n':
            p.s = "";
            e = dbus_message_iter_append_basic(iter, DBUS_TYPE_STRING, &p.s);
            break;
        default:
            PyErr_SetString(PyExc_TypeError, "Unknown data type returned by function.");
            return 1;
    }
    // FIXME - cleanup?
    if (!e) {
        PyErr_SetString(PyExc_TypeError, "no memory");
        return 1;
    }

    return 0;
}

//! Converts a DBus argument to Python object
PyObject *
dbus_py_get_item(DBusMessageIter* iter)
{
    /*!
     * Converts a DBus argument to Python object.
     *
     * @iter Iterator to append message to
     * @return Python object
     */

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
        case DBUS_TYPE_BYTE:
        case DBUS_TYPE_SIGNATURE:
        case DBUS_TYPE_OBJECT_PATH:
        case DBUS_TYPE_VARIANT:
            // FIXME
            break;
    }
    return ret;
}

//! Converts a dictionary entry array to Python dictionary
PyObject *
dbus_py_get_dict(DBusMessageIter *iter)
{
    /*!
     * Converts a dictionary entry array to Python dictionary.
     *
     * @iter Iterator to get object from
     * @return Python object, or NULL on error
     */

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

//! Converts an array to Python list
PyObject *
dbus_py_get_list(DBusMessageIter *iter)
{
    /*
     * Converts an array to Python list
     *
     * @iter Iterator to get object from
     * @return Python object, or NULL on error
     */

    int type;
    PyObject *ret = PyList_New(0);

    while ((type = dbus_message_iter_get_arg_type(iter)) != DBUS_TYPE_INVALID) {
        PyList_Append(ret, dbus_py_get_item(iter));
        dbus_message_iter_next(iter);
    }
    return ret;
}

//! Converts DBus message's arguments to Python object
PyObject *
dbus_py_import(DBusMessage *msg)
{
    /*!
     * Extracts arguments of a DBus message and converts it to a Python object
     *
     * @msg DBus message to get objects from
     * @return Python object
     */

    DBusMessageIter iter;
    dbus_message_iter_init(msg, &iter);
    return dbus_py_get_list(&iter);
}
