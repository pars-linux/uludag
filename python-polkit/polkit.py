#-*- coding: utf-8 -*-
"""
module for querying system-wide policy

 *
 * PolicyKit by David Zeuthen, <david@fubar.dk>
 * Python Bindings by Bahadır Kandemir <bahadir@pardus.org.tr>
 *                    Harald Hoyer <harald@redhat.com>
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

"""

import _polkit

from _polkit import (
    SCOPE_ONE_SHOT,
    SCOPE_PROCESS,
    SCOPE_SESSION,
    SCOPE_ALWAYS,
    TYPE_UID,
    DB_CAPABILITY_CAN_OBTAIN,
    CONSTRAINT_TYPE_REQUIRE_LOCAL,
    CONSTRAINT_TYPE_REQUIRE_ACTIVE,
    CONSTRAINT_TYPE_REQUIRE_EXE,
    CONSTRAINT_TYPE_REQUIRE_SELINUX_CONTEXT,
    error
    )

def action_list():
    """
    Lists all action_ids

    returns :
        A list() of action_ids
    """
    return [x["action_id"] for x in _polkit.action_list()]

def action_info(action_id):
    """
    Gives details about action_id

    action_id :
         Action id

    returns :
        A dict() of details about action_id
    """
    for act in _polkit.action_list():
        if act["action_id"] == action_id:
            return act
    return {}

def auth_list_uid(uid):
    """
    Lists all authorizations given to uid.

    uid :
        User ID

    returns :
        A list() of authorizations
    """
    return _polkit.auth_list_uid(uid)

def auth_list_all():
    """
    Lists all authorizations given.

    returns :
         A list() of authorizations
    """
    return _polkit.auth_list_all()

def auth_add(action_id, auth_type, uid, pid=None):
    """
    action_id :
        Action ID

    auth_type :
        Authorization type.
        Should be one of SCOPE_ONE_SHOT, SCOPE_PROCESS,
        SCOPE_SESSION or SCOPE_ALWAYS

    uid :
        User ID

    pid :
        Process ID of process to grant authorization to.
        Normally one wants to pass result of os.getpid().
    """
    if auth_type in (SCOPE_ONE_SHOT, SCOPE_PROCESS):
        if not pid:
            raise error, "Process ID required"
        return _polkit.auth_add(action_id, auth_type, uid, pid)
    else:
        return _polkit.auth_add(action_id, auth_type, uid)

def auth_revoke_all(uid):
    """
    Removes all authorizations of UID from the authorization database.

    uid :
        User ID
    """
    return _polkit.auth_revoke_all(uid)

def auth_revoke(uid, action_id):
    """
    Removes authorization of UID to perform action_id from the
    authorization database.

    uid :
        User ID

    action_id :
        Action ID
    """
    return _polkit.auth_revoke(uid, action_id)

def auth_block(uid, action_id):
    """
    Grants a negative authorization to a user for a specific action

    A negative authorization is normally used to block users that
    would normally be authorized from an implicit authorization.

    uid :
        User ID

    action_id :
        Action ID
    """
    return _polkit.auth_block(uid, action_id)
