#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os
import xml.dom.minidom

from kdecore import KConfig

class Account:
    def __init__(self):
        self.accounts = []
    
    def getTBAccounts(self, path):
        "Imports Thunderbird accounts using prefs.js file in TB profile directory"
        prefsfile = os.path.join(path, "prefs.js")
        prefs = parsePrefs(prefsfile)
        # Get accounts:
        accounts = prefs["mail.accountmanager.accounts"]
        if accounts == "":
            accounts = []
        else:
            accounts = accounts.split(",")
        # Loop over accounts:
        for account in accounts:
            accountdict = {}
            account = account.strip()
            server = prefs["mail.account." + account + ".server"]
            servertype = prefs["mail.server." + server + ".type"]
            fields = {}
            # Define account types:
            if servertype == "pop3":
                accountdict["type"] = "POP3"
                fields = {"name":"name", "host":"hostname", "port":"port", "user":"userName", "SSL":"isSecure", "dir":"directory-rel"}
            elif servertype == "nntp":
                accountdict["type"] = "NNTP"
                fields = {"name":"name", "host":"hostname", "port":"port", "SSL":"isSecure", "dir":"directory-rel", "file":"newsrc.file-rel"}
            elif servertype == "imap":
                accountdict["type"] = "IMAP"
                fields = {"name":"name", "host":"hostname", "port":"port", "user":"userName", "SSL":"isSecure", "dir":"directory-rel"}
            # Get account information from TB prefs:
            for key in fields.keys():
                field = "mail.server." + server + "." + fields[key]
                accountdict[key] = prefs.get(field, None)
            # Add new account:
            if accountdict:
                self.accounts.append(accountdict)
        # Get SMTP accounts:
        accounts = prefs["mail.smtpservers"]
        if accounts == "":
            accounts = []
        else:
            accounts = accounts.split(",")
        # Loop over SMTP accounts
        for account in accounts:
            accountdict = {}
            accountdict["type"] = "SMTP"
            account = account.strip()
            fields = {"host":"hostname", "port":"port", "user":"username", "Try SSL":"try_ssl"}
            # Get account information from TB prefs:
            for key in fields.keys():
                field = "mail.smtpserver." + account + "." + fields[key]
                accountdict[key] = prefs.get(field, None)
            # Add new accounts:
            if accountdict:
                self.accounts.append(accountdict)
    
    def getMSNAccounts(self, path):
        "Imports MSN accounts using windows users's 'Contacts' directory"
        files = os.listdir(path)
        for item in files:
            if os.path.isdir(os.path.join(path, item)):
                accountdict = {"type":"MSN", "mail":item}
                self.accounts.append(accountdict)
    
    def getGTalkAccounts(self, key):
        "Imports GTalk accounts using Windows registry key"
        # Open registry key of GTalk:
        key = key.getSubKey("Accounts")
        for account in key.subKeys():
            accountdict = {}
            accountdict["type"] = "Jabber"
            accountdict["user"] = account
            accountkey = key.getSubKey(account)
            accountdict["host"] = accountkey.getValue("px")
            accountdict["port"] = accountkey.getValue("pt")
            accountdict["SSL"] = True
            self.accounts.append(accountdict)
    
    def getOEAccounts(self, oepath):
        "Imports Outlook Express accounts using OE directory"
        for item in os.listdir(oepath):
            path = os.path.join(oepath, item)
            if os.path.isdir(path):
                for item2 in os.listdir(path):
                    if os.path.splitext(item2)[1] == ".oeaccount":      # Hey, I found an account file :)
                        path = os.path.join(path, item2)
                        dom = xml.dom.minidom.parse(path)
                        accountdict = {}
                        if getData(dom, "NNTP_Server"):
                            accountdict["type"] = "NNTP"
                            fields = {"name":"Account_Name", "host":"NNTP_Server", "realname":"NNTP_Display_Name", "email":"NNTP_Email_Address"}
                        elif getData(dom, "POP3_Server"):
                            accountdict["type"] = "POP3"
                            fields = {"name":"Account_Name", "host":"POP3_Server", "port":"POP3_Port", "user":"POP3_User_Name", "SSL":"POP3_Secure_Connection"}
                        elif getData(dom, "IMAP_Server"):
                            accountdict["type"] = "IMAP"
                            fields = {"name":"Account_Name", "host":"IMAP_Server", "port":"IMAP_Port", "user":"IMAP_User_Name", "SSL":"IMAP_Secure_Connection"}
                        for key in fields.keys():
                            value = getData(dom, fields[key])
                            if value:
                                accountdict[key] = value
                        # Add Account:
                        if accountdict:
                            self.accounts.append(accountdict)
                        # Get SMTP
                        accountdict = {}
                        fields = {}
                        if getData(dom, "SMTP_Server"):
                            accountdict["type"] = "SMTP"
                            fields = {"host":"SMTP_Server", "port":"SMTP_Port", "SSL":"SMTP_Secure_Connection", "realname":"SMTP_Display_Name", "email":"SMTP_Email_Address"}
                        for key in fields.keys():
                            value = getData(dom, fields[key])
                            if value:
                                accountdict[key] = value
                        # Add SMTP
                        if accountdict:
                            self.accounts.append(accountdict)
    
    def setKopeteAccounts(self):
        config = KConfig("kopeterc")
        for account in self.accounts:
            if account["type"] == "Jabber":
                groupname = "Account_JabberProtocol_" + account["user"]
                if not config.hasGroup(groupname):
                    config.setGroup(groupname)
                    config.writeEntry("AccountId", account["user"])
                    config.writeEntry("Protocol", "JabberProtocol")
                    config.writeEntry("CustomServer", "true")
                    config.writeEntry("Server", account["host"])
                    config.writeEntry("Port", account["port"])
                    if account["SSL"]:
                        config.writeEntry("UseSSL", "true")
            elif account["type"] == "MSN":
                groupname = "Account_MSNProtocol_" + account["user"]
                if not config.hasGroup(groupname):
                    config.setGroup(groupname)
                    config.writeEntry("AccountId", account["user"])
                    config.writeEntry("Protocol", "MSNProtocol")
                    config.writeEntry("serverName", account["host"])
                    config.writeEntry("serverPort", account["port"])
        config.sync()
    
    def yaz(self):
        "Prints accounts"
        for account in self.accounts:
            print account["type"]
            for key in account.keys():
                if key != "type":
                    print "%10s : %s" % (key, account[key])

def parsePrefs(filepath):
    "Parses Thunderbird's prefs.js file and returns it as a dictionary"
    preffile = open(filepath)
    text = preffile.read()
    preffile.close()
    # Delete comments:
    start = text.find("/")
    while 0 <= start < (len(text) - 1):
        if text[start + 1] == "*":
            end = text.find("*/", start + 2)
            end += 1        # */ iki karakter
        elif text[start + 1] == "/":
            end = text.find("\n", start + 2)
        else:
            start = text.find("/", start + 1)
            continue
        if end < 0 or end >= (len(text) - 1):
            text = text[:start]       # sonuna kadar sil
        else:
            text = text[:start] + text[(end + 1):]
        start = text.find("/", start + 1)
    # Get Options:
    prefs = {}
    lines = text.split("user_pref(\"")
    for line in lines:
        pieces = line.split("\"")
        if len(pieces) == 4:
            key = pieces[0]
            value = pieces[2]
            prefs[key] = value
        elif len(pieces) == 2:
            key = pieces[0]
            value = pieces[1].strip(", ();\n\t")
            prefs[key] = value
    return prefs

def getData(dom, tagname):
    "Gets data from a DOM's 'tagname' named children"
    data = ""
    elements = dom.getElementsByTagName(tagname)
    if elements:
        element = elements[0]
    else:
        return ""
    for node in element.childNodes:
        if node.nodeType == node.TEXT_NODE:
            data += node.data
    if element.getAttribute("type") == "DWORD":
        data = int(data, 16)
    return data

