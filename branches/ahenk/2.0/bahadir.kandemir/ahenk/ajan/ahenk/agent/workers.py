# -*- coding: utf-8 -*-

"""
    Worker processes
"""

import logging
import signal

from ahenk.agent import bck_ldap
from ahenk.agent import bck_xmpp
from ahenk.agent import utils


def worker_ldap(options, q_in, q_out, q_ldap):
    """
        LDAP interface for fetching policies.
    """

    logging.debug("LDAP client is running.")

    # Ignore interrupt signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Start LDAP client event lop
    bck_ldap.ldap_go(options, q_in, q_out, q_ldap)


def worker_xmpp(options, q_in, q_out):
    """
        XMMP interface for direct communication with clients.
    """

    logging.debug("XMPP client is running.")

    # Ignore interrupt signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Start XMPP client event lop
    bck_xmpp.xmpp_go(options, q_in, q_out)


def worker_applier(options, q_in, q_out, q_ldap):
    """
        Worker that does all the dirty job.
    """

    children = []

    def signal_handler(signum, frame):
        """
            Terminates child processes.

            "children" list is filled by process_modules method.
        """
        for proc in children:
            try:
                proc.terminate()
            except (OSError, AttributeError):
                pass

    # Register handler for interrupt signals
    signal.signal(signal.SIGINT, signal_handler)

    logging.debug("Policy applier is running.")

    # Processes all messages in queue
    while True:
        try:
            msg = q_in.get()
        except IOError:
            continue

        if msg["type"] == "command":
            message = utils.Command(msg, q_out)
        elif msg["type"] == "policy":
            message = utils.Policy(msg)
        elif msg["type"] == "policy init":
            message = utils.Policy(msg, True)
        else:
            message = utils.Message(msg, q_out)

        if message.type == "command" and message.command == "ahenk.force_update":
            q_ldap.put(True)
            continue

        # Pass message to all Ahenk modules
        utils.process_modules(options, message, children)
