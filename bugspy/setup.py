#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

import os
import sys
import glob
import shutil

from distutils.core import setup

import bugspy

# Scripts to install under /usr/bin
#SCRIPTS = ["bin/%s" % s for s in """\
#bugs.py
#""".split()]

SCRIPTS = ["bin/bugs.py", "bin/file-sec-bug.py"]

# Call distutils.setup

setup(name="bugspy",
      version=bugspy.__version__,
      description="Bugzilla tool for Pardus",
      long_description="Console based bugzilla tool for Pardus which can add/edit/get bugs",
      author="Eren Türkay",
      author_email="eren@pardus.org.tr",
      url="http://svn.pardus.org.tr/uludag/trunk/bugspy",
      license="GPLv2",
      platforms=["Linux"],
      packages=["bugspy"],
      scripts=SCRIPTS,
      data_files=[("/usr/share/bugspy", ["AUTHORS", "README", "COPYING", "THANKS"])])
