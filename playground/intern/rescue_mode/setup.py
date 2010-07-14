# -*- coding: utf-8 -*-
# option) any later version. Please read the COPYING file.

#import os
#import sys
#import glob
#import shutil

from distutils.core import setup

# Scripts to install under /usr/bin
SCRIPTS = ["scripts/%s" % s for s in """\
prm
install-mbr
""".split()]

# Call distutils.setup

setup(name="rescuemode",
      version="1.0",
      description="Pardus Rescue Mode",
      long_description="A program which rescue Windows bootloader and Pardus",
      author="Mehmet Burak Aktürk",
      author_email="mb.akturk@gmail.com",
      url="http://svn.pardus.org.tr/uludag/trunk/playground/intern/rescue_mode",
      license="GPLv2",
      platforms=["Linux"],
      packages=["prm"],
      scripts=SCRIPTS)

