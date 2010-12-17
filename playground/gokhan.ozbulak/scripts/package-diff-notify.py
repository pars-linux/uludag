#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

import sys
import os
import string
import bz2
import lzma
import urllib2
import piksemel
import pisi
import smtplib
from email.mime.text import MIMEText
from optparse import OptionParser

# URLs of Repositories
# It is recommended to define repoList as from newest repo to oldest one
repoList = (
                "http://svn.pardus.org.tr/pardus/2011/devel/pisi-index.xml.bz2",
                "http://svn.pardus.org.tr/pardus/corporate2/devel/pisi-index.xml.bz2",
                "http://svn.pardus.org.tr/pardus/2009/devel/pisi-index.xml.bz2"
           )


# Details about packages
# Structure : {packager_name -> {package_name -> [[[release1, version1],..,[releaseX, versionX]], [#package1,..,#packageX], [#patch1,..,#patchX], [distro_version1,..,distro_versionX] [packager_mail1,..,packager_mailX]]},..}
repos = {}
RELEASES, NRPACKAGES, NRPATCHES, DISTROS, MAILS = range(5)

# Option parser object
options = None

# This stores packager list maintaining same package in different distributions  '''
# Structure : { package_name -> [packager_name1,..,packager_nameX]}  '''
conflictDict = {}

# distroList is used to specify which distribution the repos entry such as #package, #patch is for
distroList = []

# This is mapping of obsolete package to the new package
# Structure : {obsolete_package -> new_package}
obsoleteDict = {}

# Modify here if necessary
mailSender = "sender_name_here"
mailSenderUsr = "sender@pardus.org.tr"
mailSenderPwd = "pwd_here"
mailSubject = "Package Summary"
mailServer = "mail.pardus.org.tr"

mailTemplate = """\
From: %s <%s>
To: %s
Subject: [Pardus] Package Summary
Content-Type: text/plain; charset="utf-8"

Dear Pardus contributor,

Here is a summary about your packages reside on our Pardus repositories. Please, take action
based on the report below:
-----------------------------------------------------------

%s

-----------------------------------------------------------
You're getting this e-mail because you have packages in our repositories.
If you think you shouldn't receive such e-mail, please contact with %s
"""

def processCmdLine():
    global options
    args = []

    # Initialization of option parser object
    usageStr = "Usage: package-diff-notify [options] [repoURL [repoURL ...]]"
    desStr = "This is a notifier script to give detailed info to packagers about their packages."
    epiStr = "repoURL:\t  compressed pisi-index file path in URL format as xz or bz2"

    parser = OptionParser(prog = "package-diff-notify", version = "%prog 1.0", usage = usageStr, description = desStr, epilog = epiStr)

    parser.add_option("-u", "--uselocal", dest = "uselocal", action = "store_true", default = False, help = "use local pisi-index files as xz or bz2. Use without <repoURL>")
    parser.add_option("-m", "--mail", dest = "mail", action = "store_true", default = False, help = "allow the util to send e-mails to packagers")
    parser.add_option("-r", "--report", dest = "report", action = "store_true", default = False, help = "dump the output into separate files")
    parser.add_option("-p", "--packager", dest = "packager", action = "store", type = "string", help = "filter the output to show details about specified packager(s) only")
    parser.add_option("-k", "--package", dest = "package", action = "store", type = "string", help = "filter the output to show details about the specified packager only")

    # Parse the command line
    (options, args) = parser.parse_args()

    # Process the command line
    if options.uselocal and args:
        parser.print_help()
        return False
    else:
        if options.uselocal:
            repoList = []
            # In cwd, only .bz2 and .xz files are considered for now
            for root, dirs, files in os.walk(os.getcwd()):
                for name in files:
                    if name.endswith(".bz2") or name.endswith(".xz"):
                        repoList.append(name)
            if not repoList:
                parser.print_help()
                return False
        elif args:
            repoList = args

    return True

def handleReplaces(spec):
    ''' This function detects if the package is replaced with other package-obsolete package- and moves the packagers of obsolete package into new package '''

    # We're just interested in the sub-package that has same name with the source name, ignoring other sub-packages if any
    for package in spec.packages:
        if package.name == spec.source.name:
            for replace in package.replaces:
                if not obsoleteDict.has_key(replace.package):
                    obsoleteDict[replace.package] = spec.source.name
                    # Move obsolete package as new package in conflictDict
                    if conflictDict.has_key(replace.package):
                        tmpPackagerList = conflictDict[replace.package]
                        del conflictDict[replace.package]
                        for tmpPackager in tmpPackagerList:
                            if tmpPackager not in conflictDict[spec.source.name]:
                                conflictDict[spec.source.name].append(tmpPackager)

def fetchRepos():
    ''' This function reads source pisi index file as remote or local and constructs "repos" structure based on this file '''

    pisiIndex = pisi.index.Index()
    for order, repo in enumerate(repoList):
        if options.uselocal:
            # Use the local index files
            if repo.endswith(".bz2"):
                decompressedIndex = bz2.decompress(open(repo, "r").read())
            else:
                # Must be .xz
                decompressedIndex = lzma.decompress(open(repo, "r").read())
        else:
            # Use the remote index files
            if repo.endswith(".bz2"):
                decompressedIndex = bz2.decompress(urllib2.urlopen(repo).read())
            else:
                decompressedIndex = lzma.decompress(urllib2.urlopen(repo).read())
        doc = piksemel.parseString(decompressedIndex)
        pisiIndex.decode(doc, [])

        # Populate distroList in order of iteration done for repositories
        distroList.append("%s %s" %(pisiIndex.distribution.sourceName, pisiIndex.distribution.version))

        # Update "repos" structure with current spec info
        for spec in pisiIndex.specs:
            if not repos.has_key(spec.source.packager.name):
                repos[spec.source.packager.name] = {}
            if not repos[spec.source.packager.name].has_key(spec.source.name):
                repos[spec.source.packager.name][spec.source.name] = [[], [], [], [], []]

            repos[spec.source.packager.name][spec.source.name][RELEASES].append([spec.history[0].release, spec.history[0].version])
            repos[spec.source.packager.name][spec.source.name][NRPACKAGES].append(len(spec.packages))
            repos[spec.source.packager.name][spec.source.name][NRPATCHES].append(len(spec.source.patches))
            repos[spec.source.packager.name][spec.source.name][DISTROS].append(distroList[order])
            if spec.source.packager.email not in repos[spec.source.packager.name][spec.source.name][MAILS]:
                repos[spec.source.packager.name][spec.source.name][MAILS].append(spec.source.packager.email)

            # We may have multiple packagers as owner of the same package residing on different repositories
            # In that case, we need to mark the package as in conflict and be aware of it while sending mail to the packager
            if conflictDict.has_key(spec.source.name):
                if spec.source.packager.name not in conflictDict[spec.source.name]:
                    conflictDict[spec.source.name].append(spec.source.packager.name)
            else:
                if obsoleteDict.has_key(spec.source.name):
                    # This control flow is redundant actually,if we have package in obsoleteDict then new package should have already been exist in conflictDict
                    # The flow is here not to lose the track of code
                    if conflictDict.has_key(obsoleteDict[spec.source.name]):
                        if spec.source.packager.name not in conflictDict[obsoleteDict[spec.source.name]]:
                            conflictDict[obsoleteDict[spec.source.name]].append(spec.source.packager.name)
                else:
                    conflictDict[spec.source.name] = [spec.source.packager.name]

            # Replaces check and handling
            handleReplaces(spec)

def createSummaryEntry(packager, package, distro):
    ''' This function creates a summary entry whose structure is specified below for given repo, say 2009 or 2011 '''

    order = repos[packager][package][DISTROS].index(distro)

    # summaryEntry = [packager_name, packager_mail, release_no, version_no, #package, #patch]
    summaryEntry = [
                    package,
                    packager,
                    repos[packager][package][MAILS],
                    repos[packager][package][RELEASES][order][0],
                    repos[packager][package][RELEASES][order][1],
                    repos[packager][package][NRPACKAGES][order],
                    repos[packager][package][NRPATCHES][order],
                    ]

    return summaryEntry

def createStanza(summaryDict):
    ''' This function create a stanza for each package. It includes details about a package exist in different distributions  '''

    sectionList = ("Package Names", "Packager", "Email", "Release", "Version", "Number of Sub-Package", "Number of Patches")
    content = ""

    # Indexing to traverse summaryDict as in sectionList manner
    for order, section in enumerate(sectionList):
        tmpContent = ""
        # Ignoring the Email item in sectionList, because handled it in previous iteration
        if section == "Email": continue
        for distro in distroList:
            if summaryDict.has_key(distro):
                if section == "Packager":
                    tmpContent = "%s    %-30s: %s <%s>\n" % (tmpContent, distro, summaryDict[distro][order], ",".join(summaryDict[distro][order + 1]))
                else:
                    tmpContent += "    %-30s: %s\n" % (distro, summaryDict[distro][order])
        content += " %s:\n%s" % (sectionList[order], tmpContent)

    return content

def isSummaryDictEmpty(summaryDict):
    for item in summaryDict.values():
        if item:
            return False

    return True

def prepareContentBody(packager):
    ''' This function generates status info about all packages of the given packager '''

    content = ""
    packageHistory = []

    if options.package:
        # Trim input coming from cmd line
        packageList = map(string.strip, options.package.split(","))
    else:
        packageList = repos[packager].keys()

    for package in packageList:
        # No need to replicate same info for obsolete package in content
        # Must consider as reversible
        if obsoleteDict.has_key(package):
            if obsoleteDict[package] in packageHistory:
                continue
        omitPackage = False
        for item in packageHistory:
            if obsoleteDict.has_key(item):
                if obsoleteDict[item] == package:
                    omitPackage = True
                    break

        if omitPackage: continue

        summaryDict = {}
        for distro in distroList:
            if repos[packager].has_key(package):
                if distro in repos[packager][package][3]:
                    summaryDict[distro] = createSummaryEntry(packager, package, distro)
                else:
                    if obsoleteDict.has_key(package):
                        pck = obsoleteDict[package]
                    else:
                        pck = package

                    for pckgr in conflictDict[pck]:
                        if repos[pckgr].has_key(pck):
                            if distro in repos[pckgr][pck][DISTROS]:
                                summaryDict[distro] = createSummaryEntry(pckgr, pck, distro)
                        if obsoleteDict.has_key(package) and repos[pckgr].has_key(package):
                            if distro in repos[pckgr][package][DISTROS]:
                                summaryDict[distro] = createSummaryEntry(pckgr, package, distro)

                    # Look for obsolete packages if no new package in distro
                    for obsolete, new in obsoleteDict.items():
                        # There may be more than one replace, no break
                        # {openoffice -> libreoffice}, {openoffice3 -> libreoffice} etc.
                        if new == package:
                            if conflictDict.has_key(new):
                                for pckgr in conflictDict[new]:
                                    if repos[pckgr].has_key(obsolete):
                                        if distro in repos[pckgr][obsolete][DISTROS]:
                                            summaryDict[distro] = createSummaryEntry(pckgr, obsolete ,distro)
        if not isSummaryDictEmpty(summaryDict):
            packageHistory.append(package)
            content = "%s%s\n%s\n%s\n\n" %(content, package, len(package) * "-", createStanza(summaryDict))

    return content

def prepareReceiverMailList(packager):
    ''' This function gathers all e-mail addresses a packager specifies in his/her packages '''

    mailList = []

    for package, info in repos[packager].items():
        for mail in info[MAILS]:
            if mail not in mailList:
                mailList.append(mail)

    return mailList

def sendMail(receiverList, contentBody):
    ''' This function sends mail to the recipient whose details are passed  '''

    if not mailSenderUsr or not mailSenderPwd or not mailServer:
        print "No enough information for connecting and authenticating to SMTP server."
        return False

    try:
        session = smtplib.SMTP(mailServer)
    except smtplib.SMTPConnectError:
        print "Opening socket to SMTP server failed"
        return False

    try:
        session.login(mailSenderUsr, mailSenderPwd)
    except smtplib.SMTPAuthenticationError:
        print "Authentication to SMTP server failed. Please, check your credentials."
        return False

    for receiver in receiverList:
        msg = mailTemplate % (mailSender, mailSenderUsr, receiver, contentBody, mailSenderUsr)
        print "Sending e-mail to %s ..." % receiver,
        try:
            session.sendmail(mailSenderUsr, receiver, msg)
            print "OK"
        except (smtplib.SMTPSenderRefused, smtplib.SMTPDataError):
            print "FAILED"

    session.quit()

    return True

def traverseRepos():
    ''' This function traverses "repos" structure to send e-mail to the packagers about their package(s) status and generate a report if necessary '''

    if options.packager:
        # Call unicode to match the cmd line string with key data of repos structure
        packagerList = [unicode(options.packager.strip())]
    else:
        packagerList = repos.keys()

    for packager in packagerList:
        contentBody = prepareContentBody(packager)

        if options.mail:
            receiverMailList = prepareReceiverMailList(packager)
            if not sendMail(receiverMailList, contentBody):
                return False

        if options.report:
            fp = open("_".join(packager.split()), "w")
            fp.write("%s" % contentBody)

    return True

def main():
    if not processCmdLine():
        return 1
    fetchRepos()
    if not traverseRepos():
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
