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

from gui.ui.packagecollection import Ui_PackageCollectionDialog
from gui.packages import PackagesDialog
from gui.languages import LanguagesDialog
from gui.translation import TranslationDialog
from repotools.selections import PackageCollection, PackageSelection, CollectionDescription, LanguageSelection

import gettext
_ = lambda x:gettext.ldgettext("pardusman", x)


class PackageCollectionDialog(QDialog, Ui_PackageCollectionDialog):
    def __init__(self, parent, repo,  collection=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.repo = repo
        self.repoURI = "%s/%s" % (repo.base_uri, repo.index_name)
        self.collection = collection
        self.tmpCollection = None

        if self.collection:
            print "modify cagrısı"
        else:
            self.tmpCollection = PackageCollection()
        self.tmpPackageSelection = None
        self.tmpLanguageSelection = None
        self.tmpDescription = None
        self.tmpIconPath = None

        self.connect(self.pushSelectPackages, SIGNAL("clicked()"), self.slotSelectPackages)
        self.connect(self.pushSelectLanguages, SIGNAL("clicked()"), self.slotSelectLanguages)
        self.connect(self.pushSelectTranslations, SIGNAL("clicked()"), self.slotSelectTranslations)
        self.connect(self.toolSelectIcon, SIGNAL("clicked()"), self.slotSelectIcon)
        self.connect(self.toolClearIcon, SIGNAL("clicked()"), self.slotClearIcon)

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
            if self.collection.packageSelection:
                print "collection.tmpPackageSelection.repoURI:%s" % self.collection.packageSelection.repoURI
        else:
            print "collection yok debug!"
    def initialize(self):
        if self.collection:
            self.lineTitle.setText(self.collection.title)
            if os.path.exists(self.collection.icon):
                self.labelIcon.setPixmap(QPixmap(self.collection.icon))
            else:
                self.labelIcon.setText(_("Icon file not found!"))
            if self.collection.descriptionSelection:
                self.textDescription.setPlainText(self.collection.descriptionSelection.description)

    def __getUniqueID(self, title):
        return hashlib.sha1(title).hexdigest()

    def __setSelectedPackagesText(self, packages, components):
        self.linePackages.setText( _("%s Selected Components and %s Selected Packages") % (len(components), len(packages)))

    def accept(self):
        title = unicode(self.lineTitle.text())
        #iconPath = self.tmpIconPath)
        #description = unicode(self.textDescription.toPlainText())
        uniqueTag = unicode(self.__getUniqueID(title))
        if not self.collection:
            self.collection = PackageCollection(uniqueTag, self.tmpIconPath, title, self.tmpDescription, self.tmpPackageSelection, self.tmpLanguageSelection)
        else:
            self.collection.title = title
            self.collection.uniqueTag = uniqueTag

        print "accept de debugCollection cagrılacak"
        self.debugCollection()

        QDialog.accept(self)

    def slotSelectIcon(self):
        filename = QFileDialog.getOpenFileName(self, _("Select Collection Icon"), "./projects/icons/", "*.png")
        if filename:
            if self.collection:
                self.collection.icon = unicode(filename)
            else:
                self.tmpCollection.icon = unicode(filename)
                self.tmpIconPath = unicode(filename)

            self.labelIcon.setPixmap(QPixmap(filename))
            print "tmpIconPAth :%s" % self.tmpIconPath

    def slotClearIcon(self):
        self.labelIcon.setPixmap(None)

    def slotSelectPackages(self):
        if self.collection:
            print "buraya geldi...."
            if self.collection.packageSelection.selectedPackages and self.collection.packageSelection.selectedComponents:
                dialog = PackagesDialog(self, self.repo, self.collection.packageSelection.selectedPackages, self.collection.packageSelection.selectedComponents)
                if dialog.exec_():
                    self.collection.packageSelection = PackageSelection(self.repoURI, dialog.components, dialog.packages, dialog.all_packages)

            else:
                dialog = PackagesDialog(self, self.repo)
                if dialog.exec_():
                    self.tmpCollection.packageSelection = PackageSelection(self.repoURI, dialog.components, dialog.packages, dialog.all_packages)
                    self.tmpPackageSelection = PackageSelection(self.repoURI, dialog.components, dialog.packages, dialog.all_packages)
        else:
            dialog = PackagesDialog(self, self.repo)
            if dialog.exec_():
                self.tmpCollection.packageSelection = PackageSelection(self.repoURI, dialog.components, dialog.packages, dialog.all_packages)
                self.tmpPackageSelection = PackageSelection(self.repoURI, dialog.components, dialog.packages, dialog.all_packages)

    def slotSelectLanguages(self):
        if self.collection:
            dialog = LanguagesDialog(self, self.collection.languageSelection.languages)
            if dialog.exec_():
                self.collectionLanguageSelection = LanguageSelection(dialog.languages[0], dialog.languages)
        else:
            dialog = LanguagesDialog(self)
            if dialog.exec_():
                self.tmpCollection.languageSelection = LanguageSelection(dialog.languages[0], dialog.languages)
                self.tmpLanguageSelection = LanguageSelection(dialog.languages[0], dialog.languages)

    def slotSelectTranslations(self):
        if self.collection and self.collection.languageSelection:
            dialog = TranslationDialog(self, unicode(self.textDescription.toPlainText()), self.collection)
            if dialog.exec_():
                self.collection.descriptionSelection = CollectionDescription(unicode(self.textDescription.toPlainText()), dialog.translations)
        elif self.tmpCollection and self.tmpCollection.languageSelection:
            dialog = TranslationDialog(self, unicode(self.textDescription.toPlainText()), self.tmpCollection)
            if dialog.exec_():
                self.tmpCollection.descriptionSelection = CollectionDescription(unicode(self.textDescription.toPlainText()), dialog.translations)
                self.tmpDescription = CollectionDescription(unicode(self.textDescription.toPlainText()), dialog.translations)
        else:
            QMessageBox.warning(self, self.windowTitle(),  _("Select Language for Collection at first..."))
