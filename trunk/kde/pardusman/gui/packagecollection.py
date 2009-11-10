 #!/usr/bin/python
 # -*- coding: utf-8 -*-
 #
 # Copyright (C) 2005-2009, TUBITAK/UEKAE
 #
 # This program is free software; you can redistribute it and/or modify it under
 # the terms of the GNU General Public License as published by the Free
 # Software Foundation; either version 2 of the License, or (at your option)
 # any later version.
 #
 # Please read the COPYING file.
 #
import hashlib
import os

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog, QFileDialog, QListWidgetItem, QMessageBox, QPixmap

from gui.ui.packagecollection import Ui_PackageCollectionsDialog
from gui.packages import PackagesDialog
from repotools.selections import PackageCollection, PackageSelection

import gettext
_ = lambda x:gettext.ldgettext("pardusman", x)


class PackageCollectionDialog(QDialog, Ui_PackageCollectionsDialog):
    def __init__(self, parent, repo,  collection=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        if collection:
            print "modify cagrısı"
        self.parent = parent
        self.repo = repo
        self.repoURI = "%s/%s" % (repo.base_uri, repo.index_name)
        self.collection = collection
        self.tmpPackageSelection = None
        self.tmpIconPath = None
        self.connect(self.pushSelectPackages, SIGNAL("clicked()"), self.slotSelectPackages)
        self.connect(self.pushSelectIcon, SIGNAL("clicked()"), self.slotSelectIcon)

        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        print "init de debugCollection cagrılacak"
        self.debugCollection()
        self.initialize()

    def debugCollection(self):
        if self.collection:
            print "collection.uniqueTag:%s" % self.collection.uniqueTag
            print "collection.iconPath:%s" % self.collection.icon
            print "collection.title:%s" % self.collection.title
            print "collection.tmpPackageSelection.repoURI:%s" % self.collection.packageSelection.repoURI
        else:
            print "collection yok debug!"
    def initialize(self):
        if self.collection:
            self.lineTitle.setText(self.collection.title)
            if os.path.exists(self.collection.icon):
                self.lineIcon.setPixmap(QPixmap(self.collection.icon))
            else:
                self.lineIcon.setText(_("Icon file not found!"))
            self.__setSelectedPackagesText(self.collection.packageSelection.selectedPackages, self.collection.packageSelection.selectedComponents)
            self.textDescription.setPlainText(self.collection.description)

    def __getUniqueID(self, title):
        return hashlib.sha1(title).hexdigest()

    def __setSelectedPackagesText(self, packages, components):
        self.linePackages.setText( _("%s Selected Components and %s Selected Packages") % (len(components), len(packages)))

    def accept(self):
        title = unicode(self.lineTitle.text())
        iconPath = unicode(self.tmpIconPath)
        description = unicode(self.textDescription.toPlainText())
        uniqueTag = unicode(self.__getUniqueID(title))
        self.collection = PackageCollection(uniqueTag, iconPath, title, description, self.tmpPackageSelection)

        print "accept de debugCollection cagrılacak"
        self.debugCollection()

        QDialog.accept(self)

    def slotSelectIcon(self):
        filename = QFileDialog.getOpenFileName(self, _("Select Collection Icon"), "/usr/share/icons/default.kde4", "*.png")
        if filename:
            self.tmpIconPath = filename
            self.lineIcon.setPixmap(QPixmap(filename))

    def slotSelectPackages(self):
        if self.collection:
            print "buraya geldi...."
            dialog = PackagesDialog(self, self.repo, self.collection.packageSelection.selectedPackages, self.collection.packageSelection.selectedComponents)
        else:
            dialog = PackagesDialog(self, self.repo)

        if dialog.exec_():
            self.__setSelectedPackagesText(dialog.packages, dialog.components)
            self.tmpPackageSelection = PackageSelection(self.repoURI, dialog.components, dialog.packages, dialog.all_packages)
            self.collection.packageSelection = self.tmpPackageSelection

