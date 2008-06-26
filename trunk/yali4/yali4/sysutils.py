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

# sysutils module provides basic system utilities

import os
import subprocess
from string import ascii_letters
from string import digits
from pardus.sysutils import find_executable
from pardus.procutils import run

from yali4._sysutils import *
from yali4.constants import consts

##
# run dbus daemon in chroot
def chroot_dbus():

    # FIXME: use mount module (needs options support)
    tgt = os.path.join(consts.target_dir, "dev")
    os.system("mount --bind /dev %s" % tgt)
    tgt = os.path.join(consts.target_dir, "proc")
    os.system("mount --bind /proc %s" % tgt)
    tgt = os.path.join(consts.target_dir, "sys")
    os.system("mount --bind /sys %s" % tgt)

    os.system("chroot %s /sbin/ldconfig" % consts.target_dir)
    os.system("chroot %s /sbin/update-environment" % consts.target_dir)
    os.system("chroot %s /bin/service dbus start" % consts.target_dir)

def checkYaliParams(param):
    for i in [x for x in open("/proc/cmdline", "r").read().split()]:
        if i.startswith("yali4="):
            if param in i.split("=")[1].split(","):
                return True
    return False

def swap_as_file(filepath, mb_size):
    dd, mkswap = find_executable('dd'), find_executable('mkswap')

    if (not dd) or (not mkswap): return False

    create_swap_file = "%s if=/dev/zero of=%s bs=1024 count=%d" % (dd, filepath, (int(mb_size)*1024))
    mk_swap          = "%s %s" % (mkswap, filepath)

    try:
        for cmd in [create_swap_file, mk_swap]:
            p = os.popen(cmd)
            p.close()
        os.chmod(filepath, 0600)
    except:
        return False

    return True

##
# total memory size
def mem_total():
    m = open("/proc/meminfo")
    for l in m:
        if l.startswith("MemTotal"):
            return int(l.split()[1]) / 1024
    return None

def eject_cdrom(mount_point=consts.source_dir):
    os.system("eject -m %s" % mount_point)

def text_is_valid(text):
    allowed_chars = ascii_letters + digits + '.' + '_' + '-'
    return len(text) == len(filter(lambda u: [x for x in allowed_chars if x == u], text))

def add_hostname(hostname = 'pardus'):
    hostname_file = os.path.join(consts.target_dir, 'etc/env.d/01hostname')
    hosts_file = os.path.join(consts.target_dir, 'etc/hosts')

    def getCont(x):
        return open(x).readlines()
    def getFp(x):
        return open(x, "w")

    hostname_fp, hosts_fp = getFp(hostname_file), getFp(hosts_file)
    hostname_contents = ""
    hosts_contents = ""
    if os.path.exists(hostname_file):
        hostname_contents = getCont(hostname_file)
    if os.path.exists(hosts_file):
        hosts_contents = getCont(hosts_file)

    if hostname_contents:
        for line in hostname_contents:
            if line.startswith('HOSTNAME'):
                line = 'HOSTNAME="%s"\n' % hostname
            hostname_fp.write(line)
        hostname_fp.close()
    else:
        hostname_fp.write('HOSTNAME="%s"\n' % hostname)

    if hosts_contents:
        for line in hosts_contents:
            if line.startswith('127.0.0.1'):
                line = '127.0.0.1\t\tlocalhost %s\n' % hostname
            hosts_fp.write(line)
        hosts_fp.close()
    else:
        hosts_fp.write('127.0.0.1\t\tlocalhost %s\n' % hostname)

def mount(source, target, fs, needs_mtab=False):
    params = ["-t", fs, source, target]
    if not needs_mtab:
        params.insert(0,"-n")

    mount_res = execClear("mount",
                          params,
                          stdout="/tmp/mount.log",
                          stderr="/tmp/mount.log")

def is_windows_boot(partition_path, file_system):
    m_dir = "/tmp/pcheck"
    if not os.path.isdir(m_dir):
        os.makedirs(m_dir)
    try:
        if file_system == "fat32":
            mount(partition_path, m_dir, "vfat")
        else:
            mount(partition_path, m_dir, file_system)
    except:
        return False

    exist = lambda f: os.path.exists(os.path.join(m_dir, f))

    if exist("boot.ini") or exist("command.com") or exist("bootmgr"):
        umount(m_dir)
        return True
    else:
        umount(m_dir)
        return False

def is_linux_boot(partition_path, file_system):
    import yali4.gui.context as ctx
    m_dir = "/tmp/pcheck"
    if not os.path.isdir(m_dir):
        os.makedirs(m_dir)
    umount(m_dir)

    ctx.debugger.log("Mounting %s to /tmp/pcheck" % partition_path)

    try:
        mount(partition_path, m_dir, file_system)
    except:
        ctx.debugger.log("Mount failed for %s " % partition_path)
        return False

    exist = lambda f: os.path.exists(os.path.join(m_dir,"boot/grub/", f))

    if exist("grub.conf") or exist("menu.lst"):
        menuLst = os.path.join(m_dir,"boot/grub/menu.lst")
        grubCnf = os.path.join(m_dir,"boot/grub/grub.conf")
        if os.path.islink(menuLst):
            ctx.debugger.log("grub.conf found on device %s" % partition_path)
            return grubCnf
        else:
            ctx.debugger.log("menu.lst found on device %s" % partition_path)
            return menuLst
        return False
    else:
        return False

def umount_(dir):
    os.system("umount %s" % dir)

def reboot():
    print "Rebooting..."
    try:
        umount(consts.target_dir + "/home")
    except:
        pass
    umount(consts.target_dir)
    fastreboot()

# Shamelessly stolen from Anaconda :)
def execClear(command, argv, stdin = 0, stdout = 1, stderr = 2):
    import yali4.gui.context as ctx

    argv = list(argv)
    if type(stdin) == type("string"):
        if os.access(stdin, os.R_OK):
            stdin = open(stdin)
        else:
            stdin = 0
    if type(stdout) == type("string"):
        stdout = open(stdout, "w")
    if type(stderr) == type("string"):
        stderr = open(stderr, "w")
    if stdout is not None and type(stdout) != int:
        ctx.debugger.log("Running CMD : %s" %([command] + argv,))
        stdout.write("Running... %s\n" %([command] + argv,))

    p = os.pipe()
    childpid = os.fork()
    if not childpid:
        os.close(p[0])
        os.dup2(p[1], 1)
        os.dup2(stderr.fileno(), 2)
        os.dup2(stdin, 0)
        os.close(stdin)
        os.close(p[1])
        stderr.close()

        os.execvp(command, [command] + argv)
        os._exit(1)

    os.close(p[1])

    while 1:
        try:
            s = os.read(p[0], 1)
        except OSError, args:
            (num, str) = args
            if (num != 4):
                raise IOError, args

        stdout.write(s)
        ctx.mainScreen.processEvents()

        if len(s) < 1:
            break

    try:
        (pid, status) = os.waitpid(childpid, 0)
    except OSError, (num, msg):
        ctx.debugger.log("exception from waitpid: %s %s" %(num, msg))

    if status is None:
        return 0

    if os.WIFEXITED(status):
        return os.WEXITSTATUS(status)

    return 1


## Run an external program and capture standard out.
# @param command The command to run.
# @param argv A list of arguments.
# @param stdin The file descriptor to read stdin from.
# @param stderr The file descriptor to redirect stderr to.
# @param root The directory to chroot to before running command.
# @return The output of command from stdout.
def execWithCapture(command, argv, stdin = 0, stderr = 2, root ='/'):
    argv = list(argv)

    if type(stdin) == type("string"):
        if os.access(stdin, os.R_OK):
            stdin = open(stdin)
        else:
            stdin = 0

    if type(stderr) == type("string"):
        stderr = open(stderr, "w")

    try:
        pipe = subprocess.Popen([command] + argv, stdin = stdin,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                cwd=root)
    except OSError, ( errno, msg ):
        raise RuntimeError, "Error running " + command + ": " + msg

    rc = pipe.stdout.read()
    pipe.wait()
    return rc


import re
import string

# Based on RedHat's ZoneTab class
class TimeZoneEntry:
    def __init__(self, code=None, timeZone=None):
        self.code = code
        self.timeZone = timeZone

class TimeZoneList:
    def __init__(self, fromFile='/usr/share/zoneinfo/zone.tab'):
        self.entries = []
        self.readTimeZone(fromFile)

    def getEntries(self):
        return self.entries

    def readTimeZone(self, fn):
        f = open(fn, 'r')
        comment = re.compile("^#")
        while 1:
            line = f.readline()
            if not line:
                break
            if comment.search(line):
                continue
            fields = string.split(line, '\t')
            if len(fields) < 3:
                continue
            code = fields[0]
            timeZone = string.strip(fields[2])
            entry = TimeZoneEntry(code, timeZone)
            self.entries.append(entry)


