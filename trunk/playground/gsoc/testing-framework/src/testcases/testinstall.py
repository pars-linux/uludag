#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pisi.api import install
from pisi.api import list_available
from pisi.api import calculate_download_size

from pisi.errors import PrivilegeError

from clcolorize import colorize


class TestInstall:
    """This class will first check for packages which are already installed, then
    will check all the available repositories to see whether the package exists.
    After checking all the above, then only it would proceed to call the Pisi API
    to attempt to install the packages."""
    def __init__(self, packagelist, installedpackages, availablepackages,
                                        failcode=None, summary=None, report=None):
        self.packagelist = packagelist
        self.installedpackages = installedpackages
        self.availablepackages = availablepackages
        self.failcode = 1
        self.summary = list()
        self.report = list()
    
    def test_install_main(self):
        """Check the conditions and call the Pisi API to install the packages"""
        # Packages in the testcase file but not installed
        packagestNotInstalled = list(set(self.packagelist) -
                                     set(self.installedpackages))
        if not packagestNotInstalled:
            self.report.append('All the required packages are installed')
            self.summary.append('Success')
            return
       
        # Install only packages that are in all the available repositories
        packagesNotInRepo = list(set(packagestNotInstalled) -
                                 set((self.availablepackages)))
        if packagesNotInRepo:
            self.report.append('The following packages were not found in ' \
                    "the repository: '{0}'".format(', '.join(packagesNotInRepo)))
        
        # if none of the package to be installed was found in the repository
        # set the failcode to 0 and return. The installation won't continue
        if len(packagesNotInRepo) == len(self.packagelist):
            self.summary.append('Fail')
            self.failcode = 0
            return
        
        # Modify the package list and remove the packages which are not in the
        # repository. this is done so 
        self.packagelist = list(set(self.packagelist) - set(packagesNotInRepo))
       
        # Only try installing those packages which are in the repository
        finalPackages = list(set(packagestNotInstalled) - set(packagesNotInRepo))
        totalPackages = len(finalPackages)
        if totalPackages == 0:
            self.report.append('No packages were installed')
            self.summary.append('Success')
            return
        
        # Calculate the download size and display it in MB        
        downloadSize = calculate_download_size(finalPackages)[0]/(1024.0 * 1024.0)
        self.report.append('Number of packages to be installed: ' \
            "'{0}', total size: '{1:.2f} MB'".format(totalPackages, downloadSize))
        print 'Installing packages, please wait ... ' \
                'Size:', colorize('{0:.2f} MB', 'bold').format(downloadSize)
        counter = 0 
        while counter < totalPackages:
            # Pisi installs new packages by using a list. However if we pass all the
            # packages as a single list, we don't have much control over the errors.
            # That is why pass a single package as a list here
            package = finalPackages[counter]
            singlePackage = package.split()
            try:
                install(singlePackage)
            except PrivilegeError:      # in case the user doesn't have permission
                self.report.append('Error: To install the packages, ' \
                                        'run the framework with root privileges')
                self.failcode = 0       # for the testcases gui, shell and automated
                print colorize('Failed: Privilege error. Run as root user.', 'red')
                self.summary.append('Fail')
                return
            counter += 1
        self.report.append("Finished installing the following " \
                            "packages: '{0}'".format(', '.join(finalPackages)))
        self.summary.append('Success')