#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Guest Account Module for Pardus Linux """

import os
import pwd

def pam_sm_authenticate(pamh, flags, argv):
    """ Authentication Function.

        If username is _guest_, with this function \
        guest user will be authenticated without \
        password.
    """
    if (pamh.get_user(None) == 'guest'):
        print "Guest user login detected,\
 please wait while your account being created...\n"
        users = [x.pw_name for x in pwd.getpwall()]
        i = 1
        while "guest" + str(i) in users:
            i = i + 1
        username = "guest%s" % i
        os.system("useradd %s -d /home/%s 2>> /var/log/guestacc.log" % (username, username))
        pamh.user = username
        os.system("echo 'Added %s user as guest' >> /var/log/guestacc.log" % username)
        print "Your temporary username set as %s and your home \
folder is /home/%s, Have Fun!" % (username, username)
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
destroy it but too dangerous"""
    username = pamh.get_user(None)
    if (username.find('guest') != -1):
        os.system("skill -KILL -u %s 2>> /var/log/guestacc.log" % username)
        os.system("userdel -f %s 2>> /var/log/guestacc.log" % username)
        os.system("groupdel %s 2>> /var/log/guestacc.log" % username)
        os.system("rm -rf /home/%s 2>> /var/log/guestacc.log" % username)
        os.system("echo 'Deleted %s user as guest \n' >> /var/log/guestacc.log" % username)
    return pamh.PAM_SUCCESS

#def pam_sm_chauthtok(pamh, flags, argv):
#    """ Chauthtok """
#    return pamh.PAM_SUCCESS
