# -*- coding: utf-8 -*-
import subprocess


def run_quiet(cmd):
  subprocess.call(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def chrootRun(path,cmd):
  run_quiet("chroot %s %s" % (path, cmd))
  
