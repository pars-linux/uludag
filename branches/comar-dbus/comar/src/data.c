/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
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
#include <sys/file.h>
#include <unistd.h>

#include "cfg.h"
#include "log.h"
#include "utility.h"

//! Database init function
int
db_init(void)
{
    /*!
    Checks comar db directory and db format, creates if not exists.
    Also checks code/lock file
    @return Returns 0 on success, \n Returns -1 on error, \n Returns -2 if db type is not app or model \n
    Returns -3 if code/lock name is not set ( either theres something wrong with data dir,
    or memory allocation error )
    */

    struct stat fs;
    size_t size;

    if (stat(cfg_data_dir, &fs) != 0) {
        if (0 != mkdir(cfg_data_dir, S_IRWXU)) {
            log_error("Cannot create data dir '%s'\n", cfg_data_dir);
            return -1;
        }
    } else {
        // FIXME: check perms and owner
    }

    size = strlen(cfg_data_dir) + 6;
    char *code_dir = malloc(size);
    if (!code_dir) return -3;
    snprintf(code_dir, size, "%s/code\0", cfg_data_dir);
    if (stat(code_dir, &fs) != 0) {
        if (0 != mkdir(code_dir, S_IRWXU)) {
            log_error("Cannot create code dir '%s'\n", code_dir);
            return -1;
        }
    }

    // FIXME: check and recover db files
    return 0;
}

//! Structure that carries databases
struct databases {
    DB_ENV *env;
    DB *app;
};

#define APP_DB 1

//! Open a database
static int
open_database(DB_ENV *env, DB **dbp, const char *name)
{
    /*!
    Creates a DB structure that is the handle for a Berkeley DB database
    and opens it as a standalone, sorted - balanced tree structured DB.
    env is the environment, and dbp is db type ( model, app, code or profile )
    with 'name' file name
    @return Returns -1 if can not create database \n
    Returns -2 if can not open database \n
    Returns 0 otherwise \n
    */

    int e;
    DB *db;

    e = db_create(dbp, env, 0);
    if (e) {
        log_error("Cannot create database, %s\n", db_strerror(e));
        *dbp = NULL;
        return -1;
    }
    db = *dbp;
    e = db->open(db, NULL, name, NULL, DB_BTREE, DB_CREATE, 0);
    if (e) {
        log_error("Cannot open database, %s\n", db_strerror(e));
        return -2;
    }
    return 0;
}

//! Create and open DB_ENV
static int
open_env(struct databases *db, int which)
{
    /*!
    Creates DB_ENV structure with db_home directory set to
    comar db dir. After creating enviroment, opens database
    with created env and specified DB type (type is 'which' in this case)
    @return Returns -1 if can not create database environment \n
    Returns -2 if can not open database environment. \n
    Returns -3 if which is a model db, and db could not be created or opened \n
    Returns -4 if which is a app db, and db could not be created or opened \n
    Returns 0 otherwise
    */

    int e;

    memset(db, 0, sizeof(struct databases));
    e = db_env_create(&db->env, 0);
    if (e) {
        log_error("Cannot create database environment, %s\n", db_strerror(e));
        db->env = NULL;
        return -1;
    }
    e = db->env->open(db->env,
        cfg_data_dir,
        DB_INIT_LOCK |DB_INIT_MPOOL | DB_INIT_LOG | DB_INIT_TXN | DB_CREATE,
        0
    );
    if (e) {
        log_error("Cannot open database environment, %s\n", db_strerror(e));
        return -2;
    }

    if (which & APP_DB) {
        if (open_database(db->env, &db->app, "app.db")) return -4;
    }

    return 0;
}

//! Close created databases and environment of db
static void
close_env(struct databases *db)
{
    if (db->app) db->app->close(db->app, 0);
    db->env->close(db->env, 0);
}

//! Fetches and returns the record called 'name' from database 'db'
static char *
get_data(DB *db, const char *name, size_t *sizep, int *errorp)
{
    /*! \param errorp Error number returned */    
    DBT pair[2];

    memset(&pair[0], 0, sizeof(DBT) * 2);
    pair[0].data = (char *) name;
    pair[0].size = strlen(name);
    pair[1].flags = DB_DBT_MALLOC;

    *errorp = db->get(db, NULL, &pair[0], &pair[1], 0);
    if (*errorp == 0) {
        if (sizep) *sizep = pair[1].size;
        return pair[1].data;
    }
    return NULL;
}

//! Put data to a database
static int
put_data(DB *db, const char *name, const char *data, size_t size)
{
    /*!
    Puts "name and 'size of name'" as first pair, and
    "data and size" as second pair to DB. \n
    DBT is key/data pair structure of berkeley db
    @return This function can return a non-zero error for errors specified for \n
    other Berkeley DB and C library or system functions. or DB_RUNRECOVERY
    */

    DBT pair[2];

    memset(&pair[0], 0, sizeof(DBT) * 2);
    pair[0].data = (char *) name;
    pair[0].size = strlen(name);
    pair[1].data = (char *) data;
    pair[1].size = size;
    return db->put(db, NULL, &pair[0], &pair[1], 0);
}

//! Delete name from database
static int
del_data(DB *db, const char *name)
{
    /*! @return Returns error number \sa put_data */    
    DBT key;

    memset(&key, 0, sizeof(DBT));
    key.data = (char *) name;
    key.size = strlen(name);
    return db->del(db, NULL, &key, 0);
}

static int
have_key(DB *db, const char *key)
{
    char *old, *t, *s;
    int e;

    old = get_data(db, key, NULL, &e);

    return old != NULL;
}

static int
key_have_item(DB *db, const char *key, const char *item)
{
    char *old, *t, *s;
    int e;

    old = get_data(db, key, NULL, &e);

    t = strdup(old);
    if (!t) return -1;
    for (; t; t = s) {
        s = strchr(t, '|');
        if (s) {
            *s = '\0';
            ++s;
        }
        if (strcmp(t, item) == 0) {
            return 1;
        }
    }

    return 0;
}

//! Append an item to db
static int
append_item(DB *db, const char *key, const char *item)
{
    /*!
    If theres no such record, put it in db
    @return If item is already in db returns -1 \n
    Returns 0 normally
    */

    char *old;
    char *data;
    size_t len;
    int e;

    old = get_data(db, key, NULL, &e);
    if (e && e != DB_NOTFOUND) return -1;

    if (!old || old[0] == '\0') {
        // no old record
        e = put_data(db, key, item, strlen(item) + 1);
        if (e) return -1;
        return 0;
    }

    if (key_have_item(db, key, item)) return 0;

    // append to old records
    len = strlen(old) + 1 + strlen(item) + 1;
    data = malloc(len);
    if (!data) return -1;
    snprintf(data, len, "%s|%s", old, item);

    e = put_data(db, key, data, strlen(data) + 1);
    if (e) return -1;

    return 0;
}

int
db_register_model(char *app, char *model)
{
    struct databases db;
    int e, ret = -1;

    if (open_env(&db, APP_DB)) goto out;

    e = append_item(db.app, app, model);
    e = append_item(db.app, "__apps__", app);

out:
    close_env(&db);
    return ret;
}

int
db_remove_app(char *app)
{
    struct databases db;
    char *list;
    int e, ret = -1;
    int no;

    if (open_env(&db, APP_DB)) goto out;

    del_data(db.app, app);

    list = get_data(db.app, "__apps__", NULL, &e);

    if (list) {
        char *k;
        int sa = strlen(app);
        k = strstr(list, app);
        if (k) {
            if (k[sa] == '|') ++sa;
            memmove(k, k + sa, strlen(k) - sa + 1);
            sa = strlen(list);
            if (sa > 0) {
                if (list[sa-1] == '|') list[sa-1] = '\0';
            }
            e = put_data(db.app, "__apps__", list, strlen(list) + 1);
            if (e) goto out;
        }
    }
    free(list);
out:
    close_env(&db);
    return ret;
}


int
db_remove_model(char *app, char *model)
{
    struct databases db;
    char *list;
    int e, ret = -1;
    int no;

    if (open_env(&db, APP_DB)) goto out;

    list = get_data(db.app, app, NULL, &e);

    if (list) {
        char *k;
        int sa = strlen(model);
        k = strstr(list, model);
        if (k) {
            if (k[sa] == '|') ++sa;
            memmove(k, k + sa, strlen(k) - sa + 1);
            sa = strlen(list);
            if (sa > 0) {
                if (list[sa-1] == '|') list[sa-1] = '\0';
            }
            e = put_data(db.app, app, list, strlen(list) + 1);
            if (e) goto out;
        }
    }
    free(list);
out:
    close_env(&db);
    return ret;
}

int
db_get_apps(char **bufferp)
{
    struct databases db;
    int e, ret = -1;

    if (open_env(&db, APP_DB)) goto out;

    *bufferp = get_data(db.app, "__apps__", NULL, &e);
    if (e) goto out; // error

    ret = 0;
out:
    close_env(&db);
    return ret;
}

int
db_get_models(char *app, char **bufferp)
{
    /*!
    Fetches data of node 'node_no' and writes it to bufferp
    @return Returns -1 on error, 0 otherwise
    */
    struct databases db;
    int e, ret = -1;

    if (open_env(&db, APP_DB)) goto out;

    *bufferp = get_data(db.app, app, NULL, &e);
    if (e) goto out; // error

    ret = 0;
out:
    close_env(&db);
    return ret;
}

int
db_check_app(char *app)
{
    if (!check_app_name(app)) {
        return 0;
    }

    struct databases db;
    int e, ret;

    if (open_env(&db, APP_DB)) goto out;

    ret = have_key(db.app, app);
out:
    close_env(&db);
    return ret;
}

int
db_check_model(char *app, char *model)
{
    if (!check_app_name(app) || !check_model_name(model)) {
        return 0;
    }

    struct databases db;
    int e, ret;

    if (open_env(&db, APP_DB)) goto out;

    ret = have_key(db.app, app);
    if (!ret) goto out;

    ret = key_have_item(db.app, app, model);
out:
    close_env(&db);
    return ret;
}
