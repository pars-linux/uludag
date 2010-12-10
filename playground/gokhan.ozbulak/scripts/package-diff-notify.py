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

options = None

''' This stores packager list maintaining same package in different distributions  '''
''' Structure : { package_name -> [packager_name1,..,packager_nameX]}  '''
conflictList = {}

''' distroList is used to specify which distribution the repos entry such as #package, #patch is for  '''
distroList = []

''' Modify here if necessary '''
reportFile = "report"
mailSender = "gozbulak@pardus.org.tr"
mailSenderPwd = "pwd_here"
mailSubject = "Package Summary"
mailServer = "mail.pardus.org.tr"
contentHeader = "Here is a summary about your packages reside on different repositories.\nPlease, take action based on summary column below.\n\n\t\t\t\t\t***PACKAGES***\n"
columns = "|%-50s|%-30s|%-10s|%-20s|%-10s|%-10s|%-100s|" %("Package", "Distro", "Release no", "Version no", "#Package", "#Patch", "Is there conflict?")
contentHeader = "%s%s" %("Here is a summary about your packages reside on different repositories.\nPlease, take action based on summary column below.\n\n\t\t\t\t\t***PACKAGES***\n", columns)
contentFooter = "You are getting this e-mail because you have packages in our repositories. If you think you shouldn't receive this e-mail please contact with %s" %(mailSender)

# Remove this later
def suppressprintHelp(detail=False, retVal=-1):
    print "This is a notifier script to give detailed info to packagers about their packages.\nUsage:\n"\
          "\tpackage-diff-notify [options] [<repoURL1> <repoURL2> ... <repoURLx>]\n"

    if detail:
        print "\t%-20s%-50s\n" %("<repoURL>", "Compressed pisi index file(pisi-index) path in URL format. Use 'xz' or 'bz2' files")
        print "Options:\n",\
              "\t%-20s%-50s\n" %("--help", "Display this information"),\
              "\t%-20s%-50s\n" %("--usecache", "Use the cached pisi index files compressed as 'xz' or 'bz2' format. Use without <repoURL>"),\
              "\t%-20s%-50s\n" %("--nomail", "Prevent the util from sending e-mail to packagers"),\
              "\t%-20s%-50s\n" %("--report", "Dump the output into a file named 'report'"),\
              "\t%-20s%-50s\n" %("-h", "Short option for 'help'"),\
              "\t%-20s%-50s\n" %("-uc", "Short option for 'usecache'"),\
              "\t%-20s%-50s\n" %("-nm", "Short option for 'nomail'"),\
              "\t%-20s%-50s\n" %("-r", "Short option for 'report'"),\

    sys.exit(retVal)

# Remove this later
def suppressprocessCmdLine():
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

def processCmdLine():
    global options
    args = []

    ''' Initialization option parser object '''
    usageStr = "Usage: package-diff-notify [options] [repoURL [repoURL ...]]"
    desStr = "This is a notifier script to give detailed info to packagers about their packages."
    epiStr = "repoURL:\t  compressed pisi-index file path in URL format as xz or bz2"
    tmp = "Use 'xz' or 'bz2' files."

    parser = OptionParser(prog = "package-diff-notify", version = "%prog 1.0", usage = usageStr, description = desStr, epilog = epiStr)
    parser.add_option("-u", "--uselocal", dest = "uselocal", action = "store_true", default = False, help = "use local pisi-index files as xz or bz2. Use without <repoURL>")
    parser.add_option("-n", "--nomail", dest = "nomail", action = "store_true", default = False, help = "prevent the util from sending e-mail to packagers")
    parser.add_option("-r", "--report", dest = "report", action = "store_true", default = False, help = "dump the output into separate files")

    ''' Parsing the command line '''
    (options, args) = parser.parse_args()

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
    summaryEntry = []
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

# Remove this later
''' This function returns a string including status info about all packages of a packager  '''
def suppressprepareContentBody(packager):
    content = "|%s|\n" %(230 * "-")
    for package in repos[packager].keys():
        for order, distro in enumerate(repos[packager][package][3]):
            ''' To prevent repeatation for package name and conflict check comment '''
            if order == 0:
                content = "%s|%-50s|" %(content, package)

                ''' Conflict check  '''
                conflictComment = "No"
                ''' Check if  there are  multiple packagers maintaining the same package'''
                if len(conflictList[package]) > 1:
                    ''' Packager may have more than one e-mail address  '''
                    tmpConflictList = list(conflictList[package])
                    for mail in repos[packager][package][4]:
                        if mail in conflictList[package]:
                            ''' Excluding packagers' own mail addresses without breaking conflict list '''
                            tmpConflictList.remove(mail)
                    if len(tmpConflictList) > 1:
                        conflictComment = "Yes, please contact with %s" %(tmpConflictList)
            else:
                content = "%s|%-50s|" % (content, " ")
                conflictComment = ""

            ''' Adding a new entry for the package as below '''
            '''  Distro_name | Release_no | Version_no | #Package | #Patch | Is there conflict? '''
            content = "%s%-30s|%-10s|%-20s|%-10s|%-10s|%-100s|\n" %(content,
                                                                distro,
                                                                repos[packager][package][0][order][0],
                                                                repos[packager][package][0][order][1],
                                                                repos[packager][package][1][order],
                                                                repos[packager][package][2][order],
                                                                conflictComment)

        content = "%s|%s|\n" %(content, (230 * "-"))

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
    msg = MIMEText("%s\n%s\n%s" % (contentHeader, contentBody.encode("utf-8"), contentFooter))
    ''' Envelope Information, just to show the e-mail correctly in recipient inbox and not to be marked as spam '''
    msg["Subject"] = mailSubject
    msg["From"] = mailSender

    try:
        for receiver in receiverList:
            if receiver == "x@pardus.org.tr":
                smtp = smtplib.SMTP(mailServer)
                msg["To"] = receiver
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(mailSender, mailSenderPwd)
                smtp.sendmail(mailSender, "gozbulak@pardus.org.tr", msg.as_string())
                smtp.quit()
    except Exception:
        return -1

''' This function traverses "repos" structure to send e-mail to the packagers about their package(s) status and generate a report if necessary '''
def traverseRepos():
    ''' Open report file if report option is set  '''
    for packager in repos.keys():
        contentBody = prepareContentBody(packager)

        if not options.nomail:
            receiverMailList = prepareReceiverMailList(packager)
            if sendMail(receiverMailList, contentBody):
                print "Send mail to %s failed." %(receiverMailList)

        if options.report:
            fp = open(packager, "w")
            fp.write("%s" %(contentBody))

def main():
    if processCmdLine(): return -1
    fetchRepos()
    traverseRepos()

if __name__ == "__main__":
    sys.exit(main())
