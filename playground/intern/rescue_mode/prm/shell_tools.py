# -*- coding: utf-8 -*-
"""This module for use shell command easyly"""

import subprocess


def run_quiet(cmd):
    """Runs the given command quietly."""
    subprocess.call(cmd, shell=True, 
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def chroot_run(path, cmd):
    """Runs the given command in a chroot."""
    run_quiet("chroot %s %s" % (path, cmd))

def mount(source, target, file_system='', param=''):
    """Mounts the given device."""
    if file_system != '':
        file_system = "-t %s" % file_system
    run_quiet("mount %s %s %s %s" % (param, file_system, source, target))

def umount(target, param=''):
    """Unmount the given device"""
    run_quiet("umount %s %s" % (param, target))

def reboot():
    """Reboot the system"""
    run_quiet("/sbin/reboot -f")

def shutdown():
    """Shut down the computer"""
    run_quiet("/sbin/shutdown -h now")
