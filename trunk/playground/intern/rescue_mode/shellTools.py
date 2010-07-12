# -*- coding: utf-8 -*-
import subprocess


def run_quiet(cmd):
    """Runs the given command quietly."""
    subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def chrootRun(path, cmd):
    """Runs the given command in a chroot."""
    run_quiet("chroot %s %s" % (path, cmd))

def mount(source, target, fs='', param=''):
    """Mounts the given device."""
    if fs != '':
        fs = "-t %s" % fs
    run_quiet("mount %s %s %s %s" % (param, fs, source, target))

def umount(target, param=''):
    run_quiet("umount %s %s" % (param, target))

def reboot():
    run_quiet("/tmp/reboot -f")

def shutdown():
    run_quiet("/tmp/shutdown -h now")
