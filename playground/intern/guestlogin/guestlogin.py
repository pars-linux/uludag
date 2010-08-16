#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Guest Account Module for Pardus Linux """

import os
import pwd
import sys
import tempfile
import subprocess
import ConfigParser

def log(text):
    """ Log Function. """

    sys.stdout.write(text)
    sys.stdout.flush()

def auth_return(pamh, level, home_dir=""):
    """ Return Function. """

    if level >= 2:
        shutil.rmtree(home_dir)

    if level >= 3:
        out = subprocess.Popen(["umount %s" % home_dir], shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out.wait()

    if level == 0:
        return pamh.PAM_SUCCESS

    if level == -1:
        return pamh.PAM_AUTHINFO_UNAVAIL

    if level == -2:
        return pamh.PAM_MAXTRIES

    if level == 1 or (level > 2):
        return pamh.PAM_AUTH_ERR

def pam_sm_authenticate(pamh, flags, argv):
    """ Authentication Function.

        If username is _guest_, with this function \
        guest user will be authenticated without \
        password.
    """

    try:
        debugging = (argv[1] == 'debug')
    except IndexError:
        debugging = False

    try:
        config = ConfigParser.ConfigParser()
        config.read('/etc/security/guestlogin.conf')
        guest_name = config.get('guest', 'guestname')
        guest_limit = config.getint('guest', 'guestlimit')
        guest_home_dir_size = config.getint('guest', 'homedirsize')
        guest_group_name = config.get('guest', 'guestgroup')

    except:
        return auth_return(pamh, -1)

    if pamh.get_user(None) == guest_name:
        users = [x.pw_name for x in pwd.getpwall()]
        i = 1
        while "%s%s" % (guest_name, i) in users:
            i = i + 1
            if (i > guest_limit):
                return auth_return(pamh, -2)

        username = "%s%s" % (guest_name, i)
        pamh.user = username
        try:
            home_dir = tempfile.mkdtemp(prefix='%s.' % username)
        except IOError:
            # No usable temporary directory name found
            return auth_return(pamh, -2)

        if debugging:
            log("%s has been created successful with mktemp.\n" % home_dir)

        out = subprocess.Popen(["mount -t tmpfs -o size=%sm -o mode=711 \
                none %s" % (guest_home_dir_size, home_dir)], shell=True)
        if out.wait() != 0:
            return auth_return(pamh, -2)

        if not (os.path.ismount(home_dir)):
            return auth_return(pamh, 2, home_dir)

        if debugging:
            log("%s has mounted as tmpfs\n" % home_dir)

        out = subprocess.Popen(["useradd -m -d %s/home -g %s %s" % (home_dir, \
                guest_group_name, username)], shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if out.wait() != 0:
            return auth_return(pamh, -2)

        try:
            pwd.getpwnam(username)

        except:
            return auth_return(pamh, 3, home_dir)

        if debugging:
            log("%s has been created successfully\n" % username)

        return auth_return(pamh, 0)

    else:
        return auth_return(pamh, -1)

def pam_sm_setcred(pamh, flags, argv):
    """ Set Cred. """

    try:
        config = ConfigParser.ConfigParser()
        config.read('/etc/security/guestlogin.conf')
        guest_name = config.get('guest', 'guestname')

    except:
        return auth_return(pamh, -1)

    if pamh.get_user(None).find(guest_name) == -1:
        return auth_return(pamh, -1)

    else:
        return auth_return(pamh, 0)

def pam_sm_open_session(pamh, flags, argv):
    """ Open Session """
    return auth_return(pamh, 0)

def pam_sm_close_session(pamh, flags, argv):
    """ Close Session, if user is guest \
destroy it but it seems quite dangerous"""

    try:
        if (argv[1] == 'debug'):
            debugging = True
    except:
        debugging = False

    try:
        config = ConfigParser.ConfigParser()
        config.read('/etc/security/guestlogin.conf')
        guest_name = config.get('guest', 'guestname')

    except:
        return auth_return(pamh, -1)

    if pamh.get_user(None).find(guest_name) != -1:
        username = pamh.get_user(None)
        _home_dir = pwd.getpwnam(username).pw_dir
        home_dir = _home_dir[0:_home_dir.rfind('/')+1]
        out = subprocess.Popen(["skill -KILL -u %s" % username], shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out.wait()

        if debugging:
            log("%s's all processes are killed\n" % username)


        out = subprocess.Popen(["umount %s" % home_dir], shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out.wait()

        if debugging:
            log("%s successfully unmounted\n" % home_dir)

        out = subprocess.Popen(["userdel -f %s" % username], shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out.wait()

        if debugging:
            log("user %s has been deleted\n" % username)

        shutil.rmtree(home_dir)

        if debugging:
            log("folder %s has been deleted\n" % home_dir)

    return auth_return(pamh, 0)
