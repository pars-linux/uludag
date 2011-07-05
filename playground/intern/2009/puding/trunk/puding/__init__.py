#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3 (Read COPYING file.)
#

import gettext

from constants import LOCALE


t = gettext.translation("puding", LOCALE, fallback = True)
_ = t.ugettext

