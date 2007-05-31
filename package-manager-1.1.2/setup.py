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
    version="1.1.2",
    author="Faik Uygur",
    author_email="faik@pardus.org.tr",
    url="http://www.pardus.org.tr/projeler/pisi/index.html",
    min_kde_version = "3.5.2",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ['src/package-manager.py', 'src/Commander.py','src/Progress.py','src/ProgressDialog.ui',
                        'src/PreferencesDialog.ui','src/Preferences.py','src/pisianime.gif','src/CommonText.py',
                        'src/RepoDialog.ui','src/HelpDialog.py','src/ComarIface.py','help', 'src/CustomEventListener.py',
                        'src/Basket.py','src/animation.js','src/layout.css','src/package-managerui.rc',
                        'src/Tray.py','src/BalloonMessage.py', 'src/BasketDialog.py', 'src/Settings.py',
                        'src/Icons.py', 'src/LocaleData.py', 'src/PmDcop.py', 'src/pm-install.py', 'src/PackageCache.py',
                        ("/usr/kde/3.5/share/applications/kde/",["src/packagemanager.desktop"]),
                        ("/usr/kde/3.5/share/applnk/.hidden/",["src/packagemanager-helper.desktop"]),
                        ("/usr/kde/3.5/share/icons/hicolor/128x128/apps",["src/package-manager.png"]),
                        ("/usr/kde/3.5/share/mimelnk/application/",["src/x-pisi.desktop"]),
                        ("/usr/kde/3.5/share/applications/kde/",["src/tasmamanager.desktop"])],
    executable_links = [('package-manager','package-manager.py'), ('pm-install','pm-install.py')],
    i18n = ('po',['src']),
    )
