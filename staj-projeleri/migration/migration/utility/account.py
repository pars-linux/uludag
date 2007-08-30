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
        self.folders = []
    
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
                fields = {"name":"name", "host":"hostname", "port":"port", "user":"userName", "SSL":"isSecure"}
                # Get folder name and path:
                field = "mail.server." + server + ".defer_get_new_mail"
                if prefs.get(field, False):     # Using Local Folders
                    field = "mail.server." + server + ".deferred_to_account"
                    realaccount = prefs.get(field, account)
                    realserver = prefs["mail.account." + realaccount + ".server"]
                else:       # Using its own folder
                    realserver = server
                foldername = prefs["mail.server." + realserver + ".name"]
                folderpath = os.path.join(path, prefs["mail.server." + realserver + ".directory-rel"].replace("[ProfD]", ""))
                # Add message boxes in this account:
                def addFolders(name, path):
                    for itemname in os.listdir(path):
                        itempath = os.path.join(path, itemname)
                        if os.path.splitext(itemname)[1] == ".msf" and os.path.isfile(itempath):
                            mboxpath = os.path.splitext(itempath)[0]
                            mboxname = os.path.join(name, os.path.basename(mboxpath))
                            if (mboxname, mboxpath) not in self.folders:
                                self.folders.append((mboxname, mboxpath))
                        elif os.path.splitext(itemname)[1] == ".sbd" and os.path.isdir(itempath):
                            addFolders(os.path.join(name, os.path.splitext(itemname)[0]), itempath)
                self.folders.append((foldername, ""))
                addFolders(foldername, folderpath)
                accountdict["inbox"] = os.path.join(foldername, "Inbox")
            elif servertype == "nntp":
                accountdict["type"] = "NNTP"
                fields = {"name":"name", "host":"hostname", "port":"port", "SSL":"isSecure", "dir":"directory-rel", "file":"newsrc.file-rel"}
            elif servertype == "imap":
                accountdict["type"] = "IMAP"
                fields = {"name":"name", "host":"hostname", "port":"port", "user":"userName", "SSL":"isSecure", "dir":"directory-rel"}
            elif servertype == "rss":
                accountdict["type"] = "RSS"
                fields = {"name":"name", "dir":"directory-rel"}
            # Get account information from TB prefs:
            for key in fields.keys():
                field = "mail.server." + server + "." + fields[key]
                accountdict[key] = prefs.get(field, None)
            # Correct values:
            if accountdict.has_key("dir"):
                accountdict["dir"] = accountdict["dir"].replace("[ProfD]", path)
            if accountdict.has_key("file"):
                accountdict["file"] = accountdict["file"].replace("[ProfD]", path)
            if accountdict.has_key("SSL"):
                if accountdict["SSL"]:
                    accountdict["SSL"] = True
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
            fields = {"host":"hostname", "port":"port", "secure":"try_ssl"}
            # Get account information from TB prefs:
            for key in fields.keys():
                field = "mail.smtpserver." + account + "." + fields[key]
                accountdict[key] = prefs.get(field, None)
            if prefs.get("mail.smtpserver." + account + ".auth_method", 0):
                accountdict["auth"] = True
                accountdict["user"] = prefs.get("mail.smtpserver." + account + ".username", None)
            else:
                accountdict["auth"] = False
            # Correct values:
            if accountdict.has_key("secure"):
                accountdict["SSL"] = False
                accountdict["TLS"] = False
                if accountdict["secure"] in ["1", "2"]:
                    accountdict["TLS"] = True
                elif accountdict["secure"] == "3":
                    accountdict["SSL"] = True
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
                            sicility = int(getData(dom, "SMTP_Use_Sicily"))
                            if sicility == 0:
                                accountdict["auth"] = False
                            elif sicility == 1:
                                accountdict["auth"] = True
                                accountdict["user"] = getData(dom, "SMTP_User_Name")
                            elif sicility == 2:
                                if getData(dom, "POP3_User_Name"):
                                    accountdict["auth"] = True
                                    accountdict["user"] = getData(dom, "POP3_User_Name")
                                elif getData(dom, "IMAP_User_Name"):
                                    accountdict["auth"] = True
                                    accountdict["user"] = getData(dom, "IMAP_User_Name")
                            elif sicility == 3:
                                accountdict["auth"] = True
                                accountdict["user"] = getData(dom, "SMTP_User_Name")
                            fields = {"host":"SMTP_Server", "port":"SMTP_Port", "SSL":"SMTP_Secure_Connection", "realname":"SMTP_Display_Name", "email":"SMTP_Email_Address"}
                        for key in fields.keys():
                            value = getData(dom, fields[key])
                            if value:
                                accountdict[key] = value
                        # Add SMTP
                        if accountdict:
                            self.accounts.append(accountdict)
    
    def setKopeteAccounts(self):
        "Add imported accounts into Kopete"
        config = KConfig("kopeterc")
        for account in self.accounts:
            if account["type"] == "Jabber":
                groupname = "Account_JabberProtocol_" + account["user"]
                if not config.hasGroup(groupname):
                    config.setGroup("Plugins")
                    config.writeEntry("kopete_jabberEnabled", "true")
                    config.setGroup(groupname)
                    config.writeEntry("AccountId", account["user"])
                    config.writeEntry("Protocol", "JabberProtocol")
                    config.writeEntry("CustomServer", "true")
                    config.writeEntry("Server", account["host"])
                    config.writeEntry("Port", account["port"])
                    if account["SSL"]:
                        config.writeEntry("UseSSL", "true")
            elif account["type"] == "MSN":
                groupname = "Account_MSNProtocol_" + account["mail"]
                if not config.hasGroup(groupname):
                    config.setGroup("Plugins")
                    config.writeEntry("kopete_msnEnabled", "true")
                    config.setGroup(groupname)
                    config.writeEntry("AccountId", account["mail"])
                    config.writeEntry("Protocol", "MSNProtocol")
                    config.writeEntry("serverName", "messenger.hotmail.com")
                    config.writeEntry("serverPort", 1863)
        config.sync()
    
    def setKMailAccounts(self):
        "Add imported accounts into Kopete"
        config = KConfig("kmailrc")
        config.setGroup("General")
        accountno = config.readNumEntry("accounts") + 1
        config.setGroup("General")
        transportno = config.readNumEntry("transports") + 1
        for account in self.accounts:
            if not KMailAccountIsValid(config, account):
                continue
            # Add POP3 Account:
            if account["type"] == "POP3":
                config.setGroup("General")
                config.writeEntry("accounts", accountno)
                config.setGroup("Account " + str(accountno))
                accountno += 1
                config.writeEntry("trash", "trash")
                config.writeEntry("Type", "pop")
                config.writeEntry("Name", account["name"])
                config.writeEntry("auth", "USER")
                config.writeEntry("host", account["host"])
                config.writeEntry("login", account["user"])
                
                # Set Inbox Folder:
                #inbox = account.get("inbox", "inbox")
                #inbox = KMailFolderName(inbox)
                inbox = "inbox"
                config.writeEntry("Folder", inbox)
                
                if account.has_key("SSL") and account["SSL"]:
                    config.writeEntry("use-ssl", "true")
                    config.writeEntry("port", 995)
                else:
                    config.writeEntry("use-ssl", "false")
                    config.writeEntry("port", 110)
                if account.has_key("port") and account["port"]:
                    config.writeEntry("port", account["port"])
                config.writeEntry("use-tls", "false")
            # Add IMAP Account:
            elif account["type"] == "IMAP":
                config.setGroup("General")
                config.writeEntry("accounts", accountno)
                config.setGroup("Account " + str(accountno))
                accountno += 1
                config.writeEntry("Folder", "")
                config.writeEntry("trash", "trash")
                config.writeEntry("Type", "imap")
                config.writeEntry("Name", account["name"])
                config.writeEntry("auth", "*")
                config.writeEntry("host", account["host"])
                config.writeEntry("login", account["user"])
                if account.has_key("SSL") and account["SSL"]:
                    config.writeEntry("use-ssl", "true")
                    config.writeEntry("port", 993)
                else:
                    config.writeEntry("use-ssl", "false")
                    config.writeEntry("port", 143)
                if account.has_key("port") and account["port"]:
                    config.writeEntry("port", account["port"])
                config.writeEntry("use-tls", "false")
            # Add SMTP Account:
            elif account["type"] == "SMTP":
                config.setGroup("General")
                config.writeEntry("transports", transportno)
                config.setGroup("Transport " + str(transportno))
                transportno += 1
                if account.get("auth", False) and account.has_key("user"):
                    config.writeEntry("auth", "true")
                    config.writeEntry("authtype", "PLAIN")
                    config.writeEntry("user", account["user"])
                config.writeEntry("name", account["host"])
                config.writeEntry("host", account["host"])
                if account.has_key("SSL") and account["SSL"]:
                    config.writeEntry("encryption", "SSL")
                    config.writeEntry("port", 465)
                else:
                    config.writeEntry("port", 25)
                    if account.has_key("TLS") and account["TLS"]:
                        config.writeEntry("encryption", "TLS")
                if account.has_key("port") and account["port"]:
                    config.writeEntry("port", account["port"])
            config.sync()
        
        ## Add missing directories and mbox files:
        #for folder in self.folders:
            #name = folder[0]
            #path = KMailFolderName(name)
            #path = os.path.join(os.path.expanduser("~/.kde/share/apps/kmail/mail"), path)
            #if not os.path.exists(path):
                #dirpath = os.path.dirname(path)
                #if not os.path.isdir(dirpath):
                    #os.makedirs(dirpath)
                #open(path, "w").close()
    
    def yaz(self):
        "Prints accounts"
        for account in self.accounts:
            print account["type"]
            for key in account.keys():
                if key not in ["type", "folders"]:
                    print "%15s : %s" % (key, account[key])
        for folder in self.folders:
            print "%30s : %s" % folder

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
            value = pieces[1].strip(",(); \r\n\t")
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

def KMailFolderName(folder):
    "Returns KMail folder name of given folder. (GMail/Inbox -> .GMail.directory/Inbox)"
    path = folder.split("/")
    for i in xrange(0, len(path) - 1):
        path[i] = "." + path[i] + ".directory"
    folder = "/".join(path)
    return folder

def KMailAccountExists(config, type1, host1, user1):
    found = False
    oldgroup = config.group()
    config.setGroup("General")
    accounts = config.readNumEntry("accounts")
    for account in xrange(1, accounts + 1):
        config.setGroup("Account " + str(account))
        type2 = config.readEntry("Type")
        host2 = config.readEntry("host")
        user2 = config.readEntry("login")
        if type1 == type2 and host1 == host2 and user1 == user2:
            found = True
            break
    config.setGroup(oldgroup)
    return found

def KMailAccountIsValid(config, account1):
    "Check if the account is valid and not already in KMail accounts"
    if (not account1.has_key("type")) or (not account1.has_key("host")) or (not account1.has_key("user")):
        return False
    if account1["type"] in ["POP3", "IMAP"]:
        config.setGroup("General")
        accounts = config.readNumEntry("accounts")
    elif account1["type"] == "SMTP":
        config.setGroup("General")
        accounts = config.readNumEntry("transports")
    else:
        return False
    # Check all accounts 
    for account2 in xrange(1, accounts + 1):
        if account1["type"] == "SMTP":
            config.setGroup("Transport " + str(account2))
            host2 = config.readEntry("host")
            user2 = config.readEntry("user")
            if account1["host"] == host2 and account1["user"] == user2:
                return False
        elif account1["type"] == "POP3":
            config.setGroup("Account " + str(account2))
            type2 = config.readEntry("Type")
            host2 = config.readEntry("host")
            user2 = config.readEntry("login")
            if "pop" == type2 and account1["host"] == host2 and account1["user"] == user2:
                return False
        elif account1["type"] == "IMAP":
            config.setGroup("Account " + str(account2))
            type2 = config.readEntry("Type")
            host2 = config.readEntry("host")
            user2 = config.readEntry("login")
            if "imap" == type2 and account1["host"] == host2 and account1["user"] == user2:
                return False
    return True

def KMailTransportExists(config, host1, user1):
    found = False
    oldgroup = config.group()
    config.setGroup("General")
    accounts = config.readNumEntry("transports")
    for account in xrange(1, accounts + 1):
        config.setGroup("Transport " + str(account))
        host2 = config.readEntry("host")
        user2 = config.readEntry("user")
        if host1 == host2 and user1 == user2:
            found = True
            break
    config.setGroup(oldgroup)
    return found

