# -*- coding: utf-8 -*-

"""
    XMPP client backend
"""

import logging
import Queue
import traceback
import time

from twisted.words.protocols.jabber import client, jid, xmlstream
from twisted.internet import task
from twisted.words import xish
from twisted.internet import reactor, error

TIMEOUT = 5


OPTIONS = None
XMLSTREAM = None
Q_IN = None
Q_OUT = None


def event_session_start(stream):
    """
        Session handler
    """
    global XMLSTREAM
    XMLSTREAM = stream

    stream.addObserver('/iq', event_iq)
    stream.addObserver('/message', event_message)
    stream.addObserver('/presence', event_presence)

    logging.debug("Logged in as %s@%s" % (OPTIONS.username, OPTIONS.domain))

    prs = xish.domish.Element(('jabber:client','presence'))
    prs.addElement('status').addContent('Online')
    stream.send(prs)

    # Subscribe to all admins
    for username in OPTIONS.admin:
        logging.debug("Subscribing to %s@%s" % (username, OPTIONS.domain))
        prs = xish.domish.Element(('jabber:client','presence'))
        prs["to"] = "%s@%s" % (username, OPTIONS.domain)
        prs["type"] = "subscribe"
        stream.send(prs)

def event_iq(iq):
    """
        Iq handler
    """
    pass

def event_presence(presence):
    """
        Presence handler
    """
    # Accept all subscriptions from admins
    if presence.getAttribute("type", None) == "subscribe":
        if presence["from"].split("@")[0] not in OPTIONS.admin:
            return
        logging.debug("Accepting subscription from %s" % presence["from"])
        prs = xish.domish.Element(('jabber:client','presence'))
        prs["to"] = presence["from"]
        prs["type"] = "subscribed"
        XMLSTREAM.send(prs)

def event_message(message):
    """
        Message handler
    """
    for tag in message.elements():
        if tag.name == "body":
            logging.debug("Message received from %s" % message["from"])
            Q_IN.put({"type": "command", "from": message["from"], "command": unicode(tag.__str__())})
            break

def event_connection_lost(connector, reason):
    """
        Reconnects if session ends.
    """
    if reason.type == error.ConnectionDone:
        logging.warning("XMPP connection lost. Retrying in %d seconds." % TIMEOUT)
        time.sleep(TIMEOUT)
        connect()

def event_connection_failed(connector, reason):
    """
        Reconnects if connection fails.
    """
    logging.warning("XMPP connection failed. Retrying in %d seconds." % TIMEOUT)
    time.sleep(TIMEOUT)
    connect()

def event_init_failed(reason):
    """
        Reconnects if authentication fails.
    """
    logging.warning("XMPP authentication failed. Retrying in %d seconds." % TIMEOUT)
    time.sleep(TIMEOUT)
    connect()

def task_message_queue():
    """
        .
    """
    if not XMLSTREAM:
        return
    try:
        msg = Q_OUT.get(timeout=0.1)
    except Queue.Empty:
        return
    except IOError:
        return
    message = xish.domish.Element(('jabber:client','message'))
    message["to"] = msg["to"]
    message["type"] = "chat"
    message.addElement("body", "jabber:client", msg["body"])
    XMLSTREAM.send(message)

def connect():
    myJid = jid.JID('%s@%s' % (OPTIONS.username, OPTIONS.domain))
    factory = client.XMPPClientFactory(myJid, OPTIONS.password)
    factory.clientConnectionLost = event_connection_lost
    factory.clientConnectionFailed = event_connection_failed
    factory.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, event_session_start)
    factory.addBootstrap(xmlstream.INIT_FAILED_EVENT, event_init_failed)
    reactor.connectTCP(OPTIONS.hostname, 5222, factory)

def xmpp_go(options, q_in, q_out):
    """
        Main event loop for XMPP worker
    """
    global Q_IN, Q_OUT, OPTIONS

    Q_IN = q_in
    Q_OUT = q_out
    OPTIONS = options

    # Send messages in queue every 0.1 seconds
    task.LoopingCall(task_message_queue).start(0.1)

    # Connect to XMPP server
    connect()

    try:
        reactor.run()
    except:
        pass
