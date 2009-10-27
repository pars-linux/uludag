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

# Qt
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QDialog, QTreeWidgetItem, QBrush, QColor

# PyKDE
from PyKDE4.kdeui import KIcon
from PyKDE4.kdecore import i18n

# UI
from gui.ui.packages import Ui_PackagesDialog


class PackageWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, package):
        QTreeWidgetItem.__init__(self, parent)
        self.package = package
        self.required = False

        self.setCheckState(0, Qt.Unchecked)
        self.setText(0, package.name)
        self.setText(1, "%.3f" % (package.size / 1024.0 / 1024.0))
        self.setText(2, package.version)
        self.setText(3, package.release)

    def setChecked(self, checked):
        if checked:
            self.setCheckState(0, Qt.Checked)
        else:
            self.setCheckState(0, Qt.Unchecked)

    def isChecked(self):
        return self.checkState(0) == Qt.Checked

    def setRequired(self, required):
        self.required = required
        brush = QBrush()
        if required:
            brush.setColor(QColor(255, 0, 0))
        else:
            brush.setColor(QColor(0, 0, 0))
        self.setForeground(0, brush)

    def isRequired(self):
        return self.required


class ComponentWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, component):
        QTreeWidgetItem.__init__(self, parent)
        self.component = component

        self.setCheckState(0, Qt.Unchecked)
        self.setText(0, component)

    def setChecked(self, checked):
        if checked:
            self.setCheckState(0, Qt.Checked)
        else:
            self.setCheckState(0, Qt.Unchecked)

    def isChecked(self):
        return self.checkState(0) == Qt.Checked


class PackagesDialog(QDialog, Ui_PackagesDialog):
    def __init__(self, parent, repo, packages=[], components=[]):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Package repository
        self.repo = repo

        # Selected packages/components
        self.packages = packages
        self.components = components
        self.all_packages = []

        # Search widget
        self.searchPackage.addTreeWidget(self.treePackages)

        # Ok/cancel buttons
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)

        # Filter combo
        self.connect(self.comboFilter, SIGNAL("currentIndexChanged(int)"), self.slotComboFilter)

        # Package/Component changes
        self.connect(self.treeComponents, SIGNAL("currentItemChanged(QTreeWidgetItem *,QTreeWidgetItem *)"), self.slotSelectComponent)
        self.connect(self.treeComponents, SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.slotClickComponent)
        self.connect(self.treePackages, SIGNAL("currentItemChanged(QTreeWidgetItem *,QTreeWidgetItem *)"), self.slotSelectPackage)
        self.connect(self.treePackages, SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.slotClickPackage)

        # Go go go!
        self.initialize()

    def initialize(self):
        """
            Fill in the blanks :)
        """
        # Packages
        for name in self.repo.packages:
            package = self.repo.packages[name]
            item = PackageWidgetItem(self.treePackages, package)

        # Components
        for name in self.repo.components:
            item = ComponentWidgetItem(self.treeComponents, name)
            if name in self.components:
                item.setChecked(True)

        # Draw selections
        self.updatePackages()

    def accept(self):
        self.packages = []
        self.components = []
        self.all_packages = []
        for index in xrange(self.treePackages.topLevelItemCount()):
            item = self.treePackages.topLevelItem(index)
            if item.isChecked():
                self.packages.append(item.package.name)
            if item.isRequired():
                self.all_packages.append(item.package.name)
        for index in xrange(self.treeComponents.topLevelItemCount()):
            item = self.treeComponents.topLevelItem(index)
            if item.isChecked():
                self.components.append(item.component)
        QDialog.accept(self)

    def slotComboFilter(self, index):
        """
            Filter packages combo box fires this function.
        """
        selected_only = index == 1
        self.filterPackages(selected_only=selected_only)

    def filterPackages(self, name=None, selected_only=False):
        """
            Filters package list.
        """
        for index in xrange(self.treePackages.topLevelItemCount()):
            item = self.treePackages.topLevelItem(index)
            if selected_only:
                if item.isChecked() or item.isRequired():
                    item.setHidden(False)
                else:
                    item.setHidden(True)
            else:
                item.setHidden(False)

    def slotSelectComponent(self, new, old):
        """
            Component selection fires this function.
        """
        print new.text(0), "selected"

    def slotClickComponent(self, item):
        """
            Component click fires this function.
        """
        if item.isChecked():
            if item.component not in self.components:
                self.components.append(item.component)
                self.updatePackages()
        else:
            if item.component in self.components:
                self.components.remove(item.component)
                self.updatePackages()

    def slotSelectPackage(self, new, old):
        """
            Package selection fires this function.
        """
        print new.text(0), "selected"

    def slotClickPackage(self, item):
        """
            Package click fires this function.
        """
        if item.isChecked():
            if item.package.name not in self.packages:
                self.packages.append(item.package.name)
                self.updatePackages()
        else:
            if item.package.name in self.packages:
                self.packages.remove(item.package.name)
                self.updatePackages()

    def updatePackages(self):
        """
            Updates package selections.
        """

        # Iterating all objects is a bad way to mark packages...

        size = 0
        required_packages = []
        for package in self.packages:
            for dep in self.repo.full_deps(package):
                if dep not in required_packages and dep != package:
                    required_packages.append(dep)

        for component in self.components:
            for package in self.repo.components[component]:
                for dep in self.repo.full_deps(package):
                    if dep not in required_packages:
                        required_packages.append(dep)

        for index in xrange(self.treePackages.topLevelItemCount()):
            item = self.treePackages.topLevelItem(index)
            selected = item.package.name in self.packages
            required = item.package.name in required_packages
            item.setChecked(selected)
            item.setRequired(required)
            if required or selected:
                size += item.package.size

        self.labelTotalSize.setText("%.3f MB" % (size / 1024.0 / 1024.0))
