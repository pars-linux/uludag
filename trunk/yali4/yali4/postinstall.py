# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import shutil
import grp

from yali4.constants import consts
import yali4.gui.context as ctx

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

