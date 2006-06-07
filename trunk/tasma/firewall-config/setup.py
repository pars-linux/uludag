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
# Authors:  Bahadır Kandemir <bahadir@pardus.org.tr>

import kdedistutils

kdedistutils.setup(
    name="firewall-config",
    version="1.4",
    author="Bahadır Kandemir",
    author_email="bahadir@pardus.org.tr",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ["src/firewall.ui", "src/firewall_config.py",
                        ("/usr/kde/3.5/share/applications/kde/", ["src/firewall_config-desk.desktop"]),
                        ("/usr/kde/3.5/share/icons/default.kde/128x128/apps", ["src/firewall_config.png"])],
    executable_links = [("firewall-config", "firewall_config.py")],
    i18n = ("po", ["src"]),
    kcontrol_modules = [("src/firewall_config-kcm.desktop", "src/firewall_config.py")]
    )
