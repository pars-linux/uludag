/*
** Copyright (c) 2005-2006, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <X11/Xlib.h>
#include <Python.h>

/* mostly stolen from KDM code. */
static PyObject*
locked(void)
{
    unsigned int lmask;
    Window dummy1, dummy2;
    int dummy3, dummy4, dummy5, dummy6;
    Display *disp = 0;

    // ops... we need our own display ;).
    disp = XOpenDisplay(NULL);
    if (!disp){
        return Py_False;
    }

    XQueryPointer( disp, DefaultRootWindow( disp ),
	    &dummy1, &dummy2, &dummy3, &dummy4, &dummy5, &dummy6,
        &lmask );

    XFlush(disp);
    XCloseDisplay(disp);

    if (lmask & LockMask) {
        return Py_True;
    }
 
    return Py_False;
}


static PyMethodDef capslocked_methods[] = {
    {"locked", locked, METH_NOARGS, NULL},
    {NULL}
};


PyMODINIT_FUNC
initcapslocked(void) 
{
    PyObject* m;

    m = Py_InitModule("capslocked", capslocked_methods);
}
