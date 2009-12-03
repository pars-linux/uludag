#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009, TUBITAK/UEKAE
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

from code import displaysettings

def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass

class Build(kdedistutils.BuildKDE):
    def run(self):
        kdedistutils.BuildKDE.run(self)

        makeDirs("build/lib/xcb")

        # Create xcb binding
        os.system("python xcb/py_client.py xcb/nvctrl.xml")
        self.move_file("nvctrl.py", "build/lib/xcb/")

class Install(kdedistutils.InstallKDE):
    def run(self):
        kdedistutils.InstallKDE.run(self)

        self.run_command("install_lib")


app_data = [
    'code/display-settings.py',
    ('displaysettings', ['code/displaysettings']),
    ('displaysettings/ui', ['ui']),
    'pics',
    'help'
]

kdedistutils.setup(
    name                = "display-settings",
    version             = displaysettings.versionString(),
    author              = "Fatih Aşıcı",
    author_email        = "fatih@pardus.org.tr",
    url                 = "http://www.pardus.org.tr/",
    min_kde_version     = "3.5.0",
    min_qt_version      = "3.3.5",
    license             = "GPL",
    application_data    = app_data,
    executable_links    = [('display-settings', 'display-settings.py')],
    i18n                = ('po', ['code', 'code/displaysettings', 'ui']),
    kcontrol_modules    = [ ('code/display-settings.desktop', 'code/display-settings.py')],
    cmdclass            = {
                            'build': Build,
                            'install': Install,
                          }
)
