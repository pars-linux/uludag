#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


import os
import tempfile
import xml.dom.minidom
from PyKDE4.kdecore import KConfig, KConfigGroup, i18n
from dbus import *

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
                    pluginsGroup = config.group("Plugins")
                    pluginsGroup.writeEntry("kopete_jabberEnabled", "true")
                    accountGroup = config.group(groupname)
                    accountGroup.writeEntry("AccountId", account["user"])
                    accountGroup.writeEntry("Protocol", "JabberProtocol")
                    accountGroup.writeEntry("CustomServer", "true")
                    accountGroup.writeEntry("Server", account["host"])
                    accountGroup.writeEntry("Port", account["port"])
                    if account["SSL"]:
                        accountGroup.writeEntry("UseSSL", "true")
            elif account["type"] == "MSN":
                groupname = "Account_MSNProtocol_" + account["mail"]
                if not config.hasGroup(groupname):
                    pluginsGroup = config.group("Plugins")
                    pluginsGroup.writeEntry("kopete_msnEnabled", "true")
                    accountGroup = config.group(groupname)
                    accountGroup.writeEntry("AccountId", account["mail"])
                    accountGroup.writeEntry("Protocol", "MSNProtocol")
                    accountGroup.writeEntry("serverName", "messenger.hotmail.com")
                    accountGroup.writeEntry("serverPort", 1863)
        config.sync()

    def setKMailAccounts(self):
        """Add imported accounts into Kmail"""

        #Set default config and configGroup
        config = KConfig("kmailrc")
        newAccountGroup = config.group("Account")
        configGroup = KConfigGroup(newAccountGroup)

        def getResourceConfigGroup(account):
            """Get Resource Config Groups for account type"""

            accountGroups = []
            if account["type"] =="SMTP":
                config = KConfig("mailtransports")
                generalGroup = config.group("General")
                defaultAccount = group.readEntry("default-transport")
                print "defaultSMTPAccount:%d" % defaultAccount
                transportGroup = config("Transport %s") % defaultAccount
                accountGroups.append(transportGroup)
            elif account["type"] == "POP3":
                config = KConfig("kmailrc")
                for each in list(config.groupList()):
                    if each.contains("Account") and not each.endWith("Wizard"):
                        accountGroups.append(each)
            return accountGroups

        for account in self.accounts:
            # Add POP3 Account:
            if account["type"] == "POP3":
                for accountGroup in getResourceConfigGroup(account):
                    if not isKMailAccountValid(accountGroup, account):
                        continue
                    configGroup.writeEntry("trash", "trash")
                    configGroup.writeEntry("Type", "Pop")
                    configGroup.writeEntry("Name", account["name"])
                    configGroup.writeEntry("auth", "USER")
                    configGroup.writeEntry("host", account["host"])
                    configGroup.writeEntry("login", account["user"])

                    # Set Inbox Folder:
                    inbox = account.get("inbox", "inbox")
                    folder = kMailFolderName(inbox)
                    configGroup.writeEntry("Folder", folder)

                    # Create inbox if not exists:
                    folders = inbox.split("/")
                    for i in xrange(len(folders)):
                        foldername = "/".join(folders[:(i + 1)])
                        foldername = kMailFolderName(foldername)
                        folderpath = os.path.expanduser("~/.kde/share/apps/kmail/mail/" + foldername)
                        if not os.path.exists(folderpath):
                            os.makedirs(folderpath)
                            os.makedirs(os.path.join(folderpath, "cur"))
                            os.makedirs(os.path.join(folderpath, "new"))
                            os.makedirs(os.path.join(folderpath, "tmp"))

                    if account.has_key("SSL") and account["SSL"]:
                        configGroup.writeEntry("use-ssl", "true")
                        configGroup.writeEntry("port", 995)
                    else:
                        configGroup.writeEntry("use-ssl", "false")
                        configGroup.writeEntry("port", 110)

                    if account.has_key("port") and account["port"]:
                        configGroup.writeEntry("port", account["port"])

                    configGroup.writeEntry("use-tls", "false")

            # Add IMAP Account:
            elif account["type"] == "IMAP":
                accountGroup = getResourceConfigGroup(account)
                if not isKMailAccountValid(accountGroup, account):
                    return

                configGroup.writeEntry("Folder", "")
                configGroup.writeEntry("trash", "trash")
                configGroup.writeEntry("Type", "Pop")
                configGroup.writeEntry("Name", account["name"])
                configGroup.writeEntry("auth", "USER")
                configGroup.writeEntry("host", account["host"])
                configGroup.writeEntry("login", account["user"])

                if account.has_key("SSL") and account["SSL"]:
                    configGroup.writeEntry("use-ssl", "true")
                    configGroup.writeEntry("port", 993)
                else:
                    configGroup.writeEntry("use-ssl", "false")
                    configGroup.writeEntry("port", 143)
                if account.has_key("port") and account["port"]:
                    configGroup.writeEntry("port", account["port"])
                configGroup.writeEntry("use-tls", "false")

            # Add SMTP Account:
            elif account["type"] == "SMTP":
                accountGroup = getResourceConfigGroup(account)
                if not isKMailAccountValid(accountGroup, account):
                    return

                config = KConfig("mailports")
                configGroup = config.group("Transport")
                configGroup = KConfigGroup(configGroup)

                if account.get("auth", False) and account.has_key("user"):
                    configGroup.writeEntry("auth", "true")
                    configGroup.writeEntry("authtype", "PLAIN")
                    configGroup.writeEntry("user", account["user"])

                configGroup.writeEntry("name", account["host"])
                configGroup.writeEntry("host", account["host"])

                if account.has_key("SSL") and account["SSL"]:
                    configGroup.writeEntry("encryption", "SSL")
                    configGroup.writeEntry("port", 465)
                else:
                    configGroup.writeEntry("port", 25)
                    if account.has_key("TLS") and account["TLS"]:
                        configGroup.writeEntry("encryption", "TLS")
                if account.has_key("port") and account["port"]:
                    configGroup.writeEntry("port", account["port"])

            configGroup.sync()

    def addKMailMessages(self, progress=None):
        # Information message:
        infomessagepath = os.path.join(tempfile.gettempdir(), "temp_kmail_info.eml")
        message = "From:pardus@localhost\r\nSubject:%s\r\n\r\n%s" % (i18n("Migrated Folder"), i18n("This messagebox is migrated using Pardus Migration Tool"))
        messagefile = open(infomessagepath, "w")
        messagefile.write(message)
        messagefile.close()
        kmail = connectKMail()
        # Loop over folders:
        for (name, path) in self.folders[2:]:
            # Add Info Message:
            #addMessage(name, infomessagepath, kmail)
            # Chech Message Box Type
            if os.path.isfile(path):
                # Copy mbox:
                box = MBox(path)
                boxsize = os.path.getsize(path)
                totalsize = 0
                messagepath = box.next()
                while messagepath:
                    try:
                        addMessage(name, messagepath, kmail)
                    except DuplicateMessage, text:
                        totalsize += os.path.getsize(messagepath)
                        progress.go(None, progress.OK, os.path.getsize(messagepath))
                    except DBUSError, text:
                        progress.go(text, progress.WARNING, 0)
                        kmail = connectKMail()
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
                box = OutlookExpressBox(path)
                messagepath = box.next()
                while messagepath:
                    try:
                        addMessage(name, messagepath, kmail)
                    except DuplicateMessage, text:
                        progress.go(None, progress.OK, os.path.getsize(messagepath))
                    except DBusException, text:
                        progress.go(text, progress.WARNING, 0)
                        kmail = connectKMail()
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

    def write(self):
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


def kMailFolderName(folder):
    "Returns KMail folder name of given folder. (GMail/Inbox -> .GMail.directory/Inbox)"
    path = folder.split("/")
    for i in xrange(0, len(path) - 1):
        path[i] = "." + path[i] + ".directory"
    folder = "/".join(path)
    return folder


def isKMailAccountValid(group, account):
    "Check if the account is valid and not already in KMail accounts"
    print "group%s" % group
    print "account[\"type\"]:%s" % account["type"]

    if len(group) == 0:
        return False

    if (not account.has_key("type")) or (not account.has_key("host")) or (not account.has_key("user")):
        return False

    # Check all accounts
    if account["type"] == "SMTP":
        host = group.readEntry("host")
        print "smptp.host%s" % host
        user = group.readEntry("user")
        print "smtp.user:%s" % user
        if account["host"] == host and account["user"] == user:
            return False
    elif account["type"] == "POP3":
        type = group.readEntry("Type")
        host = group.readEntry("host")
        print "pop.host:%s" % host
        user = group.readEntry("login")
        print "pop.user:%s" % user
        if "Pop" == type and account["host"] == host and account[login] == user:
            return False
    elif account["type"] == "IMAP":
        type = group.readEntry("Type")
        host = group.readEntry("host")
        print "imap.host:%s" % host
        user = group.readEntry("login")
        print "imap.user:%s" % user
        if ("Imap" == type or "DImap" == type) and account["host"] == host and account["login"] == user:
            return False
    return True

def getOutlookExpressFolders(path, relative=""):
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


class MBox:
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


class OutlookExpressBox:
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


def connectKMail():
    # Run KMail:
    if not os.system("kmail") == 0:
        raise Exception, "KMail cannot be started"
    # Create a dbus object:
    bus = dbus.SessionBus()
    kmail =  bus.get_object('org.kde.kmail', '/KMail', 'org.kde.kmail.kmail')
    if not kmail:
        raise Exception, "Cannot connected to KMail"
    return kmail


def addMessage(folder, message, kmail=None):
    "Adds a message to kmail with dbus interface"
    if not kmail:
        # Create a dbus object:
       kmail =  connectKMail()
       if not kmail:
            raise Exception, "Message cannot be added"
    # Add Message:
    ok, status = kmail.dbusAddMessage(str(folder), message, "")
    if not ok:
        raise DBusException, "Can not connect to kmail with DBus"
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


class DBUSError(Exception):
    pass

class MailError(Exception):
    pass

class DuplicateMessage(Exception):
    pass

