# -*- coding: utf-8 -*-

"""
    Daemon
"""

import atexit
import logging
import os
import signal
import sys
import time


class Daemon:
    """
        A generic daemon class.

        Subclass the Daemon class and override the run() method.
    """

    def __init__(self, pidfile=None, stdin="/dev/null", 
                 stdout="/dev/null", stderr="/dev/null"):
        """
            Inits daemon class.

            Args:
                pidfile: PID filename
                stdin: Input sink
                stdout: Output sink
                stderr: Error sink
        """
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
            Does the UNIX double-fork magic.
        """
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError, error:
            msg = "fork #1 failed: %d (%s)\n" % (error.errno, error.strerror)
            sys.stderr.write(msg)
            sys.exit(1)

        # Decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # Exit from second parent
                sys.exit(0)
        except OSError, error:
            msg = "fork #2 failed: %d (%s)\n" % (error.errno, error.strerror)
            sys.stderr.write(msg)
            sys.exit(1)

        logging.debug("Running in background.")

        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        stdin = file(self.stdin, 'r')
        stdout = file(self.stdout, 'a+')
        stderr = file(self.stderr, 'a+', 0)
        os.dup2(stdin.fileno(), sys.stdin.fileno())
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())

        if self.pidfile:
            # Write pidfile
            atexit.register(self.delpid)
            pid = str(os.getpid())
            file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        """
            Removes PID file.
        """
        os.remove(self.pidfile)

    def start(self):
        """
            Start the daemon.
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pidfile = file(self.pidfile,'r')
            pid = int(pidfile.read().strip())
            pidfile.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
            Stops the daemon.
        """
        # Get the pid from the pidfile
        try:
            pidfile = file(self.pidfile,'r')
            pid = int(pidfile.read().strip())
            pidfile.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return

        # Try killing the daemon process
        try:
            while True:
                os.kill(pid, signal.SIGINT)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
            Restarts the daemon.
        """
        self.stop()
        self.start()

    def run(self):
        """
            You should override this method when you subclass Daemon. It will be called after the process has been
            daemonized by start() or restart().
        """
