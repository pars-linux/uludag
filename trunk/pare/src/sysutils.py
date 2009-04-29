# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

def execWithCapture(command, argv, stdin = 0, stderr = 2, root ='/'):
     argv = list(argv)

     if isinstance(stdin, str):
         if os.access(stdin, os.R_OK):
             stdin = open(stdin)
         else:
             stdin = 0

     if isinstance(stderr, str):
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

def execClear(command, argv, stdin = 0, stdout = 1, stderr = 2):

    argv = list(argv)
    if isinstance(stdin, str):
        if os.access(stdin, os.R_OK):
            stdin = open(stdin)
        else:
            stdin = 0
    if isinstance(stdout, str):
        stdout = open(stdout, "w")
    if isinstance(stderr, str):
        stderr = open(stderr, "w")
    if stdout is not None and not isinstance(stdout, int):
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
            (num, msg) = args
            if (num != 4):
                raise IOError, args

        stdout.write(s)

        if len(s) < 1:
            break

    try:
        (pid, status) = os.waitpid(childpid, 0)
    except OSError, (num, msg):
        pass
    if status is None:
        return 0

    if os.WIFEXITED(status):
        return os.WEXITSTATUS(status)

    return 1

def notify_kernel(path, action="change"):
    """ Signal the kernel that the specified device has changed. """
    log.debug("notifying kernel of '%s' event on device %s" % (action, path))
    path = os.path.join(path, "uevent")
    if not path.startswith("/sys/") or not os.access(path, os.W_OK):
        log.debug("sysfs path '%s' invalid" % path)
        raise ValueError("invalid sysfs path")

    f = open(path, "a")
    f.write("%s\n" % action)
    f.close()

def get_sysfs_path_by_name(dev_name, class_name="block"):
    dev_name = os.path.basename(dev_name)
    sysfs_class_dir = "/sys/class/%s" % class_name
    dev_path = os.path.join(sysfs_class_dir, dev_name)
    if os.path.exists(dev_path):
        return dev_path