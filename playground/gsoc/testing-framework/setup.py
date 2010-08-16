#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from distutils.core import setup
from distutils.command.install import install
from distutils.command.build import build

try:
    import pisi.api
    import pisi.errors
    from pisi.api import calculate_download_size
except ImportError:
    print 'Unable to import the PiSi API'
    sys.exit('Please ensure that you are running Pardus GNU/ Linux')


if sys.version_info[:2] < (2, 4):
    print "Package Testing Framework requires Python 2.6 or better (but not " \
    "Python 3 yet).\nVersion {0} detected.".format(sys.version_info[:2])
    sys.exit(1)
    
    
class Install(install):
    """Override the standard install to check for dependencies."""
    def run(self):
        if check_dependencies() is None:
            print 'Missing dependency: lxml'            
            choice = raw_input('Should I install it for you? (y / n): [y] ')
            if choice in ('y', 'Y', 'yes', 'YES', ''):
                install_dependencies()
            else:
                sys.exit('Aborting: The required dependencies were not met.')
        install.run(self)


class Build(build):
    """Override the standard build procedure to compile uic files to py."""
    def run(self):
        build.run(self)
        print 'Generating the UI files ...',
        subprocess.call(['/usr/bin/pyuic4', 'src/testcases/ui/main.ui',
                                    '-o', 'build/lib/src/testcases/ui_main.py'])
        print 'Done'


def check_dependencies():
    """Check for the required dependencies for the framework."""
    package = 'lxml'
    try:
        return __import__(package)
    except ImportError:
        return None
    

def install_dependencies():
    """Install the lxml library using the PiSi API."""
    package_list = ['lxml']
    downloadSize = pisi.api.calculate_download_size(package_list)[0]/(1024.0 * 1024.0)
    try:
        print "Please wait, installing package 'lxml' ({0:.2f} MB) ...".format(downloadSize)
        pisi.api.install(package_list)
        return 
    except pisi.errors.PrivilegeError:
        sys.exit('Aborting: Please run the script with root privileges.')
        
        
setup(
      name='package-testing-framework',
      version='1.0',
      author='Sukhbir Singh',
      author_email='sukhbir.in@gmail.com',
      maintainer='Semen Cirit',
      maintainer_email='scirit@pardus.org.tr',      
      url='http://www.pardus.org.tr',
      description='A package testing framework for Pardus GNU/ Linux',
      license='GNU GPL',
      package_dir = {'': ''},
      packages = ['src', 'src.testcases', 'src.testcases.ui'],
      package_data={
        'src.testcases.ui': ['*.ui']
        },
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
      cmdclass={
          'install': Install,
          'build': Build
        } 
     )