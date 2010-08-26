# -*- coding: utf-8 -*-

"""
    Worker processes
"""

import logging
from multiprocessing import Array
import signal

from ahenk.agent import bck_ldap
from ahenk.agent import bck_xmpp
from ahenk.agent import utils


def worker_ldap(options, q_in, q_out):
    """
        LDAP interface for fetching policies.
    """

    logging.debug("LDAP client is running.")

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    bck_ldap.ldap_go(options, q_in, q_out)


def worker_xmpp(options, q_in, q_out):
    """
        XMMP interface for direct communication with clients.
    """

    logging.debug("XMPP client is running.")

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    bck_xmpp.xmpp_go(options, q_in, q_out)


def worker_applier(options, q_in, q_out):
    """
        Worker that does all the dirty job.
    """

    children = []

    def signal_handler(signum, frame):
        """
            Terminates child processes.
        """
        try:
            for proc in children:
                proc.terminate()
        except (OSError, AttributeError):
            pass
    signal.signal(signal.SIGINT, signal_handler)

    logging.debug("Policy applier is running.")

    while True:
        try:
            msg = q_in.get()
        except IOError:
            return
        if msg["type"] == "command":
            message = utils.Command(msg, q_out)
        elif msg["type"] == "policy":
            message = utils.Policy(msg)
        elif msg["type"] == "policy init":
            message = utils.Policy(msg, True)
        else:
            message = utils.Message(msg, q_out)
        utils.process_modules(options, message, children)
