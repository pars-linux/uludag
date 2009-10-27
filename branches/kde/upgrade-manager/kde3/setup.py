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

import kdedistutils

kdedistutils.setup(
    name="upgrade-manager",
    version="0.1",
    author="Faik Uygur",
    author_email="faik@pardus.org.tr",
    url="http://www.pardus.org.tr",
    min_kde_version = "3.5.2",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = [
                        # sources
                        'src/about.py',
                        'src/comariface.py',
                        'src/commander.py',
                        'src/pisiiface.py',
                        'src/dumlogging.py',
                        'src/handler.py',
                        'src/maindialog.py',
                        'src/main.py',
                        'src/state.py',

                        # ui files
                        'src/ui_maindialog.ui',

                        # data
                        ("/usr/kde/3.5/share/apps/upgrade-manager/pics", ["data/arrow.png", "data/check.png"]),
                        ("/usr/kde/3.5/share/icons/hicolor/128x128/apps", ["data/package-manager.png"]),

                        # desktop files
                        ("/usr/kde/3.5/share/applications/kde/", ["data/upgrade-manager.desktop"]),
                        ],

    executable_links = [('upgrade-manager','main.py')],
    i18n = ('po',['src']),
    )
