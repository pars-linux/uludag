#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

repoList = ["http://svn.pardus.org.tr/pardus/2009/devel/pisi-index.xml.bz2",
            "http://svn.pardus.org.tr/pardus/2011/devel/pisi-index.xml.bz2",
            "http://svn.pardus.org.tr/pardus/corporate2/devel/pisi-index.xml.bz2"]

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
            repoListTemp.append(arg)

    ''' In case that repo list is overriden by user '''
    if len(repoListTemp) > 0:
        repoList = []
        repoList.extend(repoListTemp)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        processCmdLine()
