#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

# UI
from firewallmanager.ui_settingsitem import Ui_SettingsItemWidget

# Pds Stuff
from context import KIcon

class SettingsItemWidget(QtGui.QWidget, Ui_SettingsItemWidget):

    def __init__(self, parent, name, type_):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.name = name
        self.type = type_
        self.changed =False
        self.lineItem.hide()
        self.comboItems.hide()
        self.listItems.hide()
        self.setDisabledAll()

        if type_ == "combo":
            self.comboItems.show()
        elif type_ == "editlist":
            self.listItems.show()
        elif type_ == "text":
            self.lineItem.show()

        # SIGNAL
        self.connect(self.pushAdd, QtCore.SIGNAL("clicked()"), self.addItemToList)
        self.connect(self.pushDelete, QtCore.SIGNAL("clicked()"), self.removeItemToList)
        self.connect(self.pushUp, QtCore.SIGNAL("clicked()"), self.funcPushUp)
        self.connect(self.pushDown, QtCore.SIGNAL("clicked()"), self.funcPushDown)
        self.connect(self.listWidget, QtCore.SIGNAL(("currentItemChanged(QListWidgetItem*,QListWidgetItem*)")), self.hideButtons)
        self.connect(self.lineEdit, QtCore.SIGNAL(("textChanged(QString)")), self.hideAdd)
        self.connect(self.lineEdit, QtCore.SIGNAL(("textChanged(QString)")), self.changeItem)

        # Set Icons
        self.pushAdd.setIcon(KIcon("list-add"))
        self.pushDelete.setIcon(KIcon("list-remove"))
        self.pushUp.setIcon(KIcon("arrow-up"))
        self.pushDown.setIcon(KIcon("arrow-down"))

    def count(self):
        '''
            Size of list
        '''
        return self.listWidget.count()

    def setDisabledAll(self):
        '''
            Set the buttons disabled.
        '''
        self.pushAdd.setEnabled(False)
        self.pushDelete.setEnabled(False)
        self.pushUp.setEnabled(False)
        self.pushDown.setEnabled(False)

    def hideAdd(self):
        '''
            Hide all elements in list.
        '''
        if not(self.lineEdit.text()==""):
            self.pushAdd.setEnabled(True)
        else :
            self.pushAdd.setEnabled(False)

    def alreadyInList(self):
        '''
            Check the item is in list.
        '''
        for i in range(self.listWidget.count()):
            if (self.lineEdit.text()==self.listWidget.item(i).text()):
                return True
        return False

    def alreadyInListCount(self):
        '''
            Check the changed item is already in list.
        '''
        count =0
        for i in range(self.listWidget.count()):
            if (self.lineEdit.text()==self.listWidget.item(i).text()):
                count = count+1
        return count

    def changeItem(self):

        if not self.changed:
            if self.listWidget.currentItem():
                self.listWidget.currentItem().setText(self.lineEdit.text())

            if self.lineEdit.text()== "":
                self.pushAdd.setEnabled(False)

    def addItemToList(self):
        '''
            Check the item is in list and  add item to list.
        '''

        if not self.alreadyInList():
            if self.listWidget.currentItem():
                self.listWidget.currentItem().setText(self.lineEdit.text())
            else:
                if not(self.lineEdit.text()== ""):
                    self.listWidget.insertItem(0,self.lineEdit.text())

        if self.alreadyInListCount() > 1:
            self.removeItemToList()

        self.changed=True
        self.lineEdit.setText("")
        self.changed=False
        self.listWidget.setCurrentItem(None)
        self.setDisabledAll()


    def removeItemToList(self):
        '''
            Remove the selected item from list.
        '''
        self.listWidget.takeItem(self.listWidget.currentRow())
        if (self.listWidget.count()==0):
            self.pushDelete.setEnabled(False)
        if (self.listWidget.count()<2):
            self.pushUp.setEnabled(False)
            self.pushDown.setEnabled(False)

    def listToLineEdit(self):
        '''
            Write the selected item's text to the lineEdit.
        '''
        if (self.listWidget.currentItem()):
            self.lineEdit.setText(self.listWidget.currentItem().text())
        else:
            self.lineEdit.setText("")

    def hideButtons(self):

        self.listToLineEdit()
        if not(self.lineEdit.text()==""):
            self.pushAdd.setEnabled(True)
        if self.listWidget.currentRow() == 0 :
            self.pushUp.setEnabled(False)
            self.pushDown.setEnabled(True)
        elif self.listWidget.currentRow() == self.listWidget.count()-1:
            self.pushUp.setEnabled(True)
            self.pushDown.setEnabled(False)
        else:
            self.pushDown.setEnabled(True)
            self.pushUp.setEnabled(True)
        if self.listWidget.currentRow :
            self.pushDelete.setEnabled(True)
        if (self.listWidget.count()<2):
            self.pushUp.setEnabled(False)
            self.pushDown.setEnabled(False)

    def funcPushDown(self):
        '''
        Move down the selected item in list
        '''
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        degisken = self.listWidget.currentItem().text()
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        degisken_ = self.listWidget.currentItem().text()
        self.listWidget.currentItem().setText(degisken)
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        self.listWidget.currentItem().setText(degisken_)
        self.listToLineEdit()

    def funcPushUp(self):
        '''
        Move up the selected item in list
        '''
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        degisken = self.listWidget.currentItem().text()
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        degisken_ = self.listWidget.currentItem().text()
        self.listWidget.currentItem().setText(degisken)
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        self.listWidget.currentItem().setText(degisken_)
        self.listToLineEdit()

    def setTitle(self, title):
        self.labelTitle.setText(unicode(title))

    def setOptions(self, options):
        for key, value in options.iteritems():
            if key == "choose" and self.type == "combo":
                for item in value.split("\n"):
                    name, label = item.split("\t")
                    self.comboItems.addItem(label, QtCore.QVariant(name))
            elif key == "format" and self.type in ["editlist", "text"]:
                editor = self.lineEdit
                validator = QtGui.QRegExpValidator(QtCore.QRegExp(value), self)
                editor.setValidator(validator)

    def setValue(self, value):
        value = unicode(value)
        if self.type == "combo":
            index = self.comboItems.findData(QtCore.QVariant(value))
            if index == -1:
                return
            self.comboItems.setCurrentIndex(index)
        elif self.type == "editlist":
            for item in value.split():
                self.listWidget.insertItem(0,unicode(item))
        elif self.type == "text":
            self.lineItem.setText(unicode(value))

    def getValue(self):
        if self.type == "combo":
            index = self.comboItems.currentIndex()
            return unicode(self.comboItems.itemData(index).toString())
        elif self.type == "editlist":
            items = []
            for index in range(self.listWidget.count()):
                items.append(unicode(self.listWidget.item(index).text()))
            return " ".join(items)
        elif self.type == "text":
            return unicode(self.lineItem.text())
