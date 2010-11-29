#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import bz2
import lzma
import urllib2
import piksemel
import pisi

''' URLs of Repositories  '''
repoList = {"http://svn.pardus.org.tr/pardus/2009/devel/pisi-index.xml.bz2",
            "http://svn.pardus.org.tr/pardus/2011/devel/pisi-index.xml.bz2",
            "http://svn.pardus.org.tr/pardus/corporate2/devel/pisi-index.xml.bz2"}

''' Ordered list of distributions  that are iterated '''
''' It will be used to specify which distribution the repos entry such as #package, #patch is for  '''
distroList = []

''' Details about packages  '''
''' Structure : {packager_name -> {package_name -> [[[release1, version1],..,[releaseX, versionX]], [#package1,..,#packageX], [#patch1,..,#patchX], [distro_version1,..,distro_versionX] [packager_name,packager_mail]]},..} '''
repos = {}

options = {"uc":False, "nm":False, "r":False, "sc":False}

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
                    if name.endswith(".bz2") or name.endswith(".xz")
                        repoListTemp.append(name)
        repoList = []
        repoList.extend(repoListTemp)

''' This function checks if the package given as parameter is in the conflict list '''
def isPackageInConflictList(currentPackage):
    for package in conflictList:
        if package == currentPackage:
            return True

    return False

''' This function reads source pisi index file as remote or local and constructs "repos" structure based on this file '''
def fetchRepos():
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

            repos[spec.source.packager.name][spec.source.name][0].append([spec.history[0].release, spec.history[0].version])
            repos[spec.source.packager.name][spec.source.name][1].append(len(spec.packages))
            repos[spec.source.packager.name][spec.source.name][2].append(len(spec.source.patches))
            repos[spec.source.packager.name][spec.source.name][3].append(distroList[order])
            repos[spec.source.packager.name][spec.source.name][4].append(spec.source.packager.email)

            ''' We may have multiple packagers as owner of the same package residing on different repositories '''
            ''' In that case, we need to mark the package as conflict and be aware of it while sending mail to the packager '''
            if not isPackageInConflictList(spec.source.name):
                conflictList.append(spec.source.name)

''' This function analyzes "repos" structure and send e-mail to the packagers if their package(s) are out-of-sync between different repositories '''
def analyzeRepos():
    # Analze repos structure and send e-mail if necessary

if __name__ == "__main__":

    if len(sys.argv) > 1:
        processCmdLine()

    fetchRepos()
    analyzeRepos()
