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


# Buildfarm version
__version__ = '0.1'

__all__ = ['config', 'dependency', 'main', 'qmanager', 'repomanager']


Get = lambda j, w: [x for x in j.childNodes if x.nodeType == x.ELEMENT_NODE if x.tagName == w]

