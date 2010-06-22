#! /usr/bin/env python
# -*- coding: utf-8 -*-

import string
from pisi.api import install
from pisi.errors import PrivilegeError

def test_install(packagelist, installedpackages):
    """Use the pisi api to install the packages"""
    packagestNotInstalled = list(set(packagelist) - set(installedpackages))
    totalPackages = len(packagestNotInstalled)
    if not packagestNotInstalled:
        print 'All the required packages are installed.'
        return
    counter = 0
    print 'Number of packages to be installed: [ {0} ]'.format(totalPackages)
    print 'Installing required packages. Please wait ...'
    while counter < totalPackages:
        package = packagestNotInstalled[counter]
        singlePackage = string.split(packagestNotInstalled[counter])
        try:
            install(singlePackage)
            print 'Finished installing the required packages.'
        except PrivilegeError:
            print '[Error]: The framework is not running with root privileges.'
            print '[Solution]: To install the packages, please run the framework with root privileges.'
        except:
            print "[Failed]: The package '{0}' was not found in the repository.".format(package)
        counter += 1
