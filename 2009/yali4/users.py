# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# User management module for YALI.

import random
import shutil
import locale
import glob
import sys
import os

from string import ascii_letters, digits
from yali4.constants import consts

# a set of User instances waiting...
# we'll add these users at the last step of the installation.
pending_users = []

def resetPendingUsers():
    global pending_users
    pending_users = []

def iterHeadImages():
    left, right, images = [], [], []

    g = glob.glob(consts.user_faces_dir + "/*.png")

    for e in g: left.append(e)

    for n in range(0, 5):
        right = []
        for i in range(0, len(g)/2 + 1):
            right.append(left.pop(random.randrange(len(g) - i)))
        left.reverse()
        left = right + left

    for p in left:
        images.append(p)

    while True:
        for image in images:
            yield image

head_images = iterHeadImages()

def getUserList():
    return map(lambda x: x[0], [line.split(':') for line in open('/etc/passwd', 'r').readlines()])

class User:
    """ User class for adding or editing new users 
        to the installed system """
    def __init__(self, username = ''):
        self.username = username
        self.groups = []
        self.realname = ''
        self.passwd = ''
        self.uid = -1
        self.icon = head_images.next()
        self.noPass = False

        # KDE AutoLogin Defaults
        self.autoLoginDefaults = {"AutoLoginAgain":"false",
                                  "AutoLoginDelay":"0",
                                  "AutoLoginLocked":"false"}

        self.shadow_path = os.path.join(consts.target_dir, 'etc/shadow')
        self.passwd_path = os.path.join(consts.target_dir, 'etc/passwd')
        self.group_path  = os.path.join(consts.target_dir, 'etc/group')

    def exists(self):
        """ Check if the given user exists on system """
        if filter(lambda x: x == self.username, getUserList()):
            return True
        return False

    def usernameIsValid(self):
        """ Check if the given username is valid not """
        valid = ascii_letters + '_' + digits
        name = self.username
        if len(name) == 0 or filter(lambda x: not x in valid, name) or not name[0] in ascii_letters:
            return False
        return True

    def realnameIsValid(self):
        """ Check if the given Real Name is valid or not """
        not_allowed_chars = '\n' + ':'
        return '' == filter(lambda r: [x for x in not_allowed_chars if x == r], self.realname)

    # KDE AutoLogin
    def setAutoLogin(self,state=True):
        """ Sets the KDE's Autologin feature's state """
        confFile = os.path.join(consts.target_dir, 'etc/X11/kdm/kdmrc')

        if not os.path.exists(confFile):
            import yali4.gui.context as ctx
            ctx.debugger.log("SAL: Failed, kdmrc not found; possibly KDE is not installed !")
            return False

        import ConfigParser
        section = 'X-:0-Core'
        kdmrc = ConfigParser.ConfigParser()
        kdmrc.optionxform = str
        kdmrc.readfp(open(confFile))
        for opt in self.autoLoginDefaults.keys():
            kdmrc.set(section,opt,self.autoLoginDefaults[opt])
        # Set State
        kdmrc.set(section,'AutoLoginEnable',str(state).lower())
        # Set User
        kdmrc.set(section,'AutoLoginUser',self.username)
        kdmrc.write(open(confFile,'w'))


nickmap = {
    u"ğ": u"g",
    u"ü": u"u",
    u"ş": u"s",
    u"ı": u"i",
    u"ö": u"o",
    u"ç": u"c",
}

def nickGuess(name, nicklist):
    def convert(name):
        text = ""
        for c in name:
            if c in ascii_letters:
                text += c
            else:
                c = nickmap.get(c, None)
                if c:
                    text += c
        return text

    if name == "":
        return ""

    text = unicode(name).lower().split()

    # First guess: name
    ret = convert(text[0])
    if not ret in nicklist:
        return ret

    # Second guess: nsurname
    if len(text) > 1:
        ret = convert(text[0][0]) + convert(text[1])
        if not ret in nicklist:
            return ret

    # Third guess: namesurname
    if len(text) > 1:
        ret = convert(text[0]) + convert(text[1])
        if not ret in nicklist:
            return ret

    # Last guess: nameN
    i = 2
    while True:
        ret = convert(text[0]) + unicode(i)
        if not ret in nicklist:
            return ret
        i += 1

