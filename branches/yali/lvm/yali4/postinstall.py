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

import os
import grp
import time
import dbus
import yali4
import shutil

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4.gui.context as ctx
from yali4.constants import consts
from yali4.gui.installdata import *

def cp(s, d):
    src = os.path.join(consts.target_dir, s)
    dst = os.path.join(consts.target_dir, d)
    ctx.debugger.log("Copying from '%s' to '%s'" % (src,dst))
    shutil.copyfile(src, dst)

def touch(f, m=0644):
    f = os.path.join(consts.target_dir, f)
    open(f, "w", m).close()

def chgrp(f, group):
    f = os.path.join(consts.target_dir, f)
    gid = int(grp.getgrnam(group)[2])
    os.chown(f, 0, gid)

# necessary things after a full install

def initbaselayout():
    # create /etc/hosts
    cp("usr/share/baselayout/hosts", "etc/hosts")

    # create /etc/ld.so.conf
    cp("usr/share/baselayout/ld.so.conf", "etc/ld.so.conf")

    # /etc/passwd, /etc/shadow, /etc/group
    cp("usr/share/baselayout/passwd", "etc/passwd")
    cp("usr/share/baselayout/shadow", "etc/shadow")
    os.chmod(os.path.join(consts.target_dir, "etc/shadow"), 0600)
    cp("usr/share/baselayout/group", "etc/group")

    # create empty log file
    touch("var/log/lastlog")

    touch("var/run/utmp", 0664)
    chgrp("var/run/utmp", "utmp")

    touch("var/log/wtmp", 0664)
    chgrp("var/log/wtmp", "utmp")

    # create needed device nodes
    os.system("/bin/mknod %s/dev/console c 5 1" % consts.target_dir)
    os.system("/bin/mknod %s/dev/null c 1 3" % consts.target_dir)
    os.system("/bin/mknod %s/dev/random c 1 8" % consts.target_dir)
    os.system("/bin/mknod %s/dev/urandom c 1 9" % consts.target_dir)

def setTimeZone():
    os.system("rm -rf %s" % os.path.join(consts.target_dir, "etc/localtime"))
    cp("usr/share/zoneinfo/%s" % ctx.installData.timezone, "etc/localtime")
    return True

def migrate_xorg():
    def joy(a):
        return os.path.join(consts.target_dir,a[1:])

    # copy confs
    files = ["/etc/X11/xorg.conf",
             "/etc/hal/fdi/policy/10-keymap.fdi",
             "/var/lib/zorg/config.xml"]

    for conf in files:
        if not os.path.exists(joy(os.path.dirname(conf))):
            os.makedirs(joy(os.path.dirname(conf)))

        if os.path.exists(conf):
            ctx.debugger.log("Copying from '%s' to '%s'" % (conf, joy(conf)))
            shutil.copyfile(conf, joy(conf))

global bus
bus = None

def connectToDBus():
    global bus
    for i in range(40):
        try:
            ctx.debugger.log("trying to start dbus..")
            ctx.bus = bus = dbus.bus.BusConnection(address_or_type="unix:path=%s" % ctx.consts.dbus_socket_file)
            break
        except dbus.DBusException:
            time.sleep(2)
            ctx.debugger.log("wait dbus for 1 second...")
    if bus:
        return True
    return False

def setHostName():
    global bus
    obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")
    obj.setHostName(str(ctx.installData.hostName), dbus_interface="tr.org.pardus.comar.Network.Stack")
    ctx.debugger.log("Hostname set as %s" % ctx.installData.hostName)
    return True

def getUserList():
    import comar
    link = comar.Link(socket=ctx.consts.dbus_socket_file)
    users = link.User.Manager["baselayout"].userList()
    return filter(lambda user: user[0]==0 or (user[0]>=1000 and user[0]<=65000), users)

def setUserPass(uid, password):
    import comar
    link = comar.Link(socket=ctx.consts.dbus_socket_file)
    info = link.User.Manager["baselayout"].userInfo(uid)
    return link.User.Manager["baselayout"].setUser(uid, info[1], info[3], info[4], password, info[5])

def getConnectionList():
    import comar
    link = comar.Link(socket=ctx.consts.dbus_socket_file)
    results = {}
    for package in link.Network.Link:
        results[package] = list(link.Network.Link[package].connections())
    return results

def connectTo(package, profile):
    import comar
    link = comar.Link(socket=ctx.consts.dbus_socket_file)
    return link.Network.Link[package].setState(profile, "up")

def addUsers():
    global bus

    import comar
    link = comar.Link(socket=ctx.consts.dbus_socket_file)

    def setNoPassword(uid):
        link.User.Manager["baselayout"].grantAuthorization(uid, "*")

    obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")
    for u in yali4.users.pending_users:
        ctx.debugger.log("User %s adding to system" % u.username)
        uid = obj.addUser(-1, u.username, u.realname, "", "", unicode(u.passwd), u.groups, [], [], dbus_interface="tr.org.pardus.comar.User.Manager")
        ctx.debugger.log("New user's id is %s" % uid)

        # Use random user icon from YALI Archive
        iconPath = os.path.join(ctx.consts.target_dir,"home/%s/.face.icon" % u.username)
        shutil.copy(u.icon, iconPath)
        os.chmod(iconPath, 0644)
        os.chown(iconPath, uid, 100)

        # Chown for old users..
        user_home_dir = os.path.join(consts.target_dir, 'home', u.username)
        ctx.yali.info.updateAndShow(_("User <b>%s</b>'s home directory is being prepared..") % u.username)
        os.system('chown -R %d:%d %s ' % (uid, 100, user_home_dir))
        os.chmod(user_home_dir, 0711)
        ctx.yali.info.hide()

        # Enable auto-login
        if u.username == ctx.installData.autoLoginUser:
            u.setAutoLogin()

        # Set no password ask for PolicyKit
        if u.noPass:
            setNoPassword(uid)

    return True

def setRootPassword():
    if not ctx.installData.useYaliFirstBoot:
        global bus
        obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")
        obj.setUser(0, "", "", "", str(ctx.installData.rootPassword), "", dbus_interface="tr.org.pardus.comar.User.Manager")
    return True

def writeConsoleData():
    keymap = ctx.installData.keyData["consolekeymap"]
    if isinstance(keymap, list):
        keymap = keymap[1]
    yali4.localeutils.write_keymap(ctx.installData.keyData["consolekeymap"])
    ctx.debugger.log("Keymap stored.")
    return True

def migrateXorgConf():
    if not ctx.yali.install_type == YALI_FIRSTBOOT:
        yali4.postinstall.migrate_xorg()
        ctx.debugger.log("xorg.conf and other files merged.")
    return True

def copyPisiIndex():
    target = os.path.join(ctx.consts.target_dir, "var/lib/pisi/index/%s" % ctx.consts.pardus_repo_name)

    if os.path.exists(ctx.consts.pisiIndexFile):
        # Copy package index
        shutil.copy(ctx.consts.pisiIndexFile, target)
        shutil.copy(ctx.consts.pisiIndexFileSum, target)

        # Extract the index
        import bz2
        pureIndex = file(os.path.join(target,"pisi-index.xml"),"w")
        pureIndex.write(bz2.decompress(open(ctx.consts.pisiIndexFile).read()))
        pureIndex.close()

        ctx.debugger.log("pisi index files copied.")
    else:
        ctx.debugger.log("pisi index file not found!")
    return True

def setPackages():
    global bus
    if ctx.yali.install_type == YALI_OEMINSTALL:
        ctx.debugger.log("OemInstall selected.")
        try:
            obj = bus.get_object("tr.org.pardus.comar", "/package/yali4")
            obj.setState("on", dbus_interface="tr.org.pardus.comar.System.Service")
            file("%s/etc/yali-is-firstboot" % ctx.consts.target_dir, "w")
            obj = bus.get_object("tr.org.pardus.comar", "/package/kdebase")
            obj.setState("off", dbus_interface="tr.org.pardus.comar.System.Service")
        except:
            ctx.debugger.log("Dbus error: package doesnt exist !")
            return False
    elif ctx.yali.install_type in [YALI_INSTALL, YALI_FIRSTBOOT]:
        try:
            obj = bus.get_object("tr.org.pardus.comar", "/package/yali4")
            obj.setState("off", dbus_interface="tr.org.pardus.comar.System.Service")
            obj = bus.get_object("tr.org.pardus.comar", "/package/kdebase")
            obj.setState("on", dbus_interface="tr.org.pardus.comar.System.Service")
            os.unlink("%s/etc/yali-is-firstboot" % ctx.consts.target_dir)
            os.system("pisi rm yali4")
        except:
            ctx.debugger.log("Dbus error: package doesnt exist !")
            return False
    return True


