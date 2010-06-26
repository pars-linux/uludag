#! /usr/bin/env python
# -*- coding: utf-8 -*-

import string

from pisi.api import install
from pisi.api import list_available
from pisi.api import calculate_download_size
from pisi.errors import PrivilegeError

#        testcaseInstall = testinstall.TestInstall(listInstall, self.installed_packages(), self.available_packages())

class TestInstall:
    """Class for the testcase install."""
    def __init__(self, packagelist, installedpackages, availablepackages):
        self.packagelist = packagelist
        self.installedpackages = installedpackages
        self.availablepackages = availablepackages
    
    def test_install(self):
        """Use the pisi api to install the packages"""
        # Packages which are in the testcase file and are not installed
        packagestNotInstalled = list(set(self.packagelist) - set(self.installedpackages))
        if not packagestNotInstalled:
            print 'All the required packages are installed.'
            return
        # Install only packages that are in all the repositories
        packagesNotInRepo = list(set(packagestNotInstalled) - set((self.availablepackages)))
        if packagesNotInRepo:
            print "The following packages were not found in the repository: '{0}'".format(string.join(packagesNotInRepo, ', '))
        # Only try installing those packages which are in the repository
        finalPacakges = list(set(packagestNotInstalled) - set(packagesNotInRepo))
        totalPackages = len(finalPacakges)
        if totalPackages == 0:
            print 'No packages were installed.'
            return
        print 'Number of packages to be installed: [ {0} ]'.format(totalPackages)
        print 'Installing required packages, please wait ... (Size: {0:.2f} MB)'.format(calculate_download_size(finalPacakges)[0]/(1024.0 * 1024.0))
        counter = 0 
        while counter < totalPackages:
            # Pisi installs new packages by using a list. However if we pass all the
            # packages as a single list, we don't have much control over the errors.
            # That is why pass a single package as a list here
            package = finalPacakges[counter]
            singlePackage = string.split(finalPacakges[counter])
            try:
                install(singlePackage)
            except PrivilegeError:      # in case the user doesn't have permission
                print '\n[Error]: To install the packages, run the framework with root privileges.'
                return
            counter += 1
        print "\nFinished installing the following packages: '{0}'".format(string.join(finalPacakges, ', '))