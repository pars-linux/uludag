#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pwd

globalSymlinkList = [
("/usr/kde/4/bin", "/usr/bin"),
("/usr/kde/4/env", "/usr/share/kde4/env"),
("/usr/kde/4/include", "/usr/include/kde4"),
("/usr/kde/4/lib", "/usr/lib"),
("/usr/kde/4/share/applications", "/usr/share/applications"),
("/usr/kde/4/share/apps", "/usr/share/kde4/apps"),
("/usr/kde/4/share/autostart", "/usr/share/autostart"),
("/usr/kde/4/share/config", "/usr/share/kde4/config"),
("/usr/kde/4/share/config.kcfg", "/usr/share/config.kcfg"),
("/usr/kde/4/share/desktop-directories", "/usr/share/desktop-directories"),
("/usr/kde/4/share/doc/HTML", "/usr/share/doc/kde4/html"),
("/usr/kde/4/share/emoticons", "/usr/share/emoticons"),
("/usr/kde/4/share/icons", "/usr/share/icons"),
("/usr/kde/4/share/kde4", "/usr/share/kde4"),
("/usr/kde/4/share/locale", "/usr/share/locale"),
("/usr/kde/4/share/man", "/usr/share/man"),
("/usr/kde/4/share/mime", "/usr/share/mime"),
("/usr/kde/4/share/mimelnk", "/usr/share/mimelnk"),
("/usr/kde/4/share/sounds", "/usr/share/sounds"),
("/usr/kde/4/share/templates", "/usr/share/templates"),
("/usr/kde/4/share/wallpapers", "/usr/share/wallpapers"),
("/usr/kde/4/shutdown", "/usr/share/kde4/shutdown"),
]

def migrateKDE():
    for src, dst in globalSymlinkList:
        os.symlink(src, dst)

    for user in [u for u in os.listdir("/home") if not u.startswith(".")]: #we may use pwd.getpwall here
        homeDir = os.path.join("/home", user)

        try:
            os.symlink("./kde4", os.path.join(homeDir, ".kde"))
        except OSError:
            continue

        try:
            uid, gid = pwd.getpwnam(user)[2], pwd.getpwnam(user)[3]
        except KeyError:
            continue

        os.chown(os.path.join(homeDir, ".kde"), uid, gid)

        try:
            os.unlink(os.path.join(homeDir, ".kde4", "share", "config", "kaptanrc"))
        except OSError:
            continue

if __name__ == "__main__":
    migrateKDE()
