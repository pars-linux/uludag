#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import bz2
import lzma
import urllib2
import piksemel
import pisi
import smtplib
from email.mime.text import MIMEText
from optparse import OptionParser

''' URLs of Repositories  '''
repoList = (
                "http://svn.pardus.org.tr/pardus/2009/devel/pisi-index.xml.bz2",
                "http://svn.pardus.org.tr/pardus/2011/devel/pisi-index.xml.bz2",
                "http://svn.pardus.org.tr/pardus/corporate2/devel/pisi-index.xml.bz2",
           )


''' Details about packages  '''
''' Structure : {packager_name -> {package_name -> [[[release1, version1],..,[releaseX, versionX]], [#package1,..,#packageX], [#patch1,..,#patchX], [distro_version1,..,distro_versionX] [packager_mail1,..,packager_mailX]]},..} '''
repos = {}

''' Option parser object '''
options = None

''' This stores packager list maintaining same package in different distributions  '''
''' Structure : { package_name -> [packager_name1,..,packager_nameX]}  '''
conflictList = {}

''' distroList is used to specify which distribution the repos entry such as #package, #patch is for  '''
distroList = []

''' Modify here if necessary '''
reportFile = "report"
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
based on comments next to package name. Comments and their explanations are as follows:
    Incomplete: This is shown if the package doesn't exist in one of the repositories at least.
    Conflict:   This is shown if the package is maintained by more than one packager in diferent repositories.
    Same:       This is shown if no difference among package attributes such as version number or number of patches applied
                in different repositories.
    Different:  This is opposite of comment 'Same'.
-----------------------------------------------------------

%s

-----------------------------------------------------------
You're getting this e-mail because you have packages in our repositories. If you think you shouldn't receive such e-mail, please contact with %s
"""

def processCmdLine():
    global options
    args = []

    ''' Initialization of option parser object '''
    usageStr = "Usage: package-diff-notify [options] [repoURL [repoURL ...]]"
    desStr = "This is a notifier script to give detailed info to packagers about their packages."
    epiStr = "repoURL:\t  compressed pisi-index file path in URL format as xz or bz2"

    parser = OptionParser(prog = "package-diff-notify", version = "%prog 1.0", usage = usageStr, description = desStr, epilog = epiStr)
    parser.add_option("-u", "--uselocal", dest = "uselocal", action = "store_true", default = False, help = "use local pisi-index files as xz or bz2. Use without <repoURL>")
    parser.add_option("-n", "--nomail", dest = "nomail", action = "store_true", default = False, help = "prevent the util from sending e-mail to packagers")
    parser.add_option("-r", "--report", dest = "report", action = "store_true", default = False, help = "dump the output into separate files")

    ''' Parse the command line '''
    (options, args) = parser.parse_args()

    ''' Process the command line  '''
    if options.uselocal and args:
        parser.print_help()
        return -1
    else:
        if options.uselocal:
            repoList = []
            ''' In cwd, only .bz2 and .xz files are considered for now  '''
            for root, dirs, files in os.walk(os.getcwd()):
                for name in files:
                    if name.endswith(".bz2") or name.endswith(".xz"):
                        repoList.append(name)
            if not repoList:
                parser.print_help()
                return -1
        elif args:
            repoList = args

''' This function reads source pisi index file as remote or local and constructs "repos" structure based on this file '''
def fetchRepos():
    pisiIndex = pisi.index.Index()
    for order, repo in enumerate(repoList):
        if options.uselocal:
            ''' Use the local index files '''
            if repo.endswith(".bz2"):
                decompressedIndex = bz2.decompress(file(repo).read())
            else:
                ''' Must be .xz  '''
                decompressedIndex = lzma.decompress(file(repo).read())
        else:
            ''' Use the remote index files '''
            if repo.endswith(".bz2"):
                decompressedIndex = bz2.decompress(urllib2.urlopen(repo).read())
            else:
                decompressedIndex = lzma.decompress(urllib2.urlopen(repo).read())
        doc = piksemel.parseString(decompressedIndex)
        pisiIndex.decode(doc, [])

        ''' Populate distroList in order of iteration done for repositories  '''
        distroList.append("%s %s" %(pisiIndex.distribution.sourceName, pisiIndex.distribution.version))

        ''' Update "repos" structure with current spec info '''
        for spec in pisiIndex.specs:
            if not repos.has_key(spec.source.packager.name):
                repos[spec.source.packager.name] = {}
            if not repos[spec.source.packager.name].has_key(spec.source.name):
                repos[spec.source.packager.name][spec.source.name] = [[], [], [], [], []]

            repos[spec.source.packager.name][spec.source.name][0].append([spec.history[0].release, spec.history[0].version])
            repos[spec.source.packager.name][spec.source.name][1].append(len(spec.packages))
            repos[spec.source.packager.name][spec.source.name][2].append(len(spec.source.patches))
            repos[spec.source.packager.name][spec.source.name][3].append(distroList[order])
            if not spec.source.packager.email in repos[spec.source.packager.name][spec.source.name][4]:
                repos[spec.source.packager.name][spec.source.name][4].append(spec.source.packager.email)

            ''' We may have multiple packagers as owner of the same package residing on different repositories '''
            ''' In that case, we need to mark the package as in conflict and be aware of it while sending mail to the packager '''
            if conflictList.has_key(spec.source.name):
                if not spec.source.packager.name in conflictList[spec.source.name]:
                    conflictList[spec.source.name].append(spec.source.packager.name)
            else:
                conflictList[spec.source.name] = [spec.source.packager.name]

''' This function creates a summary entry whose structure is specified below for given repo, say 2009 or 2011  '''
''' summaryEntry = [packager_name, packager_mail, release_no, version_no, #package, #patch] '''
def createSummaryEntry(packager, package, distro):
    order = repos[packager][package][3].index(distro)
    summaryEntry = [
                    packager,
                    repos[packager][package][4],
                    repos[packager][package][0][order][0],
                    repos[packager][package][0][order][1],
                    repos[packager][package][1][order],
                    repos[packager][package][2][order]
                    ]

    return summaryEntry

''' This function compares list items addressed with index argument and returns false if difference is detected  '''
def isListContentSame(summaryList, index):
    for distro in summaryList.keys():
        for dstr in summaryList.keys():
            if not summaryList[distro][index] == summaryList[dstr][index]:
                return "Different"

    return "Same"

''' This function create a stanza for each package. It includes details about a package exist in different distributions  '''
def createStanza(summaryList, conflict):
    sectionList = ("Email", "Packager(s)", "Release(s)", "Version(s)", "Number of Package", "Number of Patch")
    content = ""

    ''' Indexing to traverse summaryList as in sectionList manner  '''
    for i in range(6):
        tmpContent = ""; comment = ""; incomplete = False
        ''' İgnoring the first item in sectionList, because will handle it in nex iteration  '''
        if i == 0: continue
        for distro in distroList:
            if summaryList.has_key(distro):
                if i == 1:
                    tmpContent = "%s    %-30s: %-30s %s\n" %(tmpContent, distro, summaryList[distro][i - 1], summaryList[distro][i])
                else:
                    tmpContent = "%s    %-30s: %s\n" %(tmpContent, distro, summaryList[distro][i])
            else:
                incomplete = True
        if incomplete:
            comment = "%s %s " %(comment, "Incomplete")
        if conflict:
            comment = "%s %s " %(comment, "Conflict")
        comment = "%s %s " %(comment, isListContentSame(summaryList, i))
        content = "%s %s: [%s]\n%s" %(content, sectionList[i], comment, tmpContent)

    return content

''' This function generates status info about all packages of the given packager '''
def prepareContentBody(packager):
    content = ""

    for package in repos[packager].keys():
        summaryList = {}
        isConflict = False
        for distro in distroList:
            if distro in repos[packager][package][3]:
                summaryList[distro] = createSummaryEntry(packager, package, distro)
            elif len(conflictList[package]) > 1:
                isConflict = True
                for pckgr in conflictList[package]:
                    if distro in repos[pckgr][package][3]:
                        summaryList[distro] = createSummaryEntry(pckgr, package, distro)
        content = "%s%s\n%s\n%s\n\n" %(content, package, len(package) * "-", createStanza(summaryList, isConflict))

    return content

''' This function gathers all e-mail addresses a packager specifies in his/her packages '''
def prepareReceiverMailList(packager):
    mailList = []

    for package in repos[packager].keys():
        for mail in repos[packager][package][4]:
            if not mail in mailList:
                mailList.append(mail)

    return mailList

''' This function sends mail to the recipient whose details are passed  '''
def sendMail(receiverList, contentBody):
    if not mailSenderUsr or not mailSenderPwd or not mailServer:
        print "No enough information for connecting and authenticating to SMTP server."
        return -1

    try:
        session = smtplib.SMTP(mailServer)
    except:
        print "Opening socket to SMTP server failed"
        return -1

    try:
        session.login(mailSenderUsr, mailSenderPwd)
    except:
        print "Authentication to SMTP server failed. Please, check your credentials."
        return -1

    for receiver in receiverList:
        if receiver == "x@pardus.org.tr":
            msg = mailTemplate %(mailSender, mailSenderUsr, receiver, contentBody, mailSenderUsr)
            print "Sending e-mail to %s..." %(receiver),
            try:
                session.sendmail(mailSenderUsr, receiver, msg)
                print "[OK]"
            except:
                print "[FAILED]"

    session.quit()

''' This function traverses "repos" structure to send e-mail to the packagers about their package(s) status and generate a report if necessary '''
def traverseRepos():
    for packager in repos.keys():
        contentBody = prepareContentBody(packager)

        if not options.nomail:
            receiverMailList = prepareReceiverMailList(packager)
            if sendMail(receiverMailList, contentBody):
                return -1

        if options.report:
            fp = open("_".join(packager.split(" ")), "w")
            fp.write("%s" %(contentBody))

def main():
    if processCmdLine(): return -1
    fetchRepos()
    if traverseRepos(): return -1

if __name__ == "__main__":
    sys.exit(main())
