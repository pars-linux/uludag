#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import fcntl
import termios
import signal
import subprocess
import sys

def start():
    def fork_handler():
            # Set umask to a sane value
            # (other and group has no write permission by default)
            os.umask(022)
            # Detach from controlling terminal
            try:
                tty_fd = os.open("/dev/tty", os.O_RDWR)
                fcntl.ioctl(tty_fd, termios.TIOCNOTTY)
                os.close(tty_fd)
            except OSError:
                pass
            # Close IO channels
            devnull_fd = os.open("/dev/null", os.O_RDWR)
            os.dup2(devnull_fd, 0)
            os.dup2(devnull_fd, 1)
            os.dup2(devnull_fd, 2)
            # Detach from process group
            os.setsid()

    cmd = ["/usr/bin/comar-dbus", "--debug=all"]

    print "Starting Comar..."
    popen = subprocess.Popen(cmd, close_fds=True, preexec_fn=fork_handler, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def stop():
    def _getPid(pidfile):
        """Read process ID from a .pid file."""
        try:
            pid = file(pidfile).read()
        except IOError, e:
            if e.errno != 2:
                raise
            return None
        # Some services put custom data after the first line
        pid = pid.split("\n")[0]
        # Non-pid data is also seen when stopped state in some services :/
        if len(pid) == 0 or len(filter(lambda x: not x in "0123456789", pid)) > 0:
            return None
        return int(pid)

    pid = _getPid("/var/run/comar-dbus.pid")

    if pid:
        print "Stopping %s..." % pid
        os.kill(pid, signal.SIGHUP)
    else:
        print "Comar is not running..."


if __name__ == "__main__":
    if os.getuid() != 0:
        print "Got root?"
        sys.exit(1)
    if len(sys.argv) < 2 or sys.argv[1] not in ["start", "stop"]:
        print "Usage: %s start|stop" % sys.argv[0]
        sys.exit(1)
    if sys.argv[1] == "start":
        start()
    else:
        stop()
    sys.exit(0)
