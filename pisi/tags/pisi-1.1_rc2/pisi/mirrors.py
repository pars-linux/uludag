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

import os.path
import pisi.context as ctx
from pisi import Error

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

class Mirrors:
    def __init__(self, config=ctx.const.mirrors_conf):
        self.mirrors = {}
        self._parse(config)

    def get_mirrors(self, name):
        if self.mirrors.has_key(name):
            return list(self.mirrors[name])

        return None

    def _add_mirror(self, name, url):
        if self.mirrors.has_key(name):
            self.mirrors[name].append(url)
        else:
            self.mirrors[name] = [url]

    def _parse(self, config):
        if os.path.exists(config):
            for line in open(config, "r").readlines():
                if not line.startswith('#') and not line == '\n':
                  mirror = line.strip().split()
                  if len(mirror) == 2:
                      (name, url) = mirror
                      self._add_mirror(name, url)
        else:
            raise Error(_('Mirrors file %s does not exist. Could not resolve mirrors://') % config)

