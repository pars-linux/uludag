# -*- coding: utf-8 -*-
import subprocess


def run_quiet(cmd):
  subprocess.call(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def chrootRun(path,cmd):
  run_quiet("chroot %s %s" % (path, cmd))
  
def mount(source, target, fs='', param=''):
    if fs != '':
      fs ="-t "+fs
    run_quiet("mount %s %s %s %s"%(param,fs,source,target))
def umount(target,param=''):
    run_quiet("umount %s %s"%(param,target))
def reboot():
    run("/tmp/reboot -f")
def shutdown():
    run("/tmp/shutdown -h now")
