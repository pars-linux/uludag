#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

from qt import *
from kdecore import *
from kdeui import *

from utility import *
from profileHandler import *

class browser(QVBox):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        bar = QToolBar("lala", None, self)
        but = QToolButton(loadIconSet("add.png"), i18n("Add"), "lala", self.slotAdd, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        self.new_but = but
        but = QToolButton(bar)
        but.setEnabled(False)
        bar.setStretchableWidget(but)
        but = QToolButton(loadIconSet("help.png"), i18n("Help"), "lala", self.slotHelp, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        parseConfig()
        createModules()
        self.prflview = ProfileView(self)
        
    def slotAdd(self):
        profileHandler(self.prflview)
        
    def slotHelp(self):
        # FIXME: prepare a help document
        pass

class ProfileView(QScrollView):
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
        self.profileItems = []
        self.viewport().setPaletteBackgroundColor(KGlobalSettings.baseColor())
        self.setHScrollBarMode(self.AlwaysOff)
        self.columns = 3
        for prflname in config.sections():
            # FIXME: True parametresini duzelt. Bunun icin en son kullanilan network profiline fln bakacan.
            ProfileItem(self, prflname)
        self.myResize()

    def maxHeight(self):
        maxh = 0
        for item in self.profileItems:
            hint = item.sizeHint()
            h = hint.height()
            if h > maxh:
                maxh = h
        return maxh

    def myResize(self):
        childs = self.profileItems
        if not childs or len(childs) == 0:
            return
        
        i = 0
        w = self.width()
        maxh = self.maxHeight()
        # FIXME: add an index-value to "profile" class for sorting
##        childs.sort(key=lambda x: x.name)
        for item in childs:
            item.is_odd = i % 2
            item.setGeometry(0, i * maxh, w, maxh)
            item.update()
            i += 1
        self.resizeContents(w, i * maxh)
    
    def resizeEvent(self, event):
        size = event.size()
        self.myResize()
        QWidget.resizeEvent(self, event)
  
    def paintEvent(self, event):
        cg = self.colorGroup()
        QScrollView.paintEvent(self, event)
        paint = QPainter(self)
        paint.save()
        paint.restore()
    
    def add(self, name):
        ProfileItem(self, name)
        self.myResize()


class ProfileItem(QWidget):
    def __init__(self, view, name):
        self.is_odd = 0
        QWidget.__init__(self, view.viewport())
        self.tipper = ProfileTipper(self)
        self.tipper.parent = self
        view.profileItems.append(self)
        
        self.view = view
        if name == "noproxy":
            self.noproxy = True
            self.name = i18n("No Proxy")
        else: 
            self.noproxy = False
            self.name = name
        
        self.mypix = loadIconSet("proxy").pixmap(QIconSet.Large, QIconSet.Normal)
        self.isActive = config.getboolean(name, "isActive")
        self.check = QCheckBox(self)
        self.check.setChecked(self.isActive)
        QToolTip.add(self.check, i18n("Activate/Deactivate this proxy profile"))
        self.check.setGeometry(6, 3, 16, 16)
        self.connect(self.check, SIGNAL("toggled(bool)"), self.slotToggle)
        self.check.setAutoMask(True)
        
        w = self.check.width()
        self.pix_start = 6 + w + 3
        w = self.mypix.width()
        self.text_start = self.pix_start + w + 6
        
        if not self.noproxy:
            self.edit_but = IconButton("configure", self)
            QToolTip.add(self.edit_but, i18n("Configure this profile"))
            self.connect(self.edit_but, SIGNAL("clicked()"), self.slotEdit)
            self.del_but = IconButton("cancel", self)
            QToolTip.add(self.del_but, i18n("Delete this profile"))
            self.connect(self.del_but, SIGNAL("clicked()"), self.slotDelete)
        
        self.show()
    
    def slotToggle(self, on):
        if self.isActive or not on:
            return
        else:
            if not self.noproxy: changeProxy(self.name)
            else: changeProxy("noproxy")
            for i in self.view.profileItems:
                i.check.setChecked(False)
                i.isActive = False
            self.isActive = True
            self.check.setChecked(True)
    
    def slotDelete(self):
        m = i18n("Should I delete the\n'%s'\nproxy profile?")
        if KMessageBox.Yes == KMessageBox.questionYesNo(self, unicode(m) % self.name, i18n("Delete proxy profile?")):
            config.remove_section(self.name)
            f = open(configPath,"w")
            config.write(f)
            f.close()
            del self.view.profileItems[self.view.profileItems.index(self)]
            self.hide()
            self.view.myResize()
    
    def slotEdit(self):
        if not self.noproxy:
            profileHandler(self.parent().parent(), self.name)

    def mouseDoubleClickEvent(self, event):
        self.slotEdit()
    
    def addressText(self):
        text = "defsbsd"
        return text
    
    def paintEvent(self, event):
        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        if self.is_odd:
            col = KGlobalSettings.alternateBackgroundColor()
        if not self.noproxy:
            self.edit_but.setPaletteBackgroundColor(col)
            self.del_but.setPaletteBackgroundColor(col)
        paint.fillRect(event.rect(), QBrush(col))
        dip = (self.height() - self.mypix.height()) / 2
        paint.drawPixmap(self.pix_start, dip, self.mypix)
        paint.save()
        font = paint.font()
        font.setPointSize(font.pointSize() + 2)
        font.setBold(True)
        fm = QFontMetrics(font)
        paint.drawText(self.text_start, fm.ascent() + 5, unicode(self.name))
        fark = fm.height()
        paint.restore()
        fm = self.fontMetrics()
        paint.drawText(self.text_start, 5 + fark + 3 + fm.ascent(), self.addressText())
    
    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        dip = (h - self.check.height()) / 2
        self.check.move(6, dip)
        if not self.noproxy:
            dip = (h - self.edit_but.myHeight) / 2
            self.del_but.setGeometry(w - self.del_but.myWidth - 6 - 6, dip, self.del_but.myWidth, self.del_but.myHeight)
            self.edit_but.setGeometry(w - self.del_but.myWidth - 6 - 6 - self.edit_but.myWidth - 3, dip, self.edit_but.myWidth, self.edit_but.myHeight)
        return QWidget.resizeEvent(self, event)
    
    def sizeHint(self):
        f = QFont(self.font())
        f.setPointSize(f.pointSize() + 2)
        f.setBold(True)
        fm = QFontMetrics(f)
        fm2 = self.fontMetrics()
        rect = fm.boundingRect(unicode(self.name))
        rect2 = fm2.boundingRect(self.addressText())
        if not self.noproxy:
            w = self.text_start + min(rect.width(), 240) + 6 + self.edit_but.myWidth + 3 + self.del_but.myWidth + 6
            w2 = self.text_start + min(rect2.width(), 240) + 6 + self.edit_but.myWidth + 3 + self.del_but.myWidth + 6
        else:
            w = self.text_start + min(rect.width(), 240) + 6
            w2 = self.text_start + min(rect2.width(), 240) + 6
        w = max(w, w2)
        h = max(fm.height() + 3 + fm2.height(), 32) + 10
        return QSize(w, h)

class IconButton(QPushButton):
    def __init__(self, name, parent):
        QPushButton.__init__(self, parent)
        self.setFlat(True)
        self.myset = loadIconSet(name, KIcon.Small)
        self.setIconSet(self.myset)
        size = self.myset.iconSize(QIconSet.Small)
        self.myWidth = size.width() + 4
        self.myHeight = size.height() + 4
        self.resize(self.myWidth, self.myHeight)

class ProfileTipper(QToolTip):
    def maybeTip(self, point):
        prfl_item = self.parent
        
        rect = prfl_item.rect()
        if not self.parent.noproxy:
            rect.setWidth(rect.width() - prfl_item.del_but.myWidth - prfl_item.edit_but.myWidth - 6 - 6 - 4)
        else:
            rect.setWidth(rect.width() - 6 - 6 - 4)
        rect.setX(rect.x() + prfl_item.pix_start)
        if not rect.contains(point):
            return
        
        tip = "<nobr>"
        tip += i18n("Name:")
        tip += " <b>%s</b>" % unicode(prfl_item.name)
        tip += "</nobr>"
        self.tip(rect, tip)
