#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python Libs
import os
import shutil

# DistUtils
from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.sdist import sdist
from distutils.sysconfig import get_python_lib

PROJECT = 'rasta'
PROJECT_LIB = 'rastaLib'

class Clean(clean):
    def run(self):
        print 'Cleaning ...'
        os.system('find -name *.pyc|xargs rm -rf')
        for compiled in ('rastaLib/mainWindow.py', 'rastaLib/icons_rc.py'):
            if os.path.exists(compiled):
                print ' removing: ', compiled
                os.unlink(compiled)
        for dirs in ('build', 'dist'):
            if os.path.exists(dirs):
                print ' removing: ', dirs
                shutil.rmtree(dirs)
        clean.run(self)

class Build(build):
    def run(self):
        print 'Building ...'
        os.system('pyuic4 gui/mainWindow.ui -o rastaLib/mainWindow.py')
        os.system('pyrcc4 rastaLib/icons.qrc -o rastaLib/icons_rc.py')
        build.run(self)

class Dist(sdist):
    def run(self):
        os.system('python setup.py build')
        sdist.run(self)

class Uninstall(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        print 'Uninstalling ...'
        project_dir = os.path.join(get_python_lib(), PROJECT_LIB)
        data_dir    = '/usr/share/%s' % PROJECT
        directories = (project_dir, data_dir)
        for directory in directories:
            if os.path.exists(directory):
                print ' removing: ', directory
                shutil.rmtree(directory)
        executable = '/usr/bin/%s' % PROJECT
        if os.path.exists(executable):
            print ' removing: ', executable
            os.unlink(executable)

setup(name=PROJECT,
      version='1.0',
      description='Rasta: The Rst Editor',
      long_description='Live view supported Qt4 based Webkit integrated Rst editor for Pardus Developers and all others.',
      license='GNU GPL2',
      author='Gökmen Göksel',
      author_email='gokmen@pardus.org.tr',
      url='http://developer.pardus.org.tr',
      packages=[PROJECT_LIB],
      scripts=[PROJECT],
      data_files = [('/usr/share/%s' % PROJECT, ['AUTHORS', 'README', 'COPYING', 'HELP'])],
      cmdclass = {
          'uninstall':Uninstall,
          'build'    :Build,
          'clean'    :Clean,
          'sdist'    :Dist,
          }
     )
