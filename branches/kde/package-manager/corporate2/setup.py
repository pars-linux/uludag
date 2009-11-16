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
    name="package-manager",
    version="1.4.0",
    author="Faik Uygur",
    author_email="faik@pardus.org.tr",
    url="http://www.pardus.org.tr/projeler/pisi/index.html",
    min_kde_version = "3.5.2",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = [
                        # sources
                        'src/package-manager.py', 
                        'src/Group.py',
                        'src/Progress.py',
                        'src/Preferences.py',
                        'src/CommonText.py',
                        'src/HelpDialog.py',
                        'src/ComarIface.py',
                        'src/Tray.py',
                        'src/Notifier.py',
                        'src/BasketDialog.py',
                        'src/Settings.py',
                        'src/Icons.py',
                        'src/LocaleData.py',
                        'src/PmDcop.py',
                        'src/PmUtils.py',
                        'src/Pmlogging.py',
                        'src/pm-install.py',
                        'src/CustomEventListener.py',
                        'src/Basket.py',
                        'src/PackageCache.py',
                        'src/MainWidget.py',
                        'src/Globals.py',
                        'src/Debug.py',
                        'src/SpecialList.py',
                        'src/Group.py',
                        'src/PisiIface.py'

                        # ui files
                        'src/ProgressDialog.ui',
                        'src/PreferencesDialog.ui',
                        'src/RepoDialog.ui',

                        # data
                        'help',
                        'data/pisianime.gif',
                        'data/animation.js',
                        'data/layout.css',
                        'data/package-managerui.rc',
                        ("/usr/kde/3.5/share/icons/hicolor/128x128/apps", ["data/package-manager.png"]),

                        # desktop files
                        ("/usr/kde/3.5/share/applications/kde/", ["data/packagemanager.desktop"]),
                        ("/usr/kde/3.5/share/applnk/.hidden/", ["data/packagemanager-helper.desktop"]),
                        ("/usr/kde/3.5/share/mimelnk/application/", ["data/x-pisi.desktop"]),
                        ("/usr/kde/3.5/share/applications/kde/", ["data/tasmamanager.desktop"])
    ],

    executable_links = [('package-manager','package-manager.py'), ('pm-install','pm-install.py')],
    i18n = ('po',['src']),
    )
