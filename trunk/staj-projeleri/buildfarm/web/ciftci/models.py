# -*- coding: utf-8 -*-
#
# Copyright © 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

import os

from django.db import models

import pisi

#################################################################
# Django coding style of a model class:                         #
# 1. All database fields                                        #
# 2. Meta Class                                                 #
# 3. Admin Class                                                #
# 4. __unicode__()                                              #
# 5. __str__()                                                  #
# 6. save()                                                     #
# 7. get_absolute_url()                                         #
# 8. Other custom methods                                       #
#################################################################

# Models which define necessary elements for the web interface

# Don't really know if we need these, just for practice :)
class Repository(models.Model):
    repo_name = models.CharField(maxlength=30)

    # Can be replaced by FilePathField
    repo_path = models.CharField(maxlength=255)

    def save(self):
    # Raise an exception.
        if self.exists():
            super(Repository, self).save()

    def __str__(self):
        return self.repo_name

class Package(models.Model):
    # The package can be identified
    # 1. by its pspec.xml (parsed later) OR
    # 2. by parsing the pspec.xml and then storing the elements in db
    pspec = models.XMLField(schema_path='')

