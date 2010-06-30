#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
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

import hardware

# Call distutils.setup

setup(name="python-hardware",
      version=hardware.__version__,
      description="Python library which provides hardware informations",
      long_description="""\
python-hardware is a Python library which provides various hardware related
informations about the CPU, kernel, PCI devices, BIOS DMI data, etc.""",
      author="Ozan Çağlayan",
      author_email="ozan@pardus.org.tr",
      url="http://svn.pardus.org.tr/uludag/trunk/playground/python-hardware",
      license="GPLv2",
      platforms=["Linux"],
      packages=["hardware"],
      )
