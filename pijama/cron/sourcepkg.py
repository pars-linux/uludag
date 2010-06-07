#!/usr/bin/python
# -*- coding: utf-8 -*-

import pisi

class SourceDetails:

    def __init__(self,pkg):

        print pkg

        self.pkgdb=pisi.db.packagedb.PackageDB()
        self.package=self.pkgdb.get_package(pkg)

    def get_added_date(self):
        return self.package.history[-1].date

    def last_change_date(self):
        return self.package.history[0].date


