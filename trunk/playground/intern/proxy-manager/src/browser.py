#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

from khtml import KHTMLPart
import locale

from utility import *
from profileHandler import *

from profile import *

class browser(QVBox):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)
        
        bar = QToolBar("lala", None, self)
        but = QToolButton(loadIconSet("add.png"), i18n("Add"), "lala", self.slotAdd, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        but.setFocusPolicy(QWidget.TabFocus)
        self.new_but = but
        but = QToolButton(bar)
        but.setEnabled(False)
        bar.setStretchableWidget(but)
        but = QToolButton(loadIconSet("help.png"), i18n("Help"), "lala", self.slotHelp, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        but.setFocusPolicy(QWidget.TabFocus)
        self.help_but = but
        
        initProfiles()
        createModules()
        self.prflview = ProfileView(self)
        
        self.setTabOrder(self.new_but, self.help_but)
        self.setTabOrder(self.help_but, self.prflview.item_group)
        
    def slotAdd(self):
        profileHandler(self.prflview)
        
    def slotHelp(self):
        self.helpwin = HelpDialog("proxy-manager", i18n("Proxy Manager Help"), self)
        self.helpwin.show()

class ProfileView(QScrollView):
    def __init__(self, parent):
        QScrollView.__init__(self, parent)
        self.profileItems = []
        self.item_group = QButtonGroup()
        self.viewport().setPaletteBackgroundColor(KGlobalSettings.baseColor())
        self.setHScrollBarMode(self.AlwaysOff)
        self.columns = 3
        for p in profiles:
            ProfileItem(self, p)
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
        childs.sort(key=lambda x: x.prfl.type)
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
    
    def add(self, prfl):
        ProfileItem(self, prfl)
        profiles.append(prfl)
        self.myResize()


class ProfileItem(QWidget):
    def __init__(self, view, prfl):
        self.is_odd = 0
        QWidget.__init__(self, view.viewport())
        self.prfl = prfl
        self.tipper = ProfileTipper(self)
        self.tipper.parent = self
        view.profileItems.append(self)
        self.view = view
        self.mypix = loadIconSet("proxy").pixmap(QIconSet.Large, QIconSet.Normal)
        self.check = QRadioButton(self)
        self.view.item_group.insert(self.check)
        self.check.setChecked(self.prfl.isActive)
        QToolTip.add(self.check, i18n("Activate/Deactivate this proxy profile"))
        self.check.setGeometry(6, 3, 16, 16)
        self.connect(self.check, SIGNAL("toggled(bool)"), self.slotToggle)
        self.check.setAutoMask(True)
        
        w = self.check.width()
        self.pix_start = 6 + w + 3
        w = self.mypix.width()
        self.text_start = self.pix_start + w + 6
        
        if self.prfl.type != profile.direct:
            self.edit_but = IconButton("configure", self)
            QToolTip.add(self.edit_but, i18n("Configure this profile"))
            self.connect(self.edit_but, SIGNAL("clicked()"), self.slotEdit)
            self.del_but = IconButton("cancel", self)
            QToolTip.add(self.del_but, i18n("Delete this profile"))
            self.connect(self.del_but, SIGNAL("clicked()"), self.slotDelete)
        
        self.show()
    
    def slotToggle(self, on):
        if self.prfl.isActive or not on:
            return
        else:
            changeProxy(self.prfl)
            for i in self.view.profileItems:
                i.check.setChecked(False)
                i.isActive = False
            self.prfl.isActive = True
            self.check.setChecked(True)
    
    def slotDelete(self):
        m = i18n("Should I delete the\n'%s'\nproxy profile?")
        if KMessageBox.Yes == KMessageBox.questionYesNo(self, unicode(m) % self.prfl.name, i18n("Delete proxy profile?")):
            if self.prfl.isActive:
                self.view.profileItems[0].check.setChecked(True)
            profile.deleteProfile(self.prfl)
            del self.view.profileItems[self.view.profileItems.index(self)]
            self.hide()
            self.view.myResize()
    
    def slotEdit(self):
        if self.prfl.type != profile.direct:
            profileHandler(self.parent().parent(), self.prfl, self)

    def mouseDoubleClickEvent(self, event):
        self.slotEdit()
    
    def paintEvent(self, event):
        paint = QPainter(self)
        col = KGlobalSettings.baseColor()
        if self.is_odd:
            col = KGlobalSettings.alternateBackgroundColor()
        if self.prfl.type != profile.direct:
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
        paint.drawText(self.text_start, fm.ascent() + 5, unicode(self.prfl.name))
        fark = fm.height()
        paint.restore()
        fm = self.fontMetrics()
        paint.drawText(self.text_start, 5 + fark + 3 + fm.ascent(), self.prfl.comment)
    
    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        dip = (h - self.check.height()) / 2
        self.check.move(6, dip)
        if self.prfl.type != profile.direct:
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
        rect = fm.boundingRect(unicode(self.prfl.name))
        rect2 = fm2.boundingRect(self.prfl.comment)
        if self.prfl.type != profile.direct:
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
        self.setFocusPolicy(QWidget.NoFocus)

class ProfileTipper(QToolTip):
    def maybeTip(self, point):
        prfl_item = self.parent
        
        rect = prfl_item.rect()
        if prfl_item.prfl.type != profile.direct:
            rect.setWidth(rect.width() - prfl_item.del_but.myWidth - prfl_item.edit_but.myWidth - 6 - 6 - 4)
        else:
            rect.setWidth(rect.width() - 6 - 6 - 4)
        rect.setX(rect.x() + prfl_item.pix_start)
        if not rect.contains(point):
            return
        
        tip = "<nobr>"
        tip += i18n("Name:")
        tip += " <b>%s</b>" % unicode(prfl_item.prfl.name)
        tip += "</nobr>"
        self.tip(rect, tip)


class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 600)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)
        
        lang = locale.setlocale(locale.LC_MESSAGES)
        if "_" in lang:
            lang = lang.split("_", 1)[0]
        url = locate("data", "%s/help/%s/main_help.html" % (name, lang))
        if not os.path.exists(url):
            url = locate("data", "%s/help/en/main_help.html" % name)
        self.htmlPart.openURL(KURL(url))
