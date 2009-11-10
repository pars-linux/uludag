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

import buildfarm

# Scripts to install under /usr/bin
SCRIPTS = ["scripts/%s" % s for s in """\
buildfarm
buildfarm-report
""".split()]

# Call distutils.setup

setup(name="buildfarm",
      version=buildfarm.__version__,
      description="Pardus Buildfarm",
      long_description="A buildfarm framework which builds source packages for Pardus",
      author="Ozan Çağlayan",
      author_email="ozan@pardus.org.tr",
      url="http://svn.pardus.org.tr/uludag/trunk/buildfarm",
      license="GPLv2",
      platforms=["Linux"],
      packages=["buildfarm"],
      scripts=SCRIPTS,
      data_files=[("/etc/buildfarm", ["data/buildfarm.conf"])])
