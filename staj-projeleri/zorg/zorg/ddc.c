/*
* Copyright (c) 2007, TUBITAK/UEKAE
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License as published by the
* Free Software Foundation; either version 2 of the License, or (at your
* option) any later version. Please read the COPYING file.
*/

#include <Python.h>
#include <libx86.h>

#include "vbe.h"

#define SQR(x) ((x) * (x))

PyDoc_STRVAR(query__doc__,
	"query(adapter)\n"
	"\n"
	"Query DDC and return followings:\n"
	"((hmin, hmax), (vmin, vmax), eisa_id)\n");

PyObject*
ddc_query(PyObject *self, PyObject *args)
{
	PyObject *r, *horiz, *vert, *eisa;
	int adapter;
	struct vbe_edid1_info *edid;
	unsigned char hmin, hmax, vmin, vmax;
	char eisa_id[8] = {0};

	if (!PyArg_ParseTuple(args, "i", &adapter))
		return NULL;

	if (!vbe_get_edid_supported(adapter)) {
		Py_INCREF(Py_None);
		return Py_None;
	}
	
	if ((edid = vbe_get_edid_info(adapter)) == NULL) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	if (edid->version == 255 && edid->revision == 255) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	vbe_get_edid_ranges(edid, &hmin, &hmax, &vmin, &vmax);

	if (hmin > hmax || vmin > vmax) {
		Py_INCREF(Py_None);
		return Py_None;
	}

	if (edid->max_size_horizontal != 127 && edid->max_size_vertical != 127) {
		char manufacturer[4];
		double size = sqrt(SQR(edid->max_size_horizontal) +
					SQR(edid->max_size_vertical)) / 2.54;
		manufacturer[0] = edid->manufacturer_name.char1 + 'A' - 1;
		manufacturer[1] = edid->manufacturer_name.char2 + 'A' - 1;
		manufacturer[2] = edid->manufacturer_name.char3 + 'A' - 1;
		manufacturer[3] = '\0';
		//printf(size ? "%3.2f inches monitor (truly %3.2f')  EISA ID=%s%04x\n" : "\n", size * 1.08, size, manufacturer, edid->product_code);
		sprintf(eisa_id, "%s%04x", manufacturer, edid->product_code);
	}

	r = PyTuple_New(3);
	horiz = Py_BuildValue("ii", hmin, hmax);
	vert = Py_BuildValue("ii", vmin, vmax);
	eisa = Py_BuildValue("s", eisa_id);
	PyTuple_SET_ITEM(r, 0, horiz);
	PyTuple_SET_ITEM(r, 1, vert);
	PyTuple_SET_ITEM(r, 2, eisa);

	return r;
}

static PyMethodDef ddc_methods[] = {
	{"query", (PyCFunction)ddc_query, METH_VARARGS, query__doc__},
	{NULL, NULL}
};

PyMODINIT_FUNC
initddc(void)
{
	PyObject *m;

	m = Py_InitModule("ddc", ddc_methods);

	return;
}
