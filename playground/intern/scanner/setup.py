#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
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
from distutils.core import Extension
import kdedistutils

version = '0.1'

distfiles = """
    README
    AUTHORS
    src/*.ui
    src/*.png
    src/*.py
    src/*.desktop
    po/*.po
    po/*.pot
    help/*.css
    help/tr/*.html
    help/en/*.html
"""

def make_dist():
    distdir = "tarayici-%s" % version
    list = []
    for t in distfiles.split():
        list.extend(glob.glob(t))
    if os.path.exists(distdir):
        shutil.rmtree(distdir)
    os.mkdir(distdir)
    for file_ in list:
        cum = distdir[:]
        for d in os.path.dirname(file_).split('/'):
            dn = os.path.join(cum, d)
            cum = dn[:]
            if not os.path.exists(dn):
                os.mkdir(dn)
        shutil.copy(file_, os.path.join(distdir, file_))
    os.popen("tar -czf %s %s" % ("tarayici-" + version + ".tar.gz", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

app_data = [
    'src/tarayici',
    'src/scanner.py',
    'src/checkbox.py',
    'src/combobox.py',
    'src/extractor.py',
    'src/labeledline.py',
    'src/lineedit.py',
    'src/option.py',
    'src/options.py',
    'src/optionsreadyevent.py',
    'src/optionsthread.py',
    'src/previewArea.py',
    'src/previewImage.py',
    'src/progress.py',
    'src/sane.py',
    'src/scanevent.py',
    'src/scanresultmulti.py',
    'src/scanresult.py',
    'src/scanthread.py',
    'src/slider.py',
    'src/toolbarimages.py',
    'src/utility.py',
    'help'
]

kdedistutils.setup(
    name="tarayici",
    version=version,
    author="Aslı Okur",
    author_email="asli.pardus@gmail.com",
    url="http://www.pardus.org.tr/",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = app_data,
    executable_links = [('tarayici','tarayici')],
    i18n = ('po', ['src']),
)
