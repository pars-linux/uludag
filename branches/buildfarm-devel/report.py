#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import mailer

""" Gettext Support """
import gettext
__trans = gettext.translation("buildfarm", fallback = True)
_  =  __trans.ugettext

packages = []
for i in os.listdir("/var/www/localhost/htdocs/pardus-2007-test/"):
    if not os.path.exists("/var/www/localhost/htdocs/pardus-2007/%s" % i):
        packages.append(i)

packages.sort()
mailer.announce(_("New packages in -testing repository:\n\n%s") % "\n".join(packages))
