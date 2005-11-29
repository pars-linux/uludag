/*
** Copyright (c) 2005, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <db.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>

#include "cfg.h"
#include "data.h"
#include "model.h"
#include "log.h"
#include "process.h"
#include "ipc.h"

static DB_ENV *my_env;
static int nr_open_dbs;

static void
fix_old_db(void)
{
	// FIXME: delete old db format, remove this code before release
	// beware: quickly and badly written temporary code :)
	FILE *f;
	struct stat fs;
	char *t;
	t = malloc(strlen(cfg_data_dir) + 7 + 1);
	sprintf(t, "%s%s", cfg_data_dir, "/format");
	if (stat(t, &fs) != 0) {
		free(t);
		t = malloc(strlen(cfg_data_dir) + 9 + 1);
		sprintf(t, "rm -rf %s/*", cfg_data_dir);
		system(t);
		free(t);
		t = malloc(strlen(cfg_data_dir) + 7 + 1);
		sprintf(t, "%s%s", cfg_data_dir, "/format");
		f = fopen(t, "w");
		fwrite("1", 1, 1, f);
		fclose(f);
	}
	free(t);
}

int
db_init(void)
{
	struct stat fs;

	if (stat(cfg_data_dir, &fs) != 0) {
		if (0 != mkdir(cfg_data_dir, S_IRWXU)) {
			log_error("Cannot create data dir '%s'\n", cfg_data_dir);
			return -1;
		}
	} else {
		// FIXME: check perms and owner
	}
	fix_old_db();
	// FIXME: check and recover db files
	return 0;
}

static DB *
open_db(const char *name)
{
	DB *db;
	int e;

	// join the environment if necessary
	if (!my_env) {
		e  = db_env_create(&my_env, 0);
		if (e) {
			log_error("Cannot create env, %s\n", db_strerror(e));
			return NULL;
		}
		e = my_env->open(my_env, cfg_data_dir, DB_INIT_LOCK | DB_INIT_MPOOL
				| DB_INIT_LOG | DB_INIT_TXN | DB_CREATE, 0);
		if (e) {
			log_error("Cannot open env, %s\n", db_strerror(e));
			my_env->close(my_env, 0);
			my_env = NULL;
			return NULL;
		}
	}

	// open db
	e = db_create(&db, my_env, 0);
	if (e) {
		log_error("Cannot create db, %s\n", db_strerror(e));
		if (0 == nr_open_dbs) {
			my_env->close(my_env, 0);
			my_env = NULL;
		}
		return NULL;
	}
	e = db->open(db, NULL, name, NULL, DB_BTREE, DB_CREATE, 0);
	if (e) {
		log_error("Cannot open db, %s\n", db_strerror(e));
		db->close(db, 0);
		if (0 == nr_open_dbs) {
			my_env->close(my_env, 0);
			my_env = NULL;
		}
		return NULL;
	}

	nr_open_dbs++;
	return db;
}

static void
close_db(DB *db)
{
	db->close(db, 0);
	--nr_open_dbs;
	if (0 == nr_open_dbs) {
		my_env->close(my_env, 0);
		my_env = NULL;
	}
}

static char *
get_data(DB *db, const char *name, int rw_lock, int *errorp)
{
	DBT pair[2];

	memset(&pair[0], 0, sizeof(DBT) * 2);
	pair[0].data = (char *) name;
	pair[0].size = strlen(name);
	pair[1].flags = DB_DBT_MALLOC;

	*errorp = db->get(db, NULL, &pair[0], &pair[1], 0);
	if (*errorp == 0) return pair[1].data;
	return NULL;
}

static int
put_data(DB *db, const char *name, const char *data, size_t size)
{
	DBT pair[2];

	memset(&pair[0], 0, sizeof(DBT) * 2);
	pair[0].data = (char *) name;
	pair[0].size = strlen(name);
	pair[1].data = (char *) data;
	pair[1].size = size;
	return db->put(db, NULL, &pair[0], &pair[1], 0);
}

static int
del_data(DB *db, const char *name)
{
	DBT key;

	memset(&key, 0, sizeof(DBT));
	key.data = (char *) name;
	key.size = strlen(name);
	return db->del(db, NULL, &key, 0);
}

static char *
make_key(int node_no, const char *app)
{
	static char *key = NULL;
	static size_t max = 0;
	const char *path;
	size_t size;

	path = model_get_path(node_no);
	size = strlen(path) + 1;
	if (app) size += strlen(app) + 1;

	if (size > max) {
		key = realloc(key, size);
		max = size;
	}

	if (app)
		sprintf(key, "%s/%s", path, app);
	else
		sprintf(key, "%s", path);

	return key;
}

static char *
make_list(char *old, const char *item)
{
	// FIXME: lame
	char *ret;

	if (strcmp(old, "") != 0) {
		ret = malloc(strlen(old) + 1 + strlen(item) + 1);
		sprintf(ret, "%s/%s", old, item);
	} else {
		ret = malloc(strlen(item) + 1);
		sprintf(ret, "%s", item);
	}
	return ret;
}

int
db_put_script(int node_no, const char *app, const char *buffer, size_t size)
{
	DB *code_db = NULL, *model_db = NULL, *app_db = NULL;
	char *old;
	char *t;
	int e, ret = -1;

	app_db = open_db("app.db");
	if (!app_db) goto out;
	model_db = open_db("model.db");
	if (!model_db) goto out;
	code_db = open_db("code.db");
	if (!code_db) goto out;

	old = get_data(app_db, app, 0, &e);
	if (!old) {
		if (e == DB_NOTFOUND)
			old = "";
		else
			goto out;
	}

	t = make_key(node_no, NULL);
	if (strstr(old, t) == NULL) {
		t = make_list(old, t);
		e = put_data(app_db, app, t, strlen(t) + 1);
		free(t);
		if (e) goto out;
	}
	if (strcmp(old, "") != 0) free(old);

	e = put_data(code_db, make_key(node_no, app), buffer, size);
	if (e) goto out;

	old = get_data(model_db, make_key(node_no, NULL), 0, &e);
	if (!old) {
		if (e == DB_NOTFOUND)
			old = "";
		else
			goto out;
	}

	if (strstr(old, app) == NULL) {
		t = make_list(old, app);
		e = put_data(model_db, make_key(node_no, NULL), t, strlen(t) + 1);
		free(t);
		if (e) goto out;
	}
	if (strcmp(old, "") != 0) free(old);

	ret = 0;
out:
	if (code_db) close_db(code_db);
	if (model_db) close_db(model_db);
	if (app_db) close_db(app_db);
	return ret;
}

int
db_del_app(const char *app)
{
	DB *code_db = NULL, *model_db = NULL, *app_db = NULL;
	char *list, *list2, *t, *s;
	int e, ret = -1;

	app_db = open_db("app.db");
	if (!app_db) goto out;
	model_db = open_db("model.db");
	if (!model_db) goto out;
	code_db = open_db("code.db");
	if (!code_db) goto out;

	list = get_data(app_db, app, 0, &e);
	if (!list) goto out;

	for (t = list; t; t = s) {
		s = strchr(t, '/');
		if (s) {
			*s = '\0';
			++s;
		}

		list2 = get_data(model_db, t, 0, &e);
		if (!list2) goto out;
		{
			char *k;
			int sa = strlen(app);
			k = strstr(list2, app);
			if (k) {
				if (k[sa] == '/') ++sa;
				memmove(k, k + sa, strlen(k) - sa + 1);
				sa = strlen(list2);
				if (sa > 0) {
					if (list2[sa-1] == '/')
						list2[sa-1] = '\0';
				}
				e = put_data(model_db, t, list2, strlen(list2) + 1);
				if (e) goto out;
			}
		}
		free(list2);

		e = del_data(code_db, make_key(atoi(t), app));
		if (e) goto out;
	}

	free(list);

	e = del_data(app_db, app);
	if (e) goto out;

	ret = 0;
out:
	if (code_db) close_db(code_db);
	if (model_db) close_db(model_db);
	if (app_db) close_db(app_db);
	return ret;
}

int
db_get_apps(int node_no, char **bufferp)
{
	DB *model_db = NULL;
	int e, ret = -1;

	model_db = open_db("model.db");
	if (!model_db) goto out;

	*bufferp = get_data(model_db, make_key(node_no, NULL), 0, &e);
	if (e) goto out;

	ret = 0;
out:
	if (model_db) close_db(model_db);
	return ret;
}

int
db_get_code(int node_no, const char *app, char **bufferp, size_t *sizep)
{
	DB *code_db;
	DBT key, data;
	int e, ret = -1;

	code_db = open_db("code.db");
	if (!code_db) goto out;

	memset(&key, 0, sizeof(DBT));
	memset(&data, 0, sizeof(DBT));
	key.data = (char *) make_key(node_no, app);
	key.size = strlen(key.data);
	data.flags = DB_DBT_MALLOC;

	e = code_db->get(code_db, NULL, &key, &data, 0);
	if (e) goto out;

	*bufferp = data.data;
	*sizep = data.size;

	ret = 0;
out:
	close_db(code_db);
	return ret;
}

static char *
make_pkey(char *old, const char *part, char sep)
{
	char *ret;

	if (old) {
		ret = malloc(strlen(old) + 1 + strlen(part) + 1);
		strcpy(ret, old);
		ret[strlen(old)] = sep;
		strcpy(ret + 1 + strlen(old), part);
		free(old);
	} else {
		ret = strdup(part);
	}
	return ret;
}

int
db_put_profile(int node_no, const char *app, const char *args, size_t args_size)
{
	DB *profile_db = NULL;
	int e, ret = -1;
	char *key;

	profile_db = open_db("profile.db");
	if (!profile_db) goto out;

	key = make_pkey(NULL, model_get_path(node_no), '/');
	if (app) key = make_pkey(key, app, '/');

	ipc_use_data(args, args_size);
	while (1) {
		char *t;
		size_t sz;
		if (ipc_get_arg(&t, &sz) == 0) break;
		if (model_is_instance(node_no, t)) {
			key = make_pkey(key, t, '/');
			ipc_get_arg(&t, &sz);
			key = make_pkey(key, t, '=');
		} else {
			ipc_get_arg(&t, &sz);
		}
	}

	e = put_data(profile_db, key, args, args_size);
	free(key);
	if (e) goto out;

	ret = 0;
out:
	if (profile_db) close_db(profile_db);
	return ret;
}

int
db_get_profile(int node_no, const char *app, char **argsp, size_t *args_sizep)
{
	return -1;
}

int
db_get_instances(int node_no, const char *app, const char *key, void (*func)(char *str, size_t size))
{
	DB *profile_db = NULL;
	DBC *cursor = NULL;
	DBT pair[2];
	int e, ret = -1;
	char *match;

	memset(&pair[0], 0, sizeof(DBT) * 2);

	profile_db = open_db("profile.db");
	if (!profile_db) goto out;

	profile_db->cursor(profile_db, NULL, &cursor, 0);

	// FIXME: multiple instance keys?
	match = make_pkey(NULL, model_get_path(node_no), '/');
	if (app) match = make_pkey(match, app, '/');
	if (key) {
		match = make_pkey(match, key, '/');
		match = make_pkey(match, "", '=');
	} else {
		match = make_pkey(match, "", '/');
	}

	while ((e = cursor->c_get(cursor, &pair[0], &pair[1], DB_NEXT)) == 0) {
//printf("match [%s] pair [%.*s]\n",match,pair[0].size,pair[0].data);
		if (strncmp(match, pair[0].data, strlen(match)) == 0)
			func(((char *) pair[0].data) + strlen(match), pair[0].size - strlen(match));
	}
	if (e != DB_NOTFOUND) {
		goto out;
	}

	ret = 0;
out:
	if (cursor) cursor->c_close(cursor);
	if (profile_db) close_db(profile_db);
	return ret;
}

int
db_dump_profile(void)
{
	DB *profile_db = NULL;
	DBC *cursor = NULL;
	DBT pair[2];
	int e, ret = -1;

	memset(&pair[0], 0, sizeof(DBT) * 2);

	profile_db = open_db("profile.db");
	if (!profile_db) goto out;

	profile_db->cursor(profile_db, NULL, &cursor, 0);

	while ((e = cursor->c_get(cursor, &pair[0], &pair[1], DB_NEXT)) == 0) {
		printf("key [%.*s]\n", pair[0].size, (char *) pair[0].data);
	}
	if (e != DB_NOTFOUND) {
		goto out;
	}

	ret = 0;
out:
	if (cursor) cursor->c_close(cursor);
	if (profile_db) close_db(profile_db);
	return ret;
}
