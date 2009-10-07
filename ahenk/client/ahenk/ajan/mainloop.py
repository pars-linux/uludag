#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import Queue
import signal
import time

from ahenk.ajan import daemon
from ahenk.ajan import workers

class Ajan(daemon.Daemon):
    def __init__(self, options):
        daemon.Daemon.__init__(self, options.pidfile)
        self.options = options

    def run(self):
        # Initialize logger
        log_level = logging.INFO
        if self.options.verbose:
            log_level = logging.DEBUG
        log_file = None
        if self.options.daemon:
            log_file = self.options.logging
        logging.basicConfig(filename=log_file, level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        logging.info("Running.")

        # Queue for fetcher messages
        queue_fetcher = Queue.Queue(0)
        # Queue for policies to be applied
        queue_applier = Queue.Queue(0)

        # This thread modifies the system according to current policy
        thread_applier = workers.Applier(self.options, queue_applier, queue_fetcher)

        # This thread periodically checks central policy changes
        thread_fetcher = workers.Fetcher(self.options, queue_fetcher)

        # Handle signals
        def signal_handler(signum, frame):
            if not thread_fetcher.active and not thread_applier.active:
                return
            logging.info("Shutting down.")
            thread_fetcher.active = False
            thread_applier.active = False
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # Start threads
        thread_applier.start()
        thread_fetcher.start()

        # Serve forever
        while thread_fetcher.isAlive() or thread_applier.isAlive():
            if not queue_fetcher.empty():
                op, data = queue_fetcher.get()

                if op == "policy":
                    queue_applier.put(data)

            time.sleep(0.5)
