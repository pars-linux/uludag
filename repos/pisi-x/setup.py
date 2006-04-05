#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>

import kdedistutils

kdedistutils.setup(
    name="pisix",
    version="1.1.0_b1",
    author="İsmail Dönmez",
    author_email="ismail@uludag.org.tr",
    url="http://www.uludag.org.tr/projeler/pisi/index.html",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ['src/pisix.py', 'src/ThreadRunner.py','src/Progress.py','src/ProgressDialog.ui',
                        'src/PisiUi.py','src/PreferencesDialog.ui','src/Preferences.py','src/pisianime.gif',
                        'src/RepoDialog.ui','src/HelpDialog.py','src/Enums.py','src/ClickLineEdit.py',
                        'help','src/animation.js','src/layout.css','pisixui.rc',
                        ("/usr/kde/3.5/share/applications/kde/",["src/pisix.desktop"]),
                        ("/usr/kde/3.5/share/applnk/.hidden/",["src/pisix-helper.desktop"]),
                        ("/usr/kde/3.5/share/icons/default.kde/128x128/apps",["src/pisix.png"]),
                        ("/usr/kde/3.5/share/mimelnk/application/",["src/x-pisi.desktop"])],
    executable_links = [('pisix','pisix.py')],
    i18n = ('po',['src']),
    )
