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
import tempfile
import xml.dom.minidom

from qt import QString
from kdecore import KConfig, i18n
from dcopext import DCOPClient, DCOPObj

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
                    if not os.path.isdir(path):
                        return
                    for itemname in os.listdir(path):
                        itempath = os.path.join(path, itemname)
                        if os.path.splitext(itemname)[1] == ".msf" and os.path.isfile(itempath):
                            mboxpath = os.path.splitext(itempath)[0]
                            mboxname = os.path.join(name, os.path.basename(mboxpath))
                            if (mboxname, mboxpath) not in self.folders:
                                self.folders.append((mboxname, mboxpath))
                        elif os.path.splitext(itemname)[1] == ".sbd" and os.path.isdir(itempath):
                            addFolders(os.path.join(name, os.path.splitext(itemname)[0]), itempath)
                if (foldername, "") not in self.folders:
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
            # Correct real hostname and real username:
            realhost = prefs.get("mail.server." + server + ".realhostname", None)
            if realhost:
                accountdict["host"] = realhost
            realuser = prefs.get("mail.server." + server + ".realuserName", None)
            if realuser:
                accountdict["user"] = realuser
            # Correct paths:
            if accountdict.has_key("dir"):
                accountdict["dir"] = os.path.join(path, accountdict["dir"].replace("[ProfD]", ""))
            if accountdict.has_key("file"):
                accountdict["file"] = os.path.join(path, accountdict["file"].replace("[ProfD]", ""))
            # Correct values:
            if accountdict.has_key("SSL"):
                if accountdict["SSL"]:
                    accountdict["SSL"] = True
                else:
                    accountdict["SSL"] = False
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
                        accountpath = os.path.join(path, item2)
                        dom = xml.dom.minidom.parse(accountpath)
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
                        accountdict["inbox"] = os.path.join(accountdict["name"], "Inbox")
                        # Add Account:
                        if accountdict:
                            self.accounts.append(accountdict)
                        # Get Folders:
                        if accountdict.get("type", None) == "POP3":
                            foldername = accountdict.get("name", "")
                            self.folders.extend(getOEFolders(path, foldername))
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
                inbox = account.get("inbox", "inbox")
                folder = KMailFolderName(inbox)
                config.writeEntry("Folder", folder)
                # Create inbox if not exists:
                folders = inbox.split("/")
                for i in xrange(len(folders)):
                    foldername = "/".join(folders[:(i + 1)])
                    foldername = KMailFolderName(foldername)
                    folderpath = os.path.expanduser("~/.kde/share/apps/kmail/mail/" + foldername)
                    if not os.path.exists(folderpath):
                        os.makedirs(folderpath)
                        os.makedirs(os.path.join(folderpath, "cur"))
                        os.makedirs(os.path.join(folderpath, "new"))
                        os.makedirs(os.path.join(folderpath, "tmp"))
                
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
    
    def addKMailMessages(self, progress=None):
        # Information message:
        infomessagepath = os.path.join(tempfile.gettempdir(), "temp_kmail_info.eml")
        message = "From:pardus@localhost\r\nSubject:%s\r\n\r\n%s" % (i18n("Migrated Folder"), i18n("This messagebox is migrated using Pardus Migration Tool"))
        messagefile = open(infomessagepath, "w")
        messagefile.write(message)
        messagefile.close()
        kmail = ConnectKMail()
        # Loop over folders:
        for (name, path) in self.folders[2:]:
            # Add Info Message:
            #addMessage(name, infomessagepath, kmail)
            # Chech Message Box Type
            if os.path.isfile(path):
                # Copy mbox:
                box = mbox(path)
                boxsize = os.path.getsize(path)
                totalsize = 0
                messagepath = box.next()
                while messagepath:
                    try:
                        addMessage(name, messagepath, kmail)
                    except DuplicateMessage, text:
                        totalsize += os.path.getsize(messagepath)
                        progress.go(None, progress.OK, os.path.getsize(messagepath))
                    except DCOPError, text:
                        progress.go(text, progress.WARNING, 0)
                        kmail = ConnectKMail()
                        continue
                    except MailError, text:
                        totalsize += os.path.getsize(messagepath)
                        progress.go(text, progress.WARNING, os.path.getsize(messagepath))
                    else:
                        totalsize += os.path.getsize(messagepath)
                        progress.go(None, progress.OK, os.path.getsize(messagepath))
                    messagepath = box.next()
                progress.go(unicode(i18n("Message Box %s copied")) % name, progress.OK, boxsize - totalsize)
            elif os.path.isdir(path) and os.path.isfile(os.path.join(path, "winmail.fol")):
                # Copy OE messagebox
                box = oebox(path)
                messagepath = box.next()
                while messagepath:
                    try:
                        addMessage(name, messagepath, kmail)
                    except DuplicateMessage, text:
                        progress.go(None, progress.OK, os.path.getsize(messagepath))
                    except DCOPError, text:
                        progress.go(text, progress.WARNING, 0)
                        kmail = ConnectKMail()
                        continue
                    except MailError, text:
                        progress.go(text, progress.WARNING, os.path.getsize(messagepath))
                    else:
                        progress.go(None, progress.OK, os.path.getsize(messagepath))
                    messagepath = box.next()
                progress.go(unicode(i18n("Message Box %s copied")) % name, progress.OK, 0)

    
    def setKNodeAccounts(self):
        for account in self.accounts:
            if account["type"] == "NNTP":
                files = os.listdir(os.path.expanduser("~/.kde/share/apps/knode"))
                accountid = 1
                while "nntp." + str(accountid) in files:
                    accountid += 1
                dirname = os.path.expanduser("~/.kde/share/apps/knode/nntp." + str(accountid))
                os.mkdir(dirname)
                infofile = open(os.path.join(dirname, "info"), "w")
                infofile.write("id=%d\n" % accountid)
                fields = {"host":"server", "name":"name", "email":"Email", "realname":"Name", "port":"port"}
                for key in fields.keys():
                    value = account.get(key, None)
                    if value:
                        infofile.write("%s=%s\n" % (fields[key], value))
                infofile.close()
    
    def yaz(self):
        "Prints accounts"
        for account in self.accounts:
            print account["type"]
            for key in account.keys():
                if key not in ["type", "folders"]:
                    print "%15s : %s" % (key, account[key])
        for folder in self.folders:
            print "%30s : %s" % folder
    
    def accountSize(self, accounttypes=None):
        "Size of accounts"
        if not accounttypes:
            return len(self.accounts) * 500
        else:
            number = 0
            for account in self.accounts:
                if account.get("type", None) in accounttypes:
                    number += 1
            return number * 500
    
    def mailSize(self):
        totalsize = 0
        for (name, path) in self.folders:
            # is empty folder?
            if not path:
                continue
            # is mbox file?
            if os.path.isfile(path):
                totalsize += os.path.getsize(path)
            elif os.path.isdir(path):
                # is OE folder?
                if os.path.isfile(os.path.join(path, "winmail.fol")):
                    for item in os.listdir(path):
                        if os.path.splitext(item)[1] == ".eml":
                            totalsize += os.path.getsize(os.path.join(path, item))
                # is maildir folder?
                elif os.path.isdir(os.path.join(path, "new")) and os.path.isdir(os.path.join(path, "cur")):
                    for item in os.listdir(os.path.join(path, "new")):
                        totalsize += os.path.getsize(os.path.join(path, "new", item))
                    for item in os.listdir(os.path.join(path, "new")):
                        totalsize += os.path.getsize(os.path.join(path, "new", item))
        return totalsize


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


def getOEFolders(path, relative=""):
    "Returns OE mailbox folders under a path"
    folders = []
    # Get Sub Dirs:
    for item in os.listdir(path):
        itempath = os.path.join(path, item)
        # Here is a directory. Is it a mailbox?
        if os.path.isdir(itempath) and os.path.isfile(os.path.join(itempath, "winmail.fol")):
            foldername = os.path.join(relative, item)
            folders.append((foldername, itempath))
            folders.extend(getOEFolders(itempath, foldername))
    return folders


class mbox:
    "Class to handle unix mailbox format mbox (mailbox.UnixMailbox is not stable)"
    def __init__(self, path):
        "Opens mbox file and initilizes class"
        self.mboxfile = open(path)
        self.mboxfile.readline()
    def next(self):
        "Iterates messages"
        message = ""
        emptylines = 0
        line = self.mboxfile.readline()
        while line and line[:5] != "From ":
            message += line
            line = self.mboxfile.readline()
        # Create a temporary message file:
        if message != "":
            messagepath = os.path.join(tempfile.gettempdir(), "temp_mbox_mail.eml")
            messagefile = open(messagepath, "w")
            messagefile.write(message)
            messagefile.close()
            return messagepath
        else:
            return None


class oebox:
    "Class to handle Outlook Express messagebox format"
    def __init__(self, path):
        "Opens messagebox directory and initilizes class"
        self.path = path
        self.messages = os.listdir(path)
        self.messages = filter(lambda x: os.path.splitext(x)[1] == ".eml", self.messages)
        self.index = 0
    def next(self):
        "Iterates messages"
        if len(self.messages) <= self.index:
            return None
        messagepath = os.path.join(self.path, self.messages[self.index])
        self.index += 1
        return messagepath


def ConnectKMail():
    # Run KMail:
    if not os.system("kmail") == 0:
        raise Exception, "KMail cannot be started"
    # Create a dcop object:
    client = DCOPClient()
    if not client.attach():
        raise Exception, "Cannot connected to KMail"
    # Keep this window on top:
    kmail = DCOPObj("kmail", client, "kmail-mainwindow#1")
    kmail.lower()
    # Return KMailIface
    kmail = DCOPObj("kmail", client, "KMailIface")
    return kmail


def addMessage(folder, message, kmail=None):
    "Adds a message to kmail with dcop interface"
    if not kmail:
        # Create a dcop object:
        client = DCOPClient()
        if not client.attach():
            raise Exception, "Message cannot be added"
        kmail = DCOPObj("kmail", client, "KMailIface")
    # Add Message:
    ok, status = kmail.dcopAddMessage(QString(folder), message, "")
    if not ok:
        raise DCOPError, "Can not connect to kmail with DCOP"
    elif status == -4:
        raise DuplicateMessage, "Message in %s cannot be added: duplicate message" % folder
    elif status == -2:
        raise MailError, "Message in %s cannot be added: cannot add message to folder" % folder
    elif status == -1:
        raise MailError, "Message in %s cannot be added: cannot make folder" % folder
    elif status == 0:
        raise MailError, "Message in %s cannot be added: error while adding message" % folder
    elif status != 1:
        raise MailError, "Message in %s cannot be added, status: %d" % (folder, status)
    else:
        return True


class DCOPError(Exception):
    pass

class MailError(Exception):
    pass

class DuplicateMessage(Exception):
    pass

