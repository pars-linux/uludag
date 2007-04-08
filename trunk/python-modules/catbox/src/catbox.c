/*
** Copyright (c) 2006-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include "catbox.h"

#include <sys/wait.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/ptrace.h>
#include <linux/user.h>
#include <linux/unistd.h>

static PyObject *
catbox_run(PyObject *self, PyObject *args, PyObject *kwargs)
{
	static char *kwlist[] = {
		"function",
		"writable_paths",
		"network",
		NULL
	};
	PyObject *ret;
	PyObject *paths = NULL;
	PyObject *net = NULL;
	struct trace_context ctx;

	memset(&ctx, 0, sizeof(struct trace_context));

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|OO", kwlist, &ctx.func, &paths, &net))
		return NULL;

	if (PyCallable_Check(ctx.func) == 0) {
		PyErr_SetString(PyExc_TypeError, "First argument should be a callable function");
		return NULL;
	}

	if (paths) {
		ctx.pathlist = make_pathlist(paths);
		if (!ctx.pathlist) return NULL;
	}

	if (net == NULL || PyObject_IsTrue(net))
		ctx.network_allowed = 1;
	else
		ctx.network_allowed = 0;

	catbox_retval_init(&ctx);

	// setup is complete, run sandbox
	ret = catbox_core_run(&ctx);

	if (ctx.pathlist) {
		free_pathlist(ctx.pathlist);
	}

	return ret;
}

static PyMethodDef methods[] = {
	{ "run", (PyCFunction) catbox_run, METH_VARARGS | METH_KEYWORDS,
	  "Run given function in a sandbox."},
	{ NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC
initcatbox(void)
{
	PyObject *m;

	m = Py_InitModule("catbox", methods);
}
