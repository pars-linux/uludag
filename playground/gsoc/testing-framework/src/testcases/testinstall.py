#! /usr/bin/env python
# -*- coding: utf-8 -*-

import string

from pisi.api import install
from pisi.api import list_available
from pisi.api import calculate_download_size
from pisi.errors import PrivilegeError


def test_install(packagelist, installedpackages, availablepackages):
    """Use the pisi api to install the packages"""
    # Packages which are in the testcase file and are not installed
    packagestNotInstalled = list(set(packagelist) - set(installedpackages))
    # Install only packages that are in all the repositories
    packagesNotInRepo = list(set(packagestNotInstalled) - set((availablepackages)))
    if packagesNotInRepo:
        print "The following packages were not found in the repository: '{0}'".format(string.join(packagesNotInRepo, ', '))
    # Only try installing those packages which are in the repository
    finalPacakges = list(set(packagestNotInstalled) - set(packagesNotInRepo))
    totalPackages = len(finalPacakges)
    if not finalPacakges:
        print 'All the required packages are installed.'
        return
    print 'Number of packages to be installed: [ {0} ]'.format(totalPackages)
    sizeInMB = 1024.0 * 1024.0
    print 'Installing required packages, please wait ... (Size: {0:.2f} MB)'.format(calculate_download_size(finalPacakges)[0]/sizeInMB)
    counter = 0 
    while counter < totalPackages:
        # Pisi installs new packages by using a list. However if we pass all the
        # packages as a single list, we don't have much control over the errors.
        # That is why pass a single package as a list here
        package = finalPacakges[counter]
        singlePackage = string.split(finalPacakges[counter])
        try:
            install(singlePackage)
            print '\nFinished installing the required packages.'
        except PrivilegeError:      # in case the user doesn't have permission
            print '[Error]: The framework is not running with root privileges.'
            print '[Solution]: To install the packages, run the framework with root privileges.'
            return
        counter += 1