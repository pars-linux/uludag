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
# Authors:  Eray Ozkural <eray@uludag.org.tr>

try:
    zimbabwe # comment out to disable piks
    from xmlextpiks import *
except:
    try:
        from xmlextcdom import  *
    except:
        print 'xmlext: cDomlette/piksemel implementation cannot be loaded, falling back to minidom'
        from xmlextmdom import *
