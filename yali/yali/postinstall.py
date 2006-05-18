# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
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

from yali.constants import consts

# necessary things after a full install


def initbaselayout():
    
    def cp(s, d):
        src = os.path.join(consts.target_dir, s)
        dst = os.path.join(consts.target_dir, d)
        shutil.copyfile(src, dst)

    def touch(f, m=0644):
        f = os.path.join(consts.target_dir, f)
        open(f, "w", m).close()

    def chgrp(f, group):
        f = os.path.join(consts.target_dir, f)
        gid = int(grp.getgrnam(group)[2])
        os.chown(f, 0, gid)

    # create /etc/hosts
    cp("usr/share/baselayout/hosts", "etc/hosts")

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


    # copy xorg.conf.
    src = "/etc/X11/xorg.conf"
    dst = os.path.join(consts.target_dir, "etc/X11/xorg.conf")
    if os.path.exists(src):
        try:
            os.makedirs(os.path.dirname(dst))
        except OSError:
            pass
        shutil.copyfile(src, dst)
