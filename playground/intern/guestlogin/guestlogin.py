#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Guest Account Module for Pardus Linux """

import os
import pwd
import sys
import subprocess
import ConfigParser

def log(text):
    sys.stdout.write(text)
    sys.stdout.flush()

def pam_sm_authenticate(pamh, flags, argv):
    """ Authentication Function.

        If username is _guest_, with this function \
        guest user will be authenticated without \
        password.
    """

    try:
        if (argv[1] == 'debug'):
            debugging = True
    except:
        debugging = False

    try:
        config = ConfigParser.ConfigParser()
        config.read('/etc/security/guestlogin.conf')
        guest_name = config.get('guest', 'guestname')
        guest_limit = config.getint('guest', 'guestlimit')
        guest_home_dir_size = config.getint('guest', 'homedirsize')
        guest_group_name = config.get('guest', 'guestgroup')

    except:
        return pamh.PAM_AUTHINFO_UNAVAIL

    if (pamh.get_user(None) == guest_name):
        users = [x.pw_name for x in pwd.getpwall()]
        i = 1
        while guest_name + str(i) in users:
            i = i + 1
            if (i > guest_limit):
                return pamh.PAM_MAXTRIES

        username = "%s%s" % (guest_name, i)
        pamh.user = username
        out = subprocess.Popen(["mktemp -td %s.XXXXXX" % username], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        home_dir = out.communicate()[0][:-1]

        if (debugging):
            log("%s has been created successful with mktemp.\n" % home_dir)

        out = subprocess.Popen(["mount -t tmpfs -o size=%sm -o mode=700 none %s" % (guest_home_dir_size, home_dir)], shell=True)

        if (debugging):
            log("%s has mounted as tmpfs\n" % home_dir)

        os.system("useradd -M -g %s %s" % (guest_group_name, username))

        if (debugging):
            log("%s has been created successfully\n" % username)

        out = subprocess.Popen(["chown %s:%s %s" % (username, guest_group_name, home_dir)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if (debugging):
            log("%s directory's owner is %s now.\n" % (home_dir, username))

        os.system("usermod -d %s %s" % (home_dir, username))

        if (debugging):
            log("%s's home directory is %s\n" % (username, home_dir))

        return pamh.PAM_SUCCESS

    else:
        return pamh.PAM_AUTHINFO_UNAVAIL

def pam_sm_setcred(pamh, flags, argv):
    """ Set Cred. """

    try:
        config = ConfigParser.ConfigParser()
        config.read('/etc/security/guestlogin.conf')
        guest_name = config.get('guest', 'guestname')
        guest_limit = config.get('guest', 'guestlimit')

    except:
        return pamh.PAM_AUTHINFO_UNAVAIL

    if (pamh.get_user(None).find(guest_name) == -1):
        return pamh.PAM_AUTHINFO_UNAVAIL

    else:
        return pamh.PAM_SUCCESS

#def pam_sm_acct_mgmt(pamh, flags, argv):
#    """ Account Management """
#    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    """ Open Session """
    return pamh.PAM_SUCCESS

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
        guest_limit = config.get('guest', 'guestlimit')

    except:
        return pamh.PAM_AUTHINFO_UNAVAIL


    if (pamh.get_user(None).find(guest_name) != -1):
        username = pamh.get_user(None)
        home_dir = os.path.expanduser("~%s" % username)
        out = subprocess.Popen(["skill -KILL -u %s" % username], shell=True)

        if (debugging):
            log("%s's all processes are killed\n" % username)

        os.system("umount %s" % home_dir)

        if (debugging):
            log("%s successfully unmounted\n" % home_dir)

        os.system("userdel -f %s" % username)

        if (debugging):
            log("user %s has been deleted\n" % username)

        os.removedirs(home_dir)

        if (debugging):
            log("folder %s has been deleted\n" % home_dir)

    return pamh.PAM_SUCCESS

#def pam_sm_chauthtok(pamh, flags, argv):
#    """ Chauthtok """
#    return pamh.PAM_SUCCESS
