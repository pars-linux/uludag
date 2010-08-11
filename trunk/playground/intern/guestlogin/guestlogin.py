#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Guest Account Module for Pardus Linux """

import os
import pwd
import subprocess

def pam_sm_authenticate(pamh, flags, argv):
    """ Authentication Function.

        If username is _guest_, with this function \
        guest user will be authenticated without \
        password.
    """
    if (pamh.get_user(None) == 'guest'):
        users = [x.pw_name for x in pwd.getpwall()]
        i = 1
        while "guest" + str(i) in users:
            i = i + 1
        username = "guest%s" % i
        pamh.user = username
        procOutput = subprocess.Popen(["mktemp -td %s.XXXXXX" % username], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        homeDir = procOutput.communicate()[0][:-1]
        os.system("mount -t tmpfs -o mode=700 none %s" % homeDir)
        os.system("useradd -M %s  2>> /var/log/guestacc.log" % username)
        os.system("chown %s:%s %s" % (username, username, homeDir))
        os.system("usermod -d %s %s" % (homeDir, username))
        os.system("echo 'Added %s user as guest' >> /var/log/guestacc.log" % username)
        return pamh.PAM_SUCCESS
    else:
        return pamh.PAM_AUTHINFO_UNAVAIL

def pam_sm_setcred(pamh, flags, argv):
    """ Set Cred. """
    if (pamh.get_user(None).find('guest') == -1):
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
    if (pamh.get_user(None).find('guest') != -1):
        username = pamh.get_user(None)
        homeDir = os.path.expanduser("~%s" % username)
        os.system("skill -KILL -u %s 2>> /var/log/guestacc.log" % username)
        os.system("umount %s" % homeDir)
        os.system("userdel -f %s 2>> /var/log/guestacc.log" % username)
        os.system("groupdel %s 2>> /var/log/guestacc.log" % username)
        os.removedirs(homeDir)
        os.system("echo 'Deleted %s user as guest \n' >> /var/log/guestacc.log" % username)
    return pamh.PAM_SUCCESS

#def pam_sm_chauthtok(pamh, flags, argv):
#    """ Chauthtok """
#    return pamh.PAM_SUCCESS
