/*
** Copyright (c) 2005, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#include "csl.h"
#include "process.h"
#include "data.h"
#include "model.h"
#include "log.h"
#include "ipc.h"

static unsigned char *
load_file(const char *fname, int *sizeptr)
{
	FILE *f;
	struct stat fs;
	size_t size;
	unsigned char *data;

	// FIXME: this function sucks
	if (stat (fname, &fs) != 0) {
		printf ("Cannot stat file '%s'\n", fname);
		return NULL;
	}
	size = fs.st_size;
	if (sizeptr) *sizeptr = size;

	data = malloc (size + 1);
	if (!data) {
		printf ("Cannot allocate %d bytes\n", size);
		return NULL;
	}
	memset(data, 0, size + 1);

	f = fopen (fname, "rb");
	if (!f) {
		printf ("Cannot open file '%s'\n", fname);
		return NULL;
	}

	if (fread (data, size, 1, f) < 1) {
		printf ("Read error in file '%s'\n", fname);
		return NULL;
	}

	fclose (f);
	return data;
}

static void *chan;
static int chan_id;

static int
send_result(int cmd, const char *data, size_t size)
{
	ipc_start(cmd, chan, chan_id, 0);
	if (data) {
		if (size == 0) size = strlen(data);
		ipc_pack_arg(data, size);
	}
	ipc_send(TO_PARENT);
	return 0;
}

static int
do_register(int node, const char *app, const char *fname)
{
	char *buf;
	char *code;
	size_t codelen;
	int e;

	log_debug(LOG_JOB, "Register(%s,%s,%s)\n", model_get_path(node), app, fname);

	csl_setup();

	buf = load_file(fname, NULL);
	if (!buf) {
		send_result(CMD_FAIL, "no file", 7);
		return -1;
	}

	e = csl_compile(buf, "test", &code, &codelen);
	if (e) {
		send_result(CMD_FAIL, "compile error", 13);
		return -1;
	}

	db_put_script(node, app, code, codelen);

	send_result(CMD_RESULT, "registered", 10);

	csl_cleanup();

	return 0;
}

static int
do_remove(const char *app)
{
	log_debug(LOG_JOB, "Remove(%s)\n", app);

	db_del_app(app);
	return 0;
}

static int
do_execute(int node, const char *app)
{
	char *code;
	char *res;
	size_t code_size;
	size_t res_size;
	int e;

	log_debug(LOG_JOB, "Execute(%s,%s)\n", model_get_path(node), app);

	csl_setup();

	if (0 != db_get_code(model_parent(node), app, &code, &code_size)) return -1;
	e = csl_execute(code, code_size, model_get_method(node), &res, &res_size);
	if (e) {
		send_result(CMD_FAIL, "err", 3);
	} else {
		send_result(CMD_RESULT, res, res_size);
	}
	free(res);

	csl_cleanup();

	return e;
}

int bk_node;
char *bk_app;

static void
exec_proc(void)
{
	do_execute(bk_node, bk_app);
}

static int
do_call(int node)
{
	char *apps;

	log_debug(LOG_JOB, "Call(%s)\n", model_get_path(node));

	if (db_get_apps(model_parent(node), &apps) != 0) {
		send_result(CMD_FAIL, "no app", 6);
		exit(1);
	}

	if (strchr(apps, '/') == NULL) {
		// there is only one script
		do_execute(node, apps);
	} else {
		// multiple scripts, run concurrently
		char *t, *s;
		struct ProcChild *p;
		int cmd;
		int cnt = 0;
		size_t size;

		for (t = apps; t; t = s) {
			s = strchr(t, '/');
			if (s) {
				*s = '\0';
				++s;
			}
			bk_node = node;
			bk_app = t;
			p = proc_fork(exec_proc);
			if (p) ++cnt;
		}
		while(1) {
			struct ipc_data *ipc;
			proc_listen(&p, &cmd, &size, -1);
			proc_recv(p, &ipc, size);
			proc_send(TO_PARENT, cmd, ipc, size);
			//--cnt;
		}
	}

	free(apps);

	return 0;
}

static int
do_call_package(int node, const char *app)
{
	log_debug(LOG_JOB, "CallPackage(%s, %s)\n", model_get_path(node), app);

	do_execute(node, app);

	return 0;
}

static int
do_getlist(int node)
{
	char *apps;

	log_debug(LOG_JOB, "GetList(%s)\n", model_get_path(node));

	if (db_get_apps(node, &apps) != 0) {
		send_result(CMD_RESULT, NULL, 0);
	} else {
		send_result(CMD_RESULT, apps, 0);
	}
	return 0;
}

static void
job_proc(void)
{
	struct ProcChild *sender;
	char *t, *s;
	int cmd;
	size_t size;

	while (1) {
		if (1 == proc_listen(&sender, &cmd, &size, 1)) break;
	}
	ipc_recv(sender, size);

	chan = ipc_get_data();
	chan_id = ipc_get_id();

	switch (cmd) {
		case CMD_REGISTER:
			ipc_get_arg(&t, NULL);
			ipc_get_arg(&s, NULL);
			do_register(ipc_get_node(), t, s);
			break;
		case CMD_REMOVE:
			ipc_get_arg(&t, NULL);
			do_remove(t);
			break;
		case CMD_CALL:
			do_call(ipc_get_node());
			break;
		case CMD_CALL_PACKAGE:
			ipc_get_arg(&t, NULL);
			do_call_package(ipc_get_node(), t);
			break;
		case CMD_GETLIST:
			do_getlist(ipc_get_node());
			break;
	}
}

int
job_start(int cmd, char *ipc_msg, size_t ipc_size)
{
	struct ProcChild *p;

	p = proc_fork(job_proc);
	if (!p) return -1;
	if (proc_send(p, cmd, ipc_msg, ipc_size)) return -1;
	return 0;
}
