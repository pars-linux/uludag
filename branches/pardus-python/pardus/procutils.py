# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

"""procutils module provides basic process utilities."""

import os
import time
import socket
import subprocess

from pardus.fileutils import FileLock

def synchronized(func):
    """Syncronize method call with a per method lock.
    
    This decorator makes sure that only one instance of the script's
    method run in any given time.
    """
    class Handler:
        def handler(self, *args, **kwargs):
            lock = FileLock("/var/run/comar-%s-%s.lock" % (script(), self.myfunc.__name__))
            lock.lock()
            self.myfunc(*args, **kwargs)
            lock.unlock()
    h = Handler()
    h.myfunc = func
    return h.handler

class execReply(int):
    def __init__(self, value):
        int.__init__(self, value)
        self.stdout = None
        self.stderr = None

def run(*cmd):
    """Run a command without running a shell"""
    command = []
    if len(cmd) == 1:
        if isinstance(cmd[0], basestring):
            command = cmd[0].split()
        else:
            command = cmd[0]
    else:
        command = cmd
    proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    reply = execReply(proc.wait())
    reply.stdout, reply.stderr = proc.communicate()
    return reply

def waitBus(unix_name, timeout=5, wait=0.1, stream=True):
    if stream:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    else:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    while timeout > 0:
        try:
            sock.connect(unix_name)
            return True
        except:
            timeout -= wait
        time.sleep(wait)
    return False
