/*
** Copyright (c) 2005-2007, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdlib.h>
#include <ctype.h>
#include <sys/time.h>
#include <unistd.h>
#include <dbus/dbus.h>
#include <polkit-dbus/polkit-dbus.h>

#include "policy.h"

//! Check if sender is allowed to call method
int
policy_check(const char *sender, const char *interface, const char *method, PolKitResult *result)
{
    /*!
     *
     * @sender Bus name of the sender
     * @interface Interface
     * @method Method
     * @result PK result
     * @return 0 on success, 1 on error
     */

    DBusConnection *conn;
    DBusError err;
    PolKitContext *polkit_ctx;
    PolKitCaller *polkit_clr;
    PolKitAction *polkit_act;
    PolKitError *perr;
    uid_t uid;
    int size;
    char *action, *t;

    *result = (PolKitResult) POLKIT_RESULT_NO;

    dbus_error_init(&err);

    conn = dbus_bus_get_private(DBUS_BUS_SYSTEM, &err);
    if (dbus_error_is_set(&err)) {
        log_error("Unable to open connection to query CK: %s\n", err.message);
        dbus_error_free(&err);
        return 0;
    }

    polkit_ctx = polkit_context_new();
    if (!polkit_context_init(polkit_ctx, &perr)) {
        log_error("Unable to initialize PK context: %s\n", polkit_error_get_error_message(perr));
        polkit_error_free(perr);
        return 0;
    }

    polkit_clr = polkit_caller_new_from_dbus_name(conn, sender, &err);

    polkit_caller_get_uid(polkit_clr, &uid);
    if (uid == 0) {
        *result = (PolKitResult) POLKIT_RESULT_YES;
        return 1;
    }

    // action = interface.method
    size = strlen(interface) + 1 + strlen(method) + 1;
    action = malloc(size);
    snprintf(action, size, "%s.%s\0", interface, method);

    for (t = action; *t != '\0'; t++) {
        *t = tolower(*t);
    }

    if (!polkit_action_validate_id(action)) {
        log_error("Unable to query CK, action is not valid: %s\n", action);
        free(action);
        return 0;
    }
    polkit_act = polkit_action_new();
    polkit_action_set_action_id(polkit_act, action);
    free(action);

    *result = polkit_context_is_caller_authorized(polkit_ctx, polkit_act, polkit_clr, FALSE, &perr);

    return 1;
}
