# -*- coding: utf-8 -*-

"""
    Mainloop
"""

import logging
import multiprocessing
import signal

from ahenk.agent import daemon
from ahenk.agent import workers


class Agent(daemon.Daemon):
    """
        Ahenk-Agent (agent) daemon class.

        Usage:
            agent = Agent(options)
            agent.run() # Interactive

            agent = Agent(options)
            agent.start() # Daemon
    """

    def __init__(self, options):
        """
            Inits Ahenk-Agent (agent) daemon.
        """
        daemon.Daemon.__init__(self, options.pidfile)
        self.options = options

    def run(self):
        """
            Main event loop.
        """

        logging.info("Starting Ahenk Agent.")

        # Message queues
        q_in = multiprocessing.Queue()
        q_out = multiprocessing.Queue()

        # Queue for triggering client-pulls
        q_force = multiprocessing.Queue()

        # Worker processes
        proc_ldap = multiprocessing.Process(target=workers.worker_ldap,
                                            args=(self.options, q_in, q_out, q_force))
        proc_xmpp = multiprocessing.Process(target=workers.worker_xmpp,
                                            args=(self.options, q_in, q_out))
        proc_applier = multiprocessing.Process(target=workers.worker_applier,
                                               args=(self.options, q_in, q_out, q_foce))

        # Signal handler
        def signal_handler(signum, frame):
            """
                Terminates child processes.
            """
            logging.info("Stopping Ahenk Agent.")
            try:
                proc_xmpp.terminate()
                proc_ldap.terminate()
                proc_applier.terminate()
            except (OSError, AttributeError):
                pass
        signal.signal(signal.SIGINT, signal_handler)

        # Start child processes
        proc_applier.start()
        proc_ldap.start()
        proc_xmpp.start()

        try:
            proc_applier.join()
            proc_ldap.join()
            proc_xmpp.join()
        except OSError:
            pass
