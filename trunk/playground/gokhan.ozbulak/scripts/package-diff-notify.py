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

''' URLs of Repositories  '''
repoList = {"http://svn.pardus.org.tr/pardus/2009/devel/pisi-index.xml.bz2",
            "http://svn.pardus.org.tr/pardus/2011/devel/pisi-index.xml.bz2",
            "http://svn.pardus.org.tr/pardus/corporate2/devel/pisi-index.xml.bz2"}


''' Details about packages  '''
''' Structure : {packager_name -> {package_name -> [[[release1, version1],..,[releaseX, versionX]], [#package1,..,#packageX], [#patch1,..,#patchX], [distro_version1,..,distro_versionX] [packager_mail1,..,packager_mailX]]},..} '''
repos = {}

options = {"uc":False, "nm":False, "r":False, "sc":False}

''' This stores packager list maintaining same package in different distributions  '''
conflictList=[]

''' Modify here if necessary '''
reportFile = "report"
contentHeader = "Here is a summary about your packages reside on different repositories.\nPlease, take action based on summary column below.\n\n\t\t\t***PACKAGES***"
contentFooter = "You are getting this e-mail because you have packages in our repositories. If you think you shouldn't receive this e-mail please contact with ..."
mailSender = "gozbulak@pardus.org.tr"
mailSenderPwd = "type_pwd_here"
mailSubject = "Package Summary"
mailServer = "mail.pardus.org.tr"

def printHelp(detail=False, retVal=-1):
    print "This is a notifier script. Usage:"
    print "\tpackage-diff-notify [options] <repoURL1> <repoURL2> ... <repoURLx>"

    if detail:
        print "Option details..."

    sys.exit(retVal)

def processCmdLine():
    global repoList, options
    repoListTemp = []

    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        printHelp(True, 0)

    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            ''' This is long option  '''
            option = arg[arg.rfind("-") + 1:]
            if option == "usecache": options["uc"] = True
            elif option == "nomail": options["nm"] = True
            elif option == "report": options["r"] = True
            elif option == "splitcheck": options["sc"] = True
            else:
                printHelp(True)
        elif arg.startswith("-"):
            ''' This is short option  '''
            option = arg[arg.rfind("-") + 1:]
            if options.has_key(option):
                options[option] = True
            else:
                printHelp(True)
        else:
            ''' This is repo url  '''
            if not arg.endswith(".bz2") and not arg.endswith(".xz"):
                printHelp(True)
            repoListTemp.append(arg)

    if options["uc"] and repoListTemp:
        printHelp(True)
    else:
        if options["uc"]:
            ''' In cache, only .bz2 and .xz files are considered for now  '''
            for root, dirs, files in os.walk(os.getcwd()):
                for name in files:
                    if name.endswith(".bz2") or name.endswith(".xz"):
                        repoListTemp.append(name)
                        print repoListTemp
        elif repoListTemp:
            repoList = []
            repoList.extend(repoListTemp)

''' This function reads source pisi index file as remote or local and constructs "repos" structure based on this file '''
def fetchRepos():
    ''' distroList is used to specify which distribution the repos entry such as #package, #patch is for  '''
    distroList = []

    pisiIndex = pisi.index.Index()
    for order, repo in enumerate(repoList):
        if options["uc"]:
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
        distroList.append(pisiIndex.distribution.version)

        ''' Update "repos" structure with current spec info '''
        for spec in pisiIndex.specs:
            if not repos.has_key(spec.source.packager.name):
                repos[spec.source.packager.name] = {}
            if not repos[spec.source.packager.name].has_key(spec.source.name):
                repos[spec.source.packager.name][spec.source.name] = [[], [], [], [], []]
            else:
                repos[spec.source.packager.name][spec.source.name][4].append()

            repos[spec.source.packager.name][spec.source.name][0].append([spec.history[0].release, spec.history[0].version])
            repos[spec.source.packager.name][spec.source.name][1].append(len(spec.packages))
            repos[spec.source.packager.name][spec.source.name][2].append(len(spec.source.patches))
            repos[spec.source.packager.name][spec.source.name][3].append(distroList[order])
            if not spec.source.packager.mail in repos[spec.source.packager.name][spec.source.name][4]:
                repos[spec.source.packager.name][spec.source.name][4].append(spec.source.packager.email)

            ''' We may have multiple packagers as owner of the same package residing on different repositories '''
            ''' In that case, we need to mark the package as conflict and be aware of it while sending mail to the packager '''
            if not spec.source.name in conflictList:
                conflictList.append(spec.source.name)

''' This function returns a string including status info about all packages of a packager  '''
def prepareContentBody(packager):
    # THIS IS GONNA CHANGE
    content = ""
    for packager in repos.keys():
        for package in repos[packager].keys():
            content = "%s\n (%s-%s) -> %s" %(content, packager, package, repos[packager][package])

    return content,repos[packager][package][4][0]

''' This function gathers all e-mail addresses a packager specifies in his/her packages '''
def prepareRecevierMailList(packager):
    mailList = []

    for package in repos[packager].key():
        for mail in repos[packager][package][4]:
            if not mail in mailList:
                mailList.append(mail)

    return ",".join(mailList)

''' This function sends mail to the recipient whose details are passed  '''
def sendMail(receiver, contentBody):
    msg = MIMEText("%s\n%s\n%s" % (contentHeader, contentBody.encode("utf-8"), contentFooter))
    ''' Envelope Information, just to show the e-mail correctly in recipient inbox and not to be marked as spam '''
    msg["Subject"] = mailSubject
    msg["From"] = mailSender
    msg["To"] = receiver

    try:
        if receiver == "gozbulak@pardus.org.tr":
            smtp = smtplib.SMTP(mailServer)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(mailSender, mailSenderPwd)
            smtp.sendmail(mailSender, receiver, msg.as_string())
            smtp.quit()
    except Exception:
        return -1

''' This function traverses "repos" structure to send e-mail to the packagers about their package(s) status and generate a report if necessary '''
def traverseRepos():
    ''' Open report file if report option is set  '''
    if options["r"]:
        fp = open(reportFile, "w")
    for packager in repos.keys():
        contentBody = prepareContentBody(packager)

        if not options["nm"]:
            receiverMailList = prepareReceiverMailList(packager)
            if sendMail(receiverMailList, contentBody):
                print "Send mail to %s failed." % mailReceiver
        if options["r"]:
            fp.write(contentBody)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        processCmdLine()

    fetchRepos()
    traverseRepos()
