#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    XMPP service helper utilities
"""

# Standard modules
import simplejson
import time

# Qt4 modules
from PyQt4 import QtCore

# Twisted Matrix modules
from twisted.words.protocols.jabber import client, jid, xmlstream
from twisted.internet import task
from twisted.words import xish
from twisted.internet import reactor, error

Online = 1
Offline = 0
Error = -1

class Talk(QtCore.QThread):
    """
        Starts a XMPP client in a thread.

        Usage:
            talk = Talk()
            talk.connect("user", "jabber.org", "password")

            # To close connection:
            talk.disconnect()

            # Listen signals:
            self.connect(talk, QtCore.SIGNAL("stateChanged(int)"), self.stateChanged)
            self.connect(talk, QtCore.SIGNAL("messageFetched(QString, QString, QString)"), self.messageFetched)
            self.connect(talk, QtCore.SIGNAL("userStatusChanged(QString, int)"), self.userStatusChanged)
    """
    def __init__(self):
        """
            Constructor for XMPP client thread.
        """
        QtCore.QThread.__init__(self)

        self.is_connected = False
        self.username = None
        self.domain = None
        self.password = None
        self.connector = None
        self.stream = None
        self.online = []

        # Looping call for checking for shutdown request
        task.LoopingCall(self.__task_shutdown).start(0.5)

    def connect(self, hostname, domain, username, password):
        """
            Connects to username@domain with specified password

            Arguments:
                hostname: XMPP server address
                domain: XMPP domain name
                username: User name
                password: User password
        """
        if self.connector and self.is_connected:
            self.disconnect()

        self.hostname = hostname
        self.domain = domain
        self.username = username
        self.password = password

        myJid = jid.JID('%s@%s' % (self.username, self.domain))
        factory = client.XMPPClientFactory(myJid, self.password)
        factory.clientConnectionLost = self.__event_connection_lost
        factory.clientConnectionFailed = self.__event_connection_failed
        factory.addBootstrap(xmlstream.STREAM_AUTHD_EVENT, self.__event_session_start)

        self.is_connected = True
        self.connector = reactor.connectTCP(self.hostname, 5222, factory)

    def __task_shutdown(self):
        """
            Checks for shutdown requests.
        """
        if not self.is_connected and reactor.running:
            try:
                reactor.stop()
            except:
                pass
            self.connector = None
            self.emit(QtCore.SIGNAL("stateChanged(int)"), Offline)

    def __event_connection_lost(self, rct, reason):
        """
            Event handler to be executed when connection is lost.
        """
        if self.is_connected:
            time.sleep(3)
            self.connector.connect()
            self.emit(QtCore.SIGNAL("stateChanged(int)"), Error)

    def __event_connection_failed(self, rct, reason):
        """
            Event handler to be executed when connection is failed.
        """
        if self.is_connected:
            time.sleep(3)
            self.connector.connect()
            self.emit(QtCore.SIGNAL("stateChanged(int)"), Error)

    def __event_session_start(self, stream):
        """
            Event handler to be executed when connection is made.
        """
        self.stream = stream

        # Update status
        presence = xish.domish.Element(('jabber:client','presence'))
        presence.addElement('status').addContent('Online')
        stream.send(presence)

        # Catch messages and status changes
        stream.addObserver('/message', self.__event_message)
        stream.addObserver('/presence', self.__event_presence)

        self.emit(QtCore.SIGNAL("stateChanged(int)"), Online)

    def __event_presence(self, presence):
        """
            Event handler to be executed when a status is changed.
        """

        if presence.getAttribute("type", None) == "subscribe":
            prs = xish.domish.Element(('jabber:client','presence'))
            prs["to"] = presence["from"]
            prs["type"] = "subscribed"
            self.stream.send(prs)

            prs = xish.domish.Element(('jabber:client','presence'))
            prs["to"] = presence["from"]
            prs["type"] = "subscribe"
            self.stream.send(prs)

        state = Offline
        if presence.getAttribute("type", "available") == "available":
            state = Online

        username = str(presence["from"]).split("@")[0].lower()
        if username == self.username:
            return
        if state == Online and username not in self.online:
            self.online.append(username)
        elif state == Offline and username in self.online:
            self.online.remove(username)

        self.emit(QtCore.SIGNAL("userStatusChanged(QString, int)"), QtCore.QString(username), state)

    def __event_message(self, message):
        """
            Event handler to be executed when a message is received.
        """
        for tag in message.elements():
            if tag.name == "body":
                username = str(message["from"]).split("@")[0].lower()
                try:
                    command, arguments = tag.__str__().split(" ", 1)
                except:
                    command = tag.__str__()
                    arguments = ""
                self.emit(QtCore.SIGNAL("messageFetched(QString, QString, QString)"), QtCore.QString(username), QtCore.QString(command), QtCore.QString(arguments))
                break

    def send_message(self, to, body):
        """
            Sends a message.

            Arguments:
                to: JID of recipient
                body: Message body
        """
        message = xish.domish.Element(('jabber:client','message'))
        message["to"] = to
        message["type"] = "chat"
        message.addElement("body", "jabber:client", body)
        self.stream.send(message)

    def send_command(self, to, command, arguments=None):
        """
            Replies to an RPC command.

            Arguments:
                to: JID of recipient
                command: Command name
                arguments: Arguments
        """
        if arguments:
            body = "%s %s" % (command, simplejson.dumps(arguments))
        else:
            body = command
        self.send_message(to, body)

    def disconnect(self):
        """
            Disconnects from XMPP server.
        """
        self.is_connected = False

    def run(self):
        """
            Runs TCP reactor when necessary.

            Waits until a connector is ready to use.
            TwistedMatrix magic happens here, RTFM.
        """
        while True:
            while not self.connector:
                time.sleep(0.5)
            reactor.run(installSignalHandlers=0)
