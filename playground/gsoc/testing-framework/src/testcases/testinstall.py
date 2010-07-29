#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pisi.api import install
from pisi.api import list_available
from pisi.api import calculate_download_size

from clcolorize import colorize

from pisi.errors import PrivilegeError


class TestInstall:
    """This class will first check for packages which are already installed, then
    will check all the available repositories to see whether the package exists.
    After checking all the above, then only it would proceed to call the Pisi API
    to attempt to install the packages."""
    def __init__(self, packagelist, installedpackages, availablepackages,
                                            failcode=None, report=None):
        self.packagelist = packagelist
        self.installedpackages = installedpackages
        self.availablepackages = availablepackages
        self.failcode = 1
        self.report = list()
    
    def test_install_main(self):
        """Check the conditions and call the Pisi API to install the packages"""
        # Packages in the testcase file but not installed
        packagestNotInstalled = list(set(self.packagelist) -
                                     set(self.installedpackages))
        if not packagestNotInstalled:
            self.report.append('All the required packages are installed')
            return
       
        # Install only packages that are in all the available repositories
        packagesNotInRepo = list(set(packagestNotInstalled) -
                                 set((self.availablepackages)))
        if packagesNotInRepo:
            self.report.append('The following packages were not found in ' \
                    "the repository: '{0}'".format(', '.join(packagesNotInRepo)))
       
        # Only try installing those packages which are in the repository
        finalPacakges = list(set(packagestNotInstalled) - set(packagesNotInRepo))
        totalPackages = len(finalPacakges)
        if totalPackages == 0:
            self.report.append('No packages were installed\n')
            return
        
        downloadSize = calculate_download_size(finalPacakges)[0]/(1024.0 * 1024.0)
        self.report.append('Number of packages to be installed: ' \
            "'{0}', total size: '{1:.2f} MB'".format(totalPackages, downloadSize))
        counter = 0 
        while counter < totalPackages:
            # Pisi installs new packages by using a list. However if we pass all the
            # packages as a single list, we don't have much control over the errors.
            # That is why pass a single package as a list here
            package = finalPacakges[counter]
            singlePackage = package.split()
            try:
                print 'Installing packages, please wait ... ' \
                'Size:', colorize('{0:.2f} MB', 'bold').format(downloadSize)
                install(singlePackage)
            except PrivilegeError:      # in case the user doesn't have permission
                self.report.append('Error: To install the packages, ' \
                                   'run the framework with root privileges')
                self.failcode = 0       # for the testcases gui, shell and automated
                print colorize('Failed: Privilege error. Run as root user.', 'red')
                return
            counter += 1
        self.report.append("Finished installing the following " \
                           "packages: '{0}'".format(', '.join(finalPacakges)))