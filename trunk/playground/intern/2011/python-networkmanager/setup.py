#! /usr/bin/env python
# -*- coding: utf-8 -*-

# setup.py --- Setup script for python-networkmanager
# Copyright (c) 2002, 2003, 2004 Florent Rougon
# Copyright (c) 2011 Gökmen Göksel
#
# This file is part of python-networkmanager.
#
# python-networkmanager is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# python-networkmanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os, string, sys
from distutils.core import setup

# Note:
#  The Distutils included in Python 2.1 don't understand the "license" keyword
#  argument of setup correctly (they only understand licence); as I don't want
#  to mispell it, if you run the Distutils from Python 2.1, you will get
#  License: UNKNOWN. This problem does not appear with the version included in
#  Python 2.2.

PACKAGE = "python-networkmanager"
VERSION = "0.2"

def main():
    setup(name=PACKAGE,
          version=VERSION,
          description="A Python interface to NetworkManager via DBus",
          author="Mark Renouf",
          author_email="mark.renouf@gmail.com",
          maintainer="Gökmen Göksel",
          maintainer_email="gokmen@pardus.org.tr",
          url="https://github.com/gokmen/python-networkmanager",
          license="LGPL",
          platforms="UNIX",
          long_description="""\
A Python interface to NetworkManager over DBus. Designed to hide
the complexities of python-dbus and provide a simplified api to
interacting with network manager to control network configuration
tasks""",
          keywords=["network-manager", "DBus"],
          packages=["networkmanager"],
          scripts=['nm-util', 'network'],
          data_files=[('/etc/bash_completion.d', ['bash_completion/nm-util']),])

if __name__ == "__main__": main()
