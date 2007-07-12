#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os
import sys
import glob
import shutil
import kdedistutils

version = "0.5"

distfiles = """
    README
    AUTHORS
    COPYING
    *.py
    migration/gui/*.ui
    migration/gui/*.py
    migration/utility/*.py
    migration/*.py
    migration/migration.png
    po/*.po
    po/*.pot
"""

def make_dist():
    distdir = "migration-%s" % version
    files = []
    for item in distfiles.split():
        files.extend(glob.glob(t))
    if os.path.exists(distdir):
        shutil.rmtree(distdir)
    os.mkdir(distdir)
    for file_ in files:
        cum = distdir[:]
        for d in os.path.dirname(file_).split('/'):
            dn = os.path.join(cum, d)
            cum = dn[:]
            if not os.path.exists(dn):
                os.mkdir(dn)
        shutil.copy(file_, os.path.join(distdir, file_))
    os.popen("tar -cjf %s %s" % ("migration-" + version + ".tar.bz2", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

kdedistutils.setup(
    name="migration",
    version=version,
    author="Murat Ongan",
    author_email="mongan@cclub.metu.tr",
    url="http://www.pardus.org.tr/",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    package_dir = {"":""},
    application_data = [("migration", ["migration/migration.py", "migration/wizard.py", "migration/applythread.py", "migration/migration.png"]), ("migration/gui", ["migration/gui/__init__.py", "migration/gui/dirview.py", "migration/gui/filespage.py", "migration/gui/optionspage.py", "migration/gui/progresspage.py", "migration/gui/sidebar.py", "migration/gui/userpage.py"]), ("migration/utility", ["migration/utility/__init__.py", "migration/utility/bookmark.py", "migration/utility/files.py", "migration/utility/info.py", "migration/utility/partition.py", "migration/utility/registry.py", "migration/utility/wall.py", "migration/utility/wall.py"])],
    executable_links = [("migration", "migration/migration.py")],
    i18n = ("po", ["migration", "migration/gui", "migration/utility"])
)
