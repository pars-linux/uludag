# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
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

from kdecore import i18n

def FormatNumber(number):
    "Return a human readable representation of number"

    if number >= 1024*1024:
        result = float(number)/float(1024*1024)
        return ("%.1lf MB" % result).replace(".0","")
    elif number >= 1024:
        result = float(number)/float(1024)
        return ("%.1lf KB" % result).replace(".0","")
    else:
        return i18n("Less than one kilobyte")

