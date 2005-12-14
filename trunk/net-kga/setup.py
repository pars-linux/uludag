#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  Gürer Özen <gurer@uludag.org.tr>

import kdedistutils

kdedistutils.setup(
    name="net_kga",
    version="1.0_alpha1",
    author="Gürer Özen",
    author_email="gurer@uludag.org.tr",
    url="http://www.uludag.org.tr/projects/comar",
    min_qt_version = "3.3.0",
    license = "GPL",
    application_data = ['net_kga.py','mainwin.py','connection.py', 'widgets.py', 'links.py', 'net-up.png', 'net-down.png' ],
    executable_links = [('net-kga','net_kga.py')],
    kcontrol_modules = [ ('net_kga.desktop','net_kga.py')],
    )
