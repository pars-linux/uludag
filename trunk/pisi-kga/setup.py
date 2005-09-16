#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# setup - description                                                     #
# ------------------------------                                          #
# begin     : Pzt Ağu 15 10:07:29 EEST 2005                               #
# copyright : (C) 2005 by UEKAE/TÜBİTAK                                   #
# email     : ismail@uludag.org.tr                                        #
#                                                                         #
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
###########################################################################

import kdedistutils

kdedistutils.setup(name="pisi_kga",
    version="0.4",
    author="İsmail Dönmez",
    author_email="ismail@uludag.org.tr",
    url="http://www.uludag.org.tr/projects/pisi",
    min_kde_version = "3.4.0",
    min_qt_version = "3.3.0",
    license = "GPL",
    application_data = ['src/PisiKga.py','src/Preferences.py','src/PreferencesWidget.ui',
                        'src/ThreadRunner.py','src/RepoDialog.ui','src/MainWindow.ui',
                        'src/Progress.ui','src/ProgressDialog.py','src/PisiUi.py'],
    executable_links = [('pisi_kga','PisiKga.py')],
    docbooks = [ ('doc/en','en') ],
    i18n = ('po',['src']),
    kcontrol_modules = [ ('src/pisi_kga.desktop','PisiKga.py')] )
