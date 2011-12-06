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

from datetime import datetime
import socket

TIMEOUT = 5


OPTIONS = None
XMLSTREAM = None
Q_IN = None
Q_OUT = None
myJid = None
factory = None

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
    if( datetime.now().second%30 == 0 ):
        s = socket.socket()
        try:
            logging.warning("Checking Network Link")
            s.connect((OPTIONS.hostname, 5222))
            s.close()
            s = None;
        except:
            logging.warning("Network is unreachable now. try to reconnect")
            time.sleep(TIMEOUT)
            connect()
    if not XMLSTREAM:
        return
    try:
        msg = Q_OUT.get(timeout=0.1)
    except Queue.Empty:
        return
    except IOError:
        return
    if 'to' in msg:
        message = xish.domish.Element(('jabber:client','message'))
        message["to"] = msg["to"]
        message["type"] = "chat"
        message.addElement("body", "jabber:client", msg["body"])
        XMLSTREAM.send(message)
    elif 'subscribe' in msg:
        # Subscribe to all admins
        for user_dn in msg['subscribe']:
            username = user_dn.split(',')[0].split('=')[1]
            logging.debug("Subscribing to %s@%s" % (username, OPTIONS.domain))
            message = xish.domish.Element(('jabber:client','presence'))
            message["to"] = "%s@%s" % (username, OPTIONS.domain)
            message["type"] = "subscribe"
            XMLSTREAM.send(message)

def connect():
    reactor.connectTCP(OPTIONS.hostname, 5222, factory, 10)

def xmpp_go(options, q_in, q_out):
    """
        Main event loop for XMPP worker
    """
    global Q_IN, Q_OUT, OPTIONS, myJid, factory

    Q_IN = q_in
    Q_OUT = q_out
    OPTIONS = options


    myJid = jid.JID('%s@%s/Ahenk' % (OPTIONS.username, OPTIONS.domain))
    factory = client.XMPPClientFactory(myJid, OPTIONS.password)
    factory.clientConnectionLost = event_connection_lost
    factory.clientConnectionFailed = event_connection_failed
    factory.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, event_session_start)
    factory.addBootstrap(xmlstream.INIT_FAILED_EVENT, event_init_failed)

    # Send messages in queue every 0.1 seconds
    task.LoopingCall(task_message_queue).start(1.0)

    # Connect to XMPP server
    connect()

    try:
        reactor.run()
    except:
        pass
