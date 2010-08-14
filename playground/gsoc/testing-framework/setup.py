#! /usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import sys

from distutils.core import setup
from distutils.command import install

try:
    import pisi.api
    import pisi.errors
except ImportError:
    print 'Unable to import the PiSi API'
    sys.exit('Please ensure that you are running Pardus GNU/ Linux')

    
class Install(install):
    """Override the standard install to check for dependencies."""
    def run(self):
        if check_dependencies('lxml') is None:
            print "Found one missing dependency: 'lxml'"
            print 'Should I install it for you? (y / n): [y]'
            if choice in ('y', 'Y', 'yes', 'YES'):
                install_dependencies()
            else:
                print 'The required dependencies were not met'
                sys.exit('Aborting installation')


def check_dependencies(module_name):
    """Check for the required dependencies for the framework."""
    try:
        __import__(module_name)
    except ImportError:
        return None
    

def install_dependencies():
    package_list = ['lxml']
    try:
        pisi.api.install(package_list)
        return 
    except pisi.errors.PrivilegeError:
        sys.exit('Please run the script with root privileges')


if sys.version_info[:2] < (2, 4):
    print "Package Testing Framework requires Python 2.6 or better (but not " \
    "Python 3 yet).\nVersion {0} detected.".format(sys.version_info[:2])
    sys.exit(1)
        
setup(
      name='Package Tesing Framework',
      version='1.0',
      author='Sukhbir Singh',
      author_email='sukhbir.in@gmail.com',
      maintainer='Semen Cirit',
      maintainer_email='scirit@pardus.org.tr',      
      url='http://www.pardus.org.tr',
      description='A package testing framework for Pardus GNU/ Linux',
      license='GNU GPL',
      package_dir = {'': 'src'},
      packages = ['src', 'src.testcases', 'src.testcases.ui', 'doc'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: Qt',          
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',          
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX :: Linux',          
          'Programming Language :: Python :: 2.6',
          'Topic :: Software Development :: Testing'
          ],
      cmdclass={'install': Install} 
     )