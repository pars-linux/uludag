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
    return _polkit.action_list()

def action_info(action_id):
    """
    Gives details about action_id

    action_id :
         Action id

    returns :
        A dict() of details about action_id
    """
    return _polkit.action_info(action_id)

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

def check_auth(pid, *args):
    """
    This function is similar to check_authv(),
    but takes the action_ids as a plain parameter list.
    """
    return check_authv(pid, args)

def check_authv(pid, action_ids):
    """
    A simple convenience function to check whether a given
    process is authorized for a number of actions.

    This is useful for programs that just wants to check whether
    they should carry out some action. Note that the user identity
    used for the purpose of checking authorizations is the Real
    one compared to the e.g. Effective one (e.g. getuid(), getgid()
    is used instead of e.g. geteuid(), getegid()). This is typically
    what one wants in a setuid root program if the setuid root program
    is designed to do work on behalf of the unprivileged user who
    invoked it (for example, the PulseAudio sound server is setuid
    root only so it can become a real time process; after that it
    drops all privileges).

    It varies whether one wants to pass getpid() or getppid() as
    the process id to this function. For example, in the PulseAudio
    case it is the right thing to pass getpid(). However, in a setup
    where the process is a privileged helper, one wants to pass the
    process id of the parent. Beware though, if the parent dies, getppid()
    will return 1 (the process id of /sbin/init) which is almost
    certainly guaranteed to be privileged as it is running as uid 0.

    Note that this function will open a connection to the system
    message bus and query ConsoleKit for details. In addition, it
    will load PolicyKit specific files and spawn privileged helpers
    if necessary. As such, there is a bit of IPC, context switching,
    syscall overhead and I/O involved in using this function.

    pid :
        Process ID of process to grant authorization to. 
        Normally one wants to pass result of os.getpid().

    action_ids :
         A list or tuple of action id strings

    returns :
         A set() of action_ids, where authentication succeeded
    """
    ret = _polkit.check_authv(pid, action_ids)
    auth = set()
    if (type(ret) is not long):
        raise error
    for i, action in enumerate(action_ids):
        if (ret & (1<<i)):
            auth.add(action)
    return auth

def auth_obtain(action_id, xid, pid):
    """
    Convenience function to prompt the user to authenticate to
    gain an authorization for the given action. First, an attempt
    to reach an Authentication Agent on the session message bus is made.
    If that doesn't work and stdout/stdin are both tty's,
    polkit-auth(1) is invoked.

    action_id :
        The action_id string for the PolKitAction to make the
        user authenticate for.

    xid :
        X11 window ID for the window that the dialog will be transient for.
        If there is no window, pass 0.

    pid :
        Process ID of process to grant authorization to.
        Normally one wants to pass result of os.getpid().
    """
    if action_id in check_auth(pid, action_id):
        return True

    ret = _polkit.auth_obtain(action_id, xid, pid)
    if (ret is list):
        raise error, "%s: %s" % ret
    return ret

